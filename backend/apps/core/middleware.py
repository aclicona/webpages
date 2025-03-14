from dataclasses import dataclass
from datetime import datetime
import json
from typing import Optional, Dict, Any, List, Tuple, Union
import zstd
import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from django.http import HttpRequest, HttpResponse
from django.core.cache import cache
from gqlauth.models import RefreshToken
from gqlauth.settings_type import decode_jwt as jwt_decode_jwt
from gqlauth.settings_type import create_token_type
from functools import lru_cache
from gqlauth.core.constants import JWT_PREFIX


@dataclass
class TokenConfig:
    """Configuration class for token-related settings to improve maintainability"""
    REFRESH_TOKEN_COOKIE: str = 'refreshToken'
    ACCESS_TOKEN_COOKIE: str = 'accessToken'
    COOKIE_MAX_AGE: int = 60 * 60 * 24 * 5  # 5 days
    CACHE_TTL: int = 300  # 5 minutes
    TOKEN_BLACKLIST_PREFIX: str = 'blacklisted_token:'


class TokenService:
    """Service class for token-related operations with improved error handling and caching"""

    def __init__(self, secret_key: str = settings.SECRET_KEY):
        self.secret_key = secret_key
        self.algorithm = "HS256"

    @lru_cache(maxsize=1000)
    def _cached_encode(self, payload_tuple: Tuple[Tuple[str, Any], ...]) -> str:
        """Internal method to handle the actual caching of encoded tokens"""
        payload_dict = dict(payload_tuple)
        # Convert string-encoded values back to their original format
        for key, value in payload_dict.items():
            try:
                if isinstance(value, str) and (value.startswith('{') or value.startswith('[')):
                    payload_dict[key] = json.loads(value)
            except (json.JSONDecodeError, ValueError):
                continue
        return jwt.encode(payload_dict, self.secret_key, algorithm=self.algorithm)

    @staticmethod
    def _make_payload_hashable(payload: Dict[str, Any]) -> Tuple[Tuple[str, Any], ...]:
        """Convert dictionary payload to a hashable tuple format"""
        return tuple(sorted((k, json.dumps(v) if isinstance(v, (dict, list)) else v)
                            for k, v in payload.items()))

    def encode_jwt(self, payload: Dict[str, Any]) -> str:
        """
        Encode JWT with caching for frequently used payloads.
        Converts the payload to a hashable format before caching.

        Args:
            payload: Dictionary containing the JWT claims

        Returns:
            str: Encoded JWT token

        Raises:
            jwt.InvalidTokenError: If token encoding fails
        """
        try:
            hashable_payload = self._make_payload_hashable(payload)
            return self._cached_encode(hashable_payload)
        except Exception as e:
            raise jwt.InvalidTokenError(f"Failed to encode token: {str(e)}")

    def decode_jwt(self, token: str) -> Optional[Dict[str, Any]]:
        """
        Decode JWT with comprehensive error handling and token blacklist check.
        Returns None for invalid or blacklisted tokens.
        """
        if self._is_token_blacklisted(token):
            return None

        try:
            return jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
        except jwt.InvalidTokenError:
            return None

    @staticmethod
    def _is_token_blacklisted(token: str) -> bool:
        """Check if token is blacklisted using Redis cache"""
        cache_key = f"{TokenConfig.TOKEN_BLACKLIST_PREFIX}{token}"
        return bool(cache.get(cache_key))

    @staticmethod
    def blacklist_token(token: str) -> None:
        """Blacklist a token using Redis cache"""
        cache_key = f"{TokenConfig.TOKEN_BLACKLIST_PREFIX}{token}"
        cache.set(cache_key, True, TokenConfig.COOKIE_MAX_AGE)


class UserService:
    """Service class for user-related operations with caching and optimization"""

    def __init__(self):
        self.UserModel = get_user_model()

    @lru_cache(maxsize=100)
    def get_user_groups(self, user_id: int) -> List[str]:
        """Cache user groups to reduce database queries"""
        user = self.UserModel.objects.prefetch_related('groups').get(id=user_id)
        return list(user.groups.values_list('name', flat=True))

    def invalidate_user_cache(self, user_id: int) -> None:
        """Invalidate user-related cache entries"""
        self.get_user_groups.cache_clear()


class CookieManager:
    """Manages secure cookie operations with enhanced security features"""

    @staticmethod
    def get_secure_cookie_params(http_only: bool = True) -> Dict[str, Any]:
        """Get secure cookie parameters with CSRF protection"""
        return {
            'max_age': TokenConfig.COOKIE_MAX_AGE,
            'httponly': http_only,
            'secure': not settings.DEBUG,
            'samesite': 'Lax',
            'path': '/',
            # 'domain': settings.SESSION_COOKIE_DOMAIN
        }

    @classmethod
    def set_auth_cookies(cls, response: HttpResponse, token: str, refresh_token: str) -> None:
        """Set authentication cookies with enhanced security"""
        cookie_params = cls.get_secure_cookie_params()

        # Set refresh token with encryption
        response.set_cookie(
            TokenConfig.REFRESH_TOKEN_COOKIE,
            refresh_token,
            **cookie_params
        )
        # Set refresh token with encryption
        response.set_cookie(
            TokenConfig.ACCESS_TOKEN_COOKIE,
            token,
            **cookie_params
        )


    @staticmethod
    def clear_auth_cookies(response: HttpResponse) -> None:
        """Clear all authentication cookies securely"""
        for cookie in (
                TokenConfig.ACCESS_TOKEN_COOKIE, TokenConfig.REFRESH_TOKEN_COOKIE):
            response.delete_cookie(cookie, path='/', domain=settings.SESSION_COOKIE_DOMAIN)


