from typing import Optional, List

import strawberry_django
from django.contrib.auth import get_user_model
from strawberry.types import Info
from gqlauth.core.types_ import GQLAuthError, GQLAuthErrors
from gqlauth.core.utils import get_user
from .types import UserFilter, ExtendedUserType
from django.contrib.auth.models import Group

USER_MODEL = get_user_model()


@strawberry_django.type(model=USER_MODEL, filters=UserFilter)
class UserQueries:
    @strawberry_django.field(description="Returns the current user if he is not anonymous.")
    def public_user(self, info: Info) -> Optional[ExtendedUserType]:
        user = get_user(info)
        if not user.is_anonymous:
            return user  # type: ignore
        return None

    @strawberry_django.field()
    def me(self, info: Info) -> ExtendedUserType:
        user = get_user(info)
        if not user.is_authenticated:
            raise GQLAuthError(code=GQLAuthErrors.UNAUTHENTICATED)
        return user  # type: ignore

    @strawberry_django.field()
    def get_grupos_usuario(self, info) -> Optional[List[str]]:
        user = get_user(info)
        if user.is_authenticated:
            groups: List = list(user.groups.values_list('name', flat=True))
            if user.is_superuser:
                groups.append('Admin')
            return groups
        return None

    @strawberry_django.field()
    def get_grupos_list(self, _info: Info) -> List[str]:
        return [grupo.name for grupo in Group.objects.all()]

    @strawberry_django.field()
    def authenticated(self, info: Info) -> bool:
        user = get_user(info)
        if user.is_authenticated:
            return True
        return False