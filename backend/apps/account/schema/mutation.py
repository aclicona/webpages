import strawberry
import strawberry_django
from asgiref.sync import sync_to_async
from django.apps import apps
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.exceptions import ObjectDoesNotExist
from gqlauth.core.constants import TokenAction
from gqlauth.models import RefreshToken
from gqlauth.settings import gqlauth_settings as app_settings
from gqlauth.user import arg_mutations as mutations
from strawberry.types import Info

from .types import CreateStaffUserSuccess, CreateStaffUserInput
from .types import LogoutResponse
from .utils import random_string
from ...core.send_mails import send_html_mail


@sync_to_async
def get_email_context(new_user, info):
    return new_user.status.get_email_context(info, app_settings.PASSWORD_RESET_PATH_ON_EMAIL,
                                             TokenAction.PASSWORD_RESET)

class CreateStaffUser:
    """
        Mutation to create a staff user.
        """

    @classmethod
    async def mutate(cls, root, info: Info, input: CreateStaffUserInput) -> CreateStaffUserSuccess:
        user = info.context.user if hasattr(info.context, 'user') and info.context.user.is_authenticated else None

        if not user or not user.is_staff:
            raise PermissionError('No dispone de permisos para crear usuarios de Staff')

        password = random_string()
        user_model = apps.get_model(settings.AUTH_USER_MODEL)

        # Create user
        new_user = await user_model.objects.acreate(
            first_name=input.first_name,
            last_name=input.last_name,
            email=input.email,
        )

        # Set password
        new_user.set_password(password)

        # Handle groups
        for group_input in input.groups:
            if group_input.add:
                try:
                    group = await Group.objects.aget(name=group_input.name)
                    await new_user.groups.aadd(group)
                except Group.DoesNotExist:
                    continue

        await new_user.asave()
        email_context = await get_email_context(new_user, info)
        send_html_mail(
            f'Bienvenido al equipo de {settings.SITE_NAME}',
            'account_staff_creation_email.html',
            [input.email],
            email_context
        )
        return CreateStaffUserSuccess(success=True)

    @classmethod
    def field(cls):
        """Generate field for schema registration"""
        return strawberry.mutation(
            resolver=cls.mutate,
            description=cls.__doc__
        )

class UpdateStaffUser:
    """
        Mutation to update a staff user.
        """

    @classmethod
    async def mutate(cls, root, info: Info, input: CreateStaffUserInput) -> CreateStaffUserSuccess:
        user = info.context.user if hasattr(info.context, 'user') and info.context.user.is_authenticated else None

        if not user or not user.is_staff:
            raise PermissionError('No dispone de permisos para crear usuarios de Staff')

        password = random_string()
        user_model = apps.get_model(settings.AUTH_USER_MODEL)

        # Create user
        new_user = await user_model.objects.acreate(
            first_name=input.first_name,
            last_name=input.last_name,
            email=input.email,
        )

        # Set password
        new_user.set_password(password)

        # Handle groups
        for group_input in input.groups:
            if group_input.add:
                try:
                    group = await Group.objects.aget(name=group_input.name)
                    await new_user.groups.aadd(group)
                except Group.DoesNotExist:
                    continue

        await new_user.asave()
        email_context = await get_email_context(new_user, info)
        send_html_mail(
            f'Bienvenido al equipo de {settings.SITE_NAME}',
            'account_staff_creation_email.html',
            [input.email],
            email_context
        )
        return CreateStaffUserSuccess(success=True)

    @classmethod
    def field(cls):
        """Generate field for schema registration"""
        return strawberry.mutation(
            resolver=cls.mutate,
            description=cls.__doc__
        )


# Define the logout mutation class
class LogoutUser:
    """
    Mutation to handle user logout by revoking refresh tokens
    and cleaning up session data
    """

    @classmethod
    async def mutate(cls, root, info: Info) -> LogoutResponse:
        try:
            # Get the current user from the context
            user = info.context.request.user
            if not user.is_authenticated:
                return LogoutResponse(
                    success=False,
                    errors=["Not authenticated"],
                    message="User is not logged in"
                )

            # Find and revoke all refresh tokens for the user
            await RefreshToken.objects.filter(user=user).adelete()

            # Clear session data if using session authentication
            if hasattr(info.context, 'session'):
                if hasattr(info.context.session, 'aflush'):
                    await info.context.session.aflush()
                else:
                    # Otherwise use sync version in async context
                    import asyncio
                    await asyncio.to_thread(info.context.session.flush)

            return LogoutResponse(
                success=True,
                message="Successfully logged out"
            )

        except ObjectDoesNotExist:
            return LogoutResponse(
                success=False,
                errors=["User not found"],
                message="Unable to process logout"
            )
        except Exception as e:
            return LogoutResponse(
                success=False,
                errors=[str(e)],
                message="An error occurred during logout"
            )

    @classmethod
    def field(cls):
        """Generate field for schema registration"""
        return strawberry.mutation(
            resolver=cls.mutate,
            description=cls.__doc__
        )


@strawberry_django.type(model=get_user_model())
class UserMutations:
    verify_token = mutations.VerifyToken.field
    update_account = mutations.UpdateAccount.field
    archive_account = mutations.ArchiveAccount.field
    delete_account = mutations.DeleteAccount.field
    password_change = mutations.PasswordChange.field
    login_auth_token = mutations.ObtainJSONWebToken.field
    register_user = mutations.Register.field
    verify_account = mutations.VerifyAccount.field
    resend_activation_email = mutations.ResendActivationEmail.field
    send_password_reset_email = mutations.SendPasswordResetEmail.field
    password_reset = mutations.PasswordReset.field
    password_set = mutations.PasswordSet.field
    refresh_token = mutations.RefreshToken.field
    revoke_token = mutations.RevokeToken.field
    logout_user = LogoutUser.field()
    create_staff_user = CreateStaffUser.field()