class JWTMiddleware:
    """
    Enhanced JWT middleware with improved architecture and performance optimizations.
    Implements a service-based architecture for better separation of concerns.
    """

    def __init__(self, get_response):
        self.get_response = get_response
        self.token_service = TokenService()
        self.user_service = UserService()
        self.cookie_manager = CookieManager()

    def _create_auth_payload(self, user) -> Dict[str, Any]:
        """Create authentication payload with additional security claims"""
        now = datetime.utcnow()
        username_field = get_user_model().USERNAME_FIELD
        iat = int(now.timestamp())
        exp = int(iat + settings.GRAPHQL_JWT['JWT_EXPIRATION_DELTA'].total_seconds())
        return {
            username_field: getattr(user, username_field),
            'exp': exp,
            'origIat': iat
        }

    def _process_refresh_token(self, request: HttpRequest) -> Tuple[Optional[str], bool]:
        """Process refresh token and return new access token if valid"""
        header = request.headers.get(TokenConfig.REFRESH_TOKEN_COOKIE)
        refresh_token = header or request.COOKIES.get(TokenConfig.REFRESH_TOKEN_COOKIE)
        if not refresh_token:
            return None, False
        try:
            instance = RefreshToken.objects.select_related('user').get(
                token=refresh_token
            )
            if not instance.is_expired_():
                token = create_token_type(instance.user)
                return getattr(token, 'token'), False
            # Refresh token is expired and must be revoked
            instance.revoke()
            return None, True
        except RefreshToken.DoesNotExist:
            return None, True

    @staticmethod
    def _process_access_token(request: HttpRequest):
        authorization_token = request.headers.get('Authorization')
        if authorization_token and authorization_token.startswith(JWT_PREFIX):
            authorization_token = authorization_token[len(JWT_PREFIX):].strip(" ")
        access_token = authorization_token or request.COOKIES.get(TokenConfig.ACCESS_TOKEN_COOKIE)
        if access_token:
            if not jwt_decode_jwt(access_token).is_expired():
                return access_token, False
            return None, True
        return None, True

    def _handle_response_content(self, response: HttpResponse, remove_cookie: bool, new_access_token=None) -> None:
        """Handle response content and manage authentication state"""
        try:
            content_type = response.headers.get('Content-Type', '')
            if 'application/json' in content_type:
                # For JSON responses
                try:
                    str_content_response = zstd.decompress(response.content)
                except:
                    str_content_response = response.content.decode('utf-8')
            else:
                # For other content types, try to decode or handle accordingly
                # For JSON responses
                try:
                    str_content_response = zstd.decompress(response.content)
                except:
                    str_content_response = response.content.decode('utf-8')
            content = json.loads(str_content_response)

            # Handle authentication operations
            if 'loginAuthToken' in str(content) or 'registerUser' in str(content):
                token = self._extract_tokens(content, 'token')
                refresh_token = self._extract_tokens(content, 'refreshToken')
                if token and refresh_token:
                    self.cookie_manager.set_auth_cookies(response, token, refresh_token)

            # Handle logout or token removal
            if 'logoutUser' in str(content) or remove_cookie:
                current_token = response.cookies.get(TokenConfig.REFRESH_TOKEN_COOKIE)
                if current_token:
                    self.token_service.blacklist_token(current_token.value)
                self.cookie_manager.clear_auth_cookies(response)
            if new_access_token:
                cookie_params = CookieManager().get_secure_cookie_params()
                response.set_cookie(
                    TokenConfig.ACCESS_TOKEN_COOKIE,
                    new_access_token,
                    **cookie_params
                )
        except json.JSONDecodeError:
            pass

    @staticmethod
    def _extract_tokens(data: Dict[str, Any], key_search: str) -> Optional[str]:
        """Extract refresh token using efficient iteration"""
        queue = [(k, v) for k, v in data.items()]
        while queue:
            key, value = queue.pop(0)
            if key == key_search and isinstance(value, dict):
                return value.get('token')
            if isinstance(value, dict):
                queue.extend(value.items())
        return None

    def __call__(self, request: HttpRequest) -> HttpResponse:
        """Process the request/response cycle with enhanced error handling"""
        remove_cookie = False
        access_token, require_new_access_token = self._process_access_token(request)
        if access_token and not require_new_access_token:
            token = access_token
        elif not access_token and require_new_access_token:
            token, remove_cookie = self._process_refresh_token(request)
        else:
            token = None
        if token:
            request.META['HTTP_AUTHORIZATION'] = f'{JWT_PREFIX}{token}'
            request.headers._store['authorization'] = ('authorization', f'{JWT_PREFIX}{token}')
        response = self.get_response(request)
        if hasattr(response, 'content'):
            if not require_new_access_token:
                self._handle_response_content(response, remove_cookie)
            else:
                self._handle_response_content(response, remove_cookie, token)
        return response
