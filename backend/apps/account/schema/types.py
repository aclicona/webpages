# backend/apps/account/types.py
import os
from dataclasses import dataclass
from typing import Optional, Any, List

import strawberry
import strawberry_django
from django.conf import settings
from django.core.exceptions import ValidationError
from gqlauth.core.utils import inject_fields
from gqlauth.user.types_ import USER_MODEL, USER_FIELDS, UserFilter, UserStatusType
from strawberry import auto
from strawberry.types import Info


@dataclass
class ImageValidator:
    """Validates image-related operations"""
    MAX_SIZE_MB: int = 5
    ALLOWED_EXTENSIONS: tuple[str, ...] = ('jpg', 'jpeg', 'png', 'webp')

    @classmethod
    def validate_image(cls, image: Any) -> None:
        """Validates image size and format"""
        if not image:
            return

        if image.size > cls.MAX_SIZE_MB * 1024 * 1024:
            raise ValidationError(f"Image size must be less than {cls.MAX_SIZE_MB}MB")

        ext = image.name.split('.')[-1].lower()
        if ext not in cls.ALLOWED_EXTENSIONS:
            raise ValidationError(f"Image must be one of: {', '.join(cls.ALLOWED_EXTENSIONS)}")


@strawberry.scalar(description="Custom scalar for handling image URLs with validation and default fallback")
class ImageURL:
    """
    Custom scalar for handling image URLs with built-in validation and error handling.
    Provides secure serialization and parsing of image fields with default fallback.
    """
    DEFAULT_IMAGE_PATH = 'images/userplaceholder.jpg'  # Default image in static files

    @classmethod
    def get_default_image_url(cls) -> str:
        """Returns the URL for the default image with proper validation"""
        media_path = os.path.join(settings.MEDIA_ROOT, cls.DEFAULT_IMAGE_PATH)
        static_path = os.path.join(settings.STATIC_ROOT, cls.DEFAULT_IMAGE_PATH)

        if hasattr(settings, 'MEDIA_URL') and os.path.exists(media_path):
            return f"{settings.MEDIA_URL.rstrip('/')}/{cls.DEFAULT_IMAGE_PATH}"
        elif os.path.exists(static_path):
            return f"{settings.STATIC_URL.rstrip('/')}/{cls.DEFAULT_IMAGE_PATH}"
        else:
            return ""  # O una URL por defecto garantizada


@strawberry_django.type(
    model=USER_MODEL,
    filters=UserFilter,
    description="Extended user type with additional fields and functionality"
)
@inject_fields(USER_FIELDS, annotations_only=True)
class ExtendedUserType:
    """
    Extended user type that includes additional fields and computed properties.
    Provides a comprehensive representation of user data for GraphQL queries.
    """
    logentry_set: auto
    is_superuser: auto
    last_login: auto
    is_staff: auto
    is_active: auto
    date_joined: auto
    status: UserStatusType

    @strawberry_django.field(description="Check if user account is archived")
    def archived(self, info: Info) -> bool:
        """Returns whether the user account is archived"""
        return bool(self.status.archived)

    @strawberry_django.field(description="Check if user account is verified")
    def verified(self, info: Info) -> bool:
        """Returns whether the user account is verified"""
        return bool(self.status.verified)

    @strawberry_django.field(description="Get user's display name")
    def display_name(self, info: Info) -> str:
        """Returns the user's display name, falling back to email if name is not set"""
        return self.get_full_name() or self.email

    @strawberry_django.field(description="Get user's permissions")
    def permissions(self, info: Info) -> list[str]:
        """Returns list of user's permissions"""
        return sorted(
            f"{perm.content_type.app_label}.{perm.codename}"
            for perm in self.user_permissions.all()
        )

    @strawberry_django.field(description="Get user's permissions")
    def image(self, info) -> str:
        if self.image:
            return self.image.url
        try:
            return self.optional_image.url
        except:
            return ""

    @strawberry_django.field(description="Get user's permissions")
    def avatar(self, info) -> str:
        if self.image:
            return self.image.crop['50x50'].url
        try:
            return self.optional_image.url
        except:
            return ""


@strawberry.type
class UserActionResponse:
    """
    Generic response type for user-related actions.
    Provides a consistent structure for mutation responses.
    """
    success: bool
    message: str
    errors: Optional[list[str]] = None
    user: Optional[ExtendedUserType] = None


@strawberry.type
class LogoutResponse(UserActionResponse):
    """
    Specific response type for logout mutation.
    Inherits from UserActionResponse for consistency.
    """
    refresh_token: Optional[str] = None

@strawberry.input
class GroupInput:
    name: str
    add: bool  # Use 'add' instead of 'should_add' for clarity



@strawberry.type
class CreateStaffUserSuccess:
    success: bool


@strawberry.input
class CreateStaffUserInput:
    first_name: str
    last_name: Optional[str]
    email: str
    groups: List[GroupInput]