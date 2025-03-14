import os

from django.conf import settings
from django.contrib.auth.models import (
    AbstractUser,
    BaseUserManager,
)
from django.db import models
from django.dispatch import receiver
from versatileimagefield.fields import VersatileImageField, PPOIField
from versatileimagefield.image_warmer import VersatileImageFieldWarmer
from versatileimagefield.placeholder import OnDiscPlaceholderImage


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    email = models.EmailField("email address of user", unique=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    image = VersatileImageField(
        upload_to="user", ppoi_field="ppoi", blank=True, null=True
    )
    ppoi = PPOIField()
    optional_image = VersatileImageField(
        "Optional Image",
        upload_to="images/usuarios/cuenta",
        blank=True,
        placeholder_image=OnDiscPlaceholderImage(
            path=os.path.join(settings.STATICFILES_DIRS[0], "images/userplaceholder.jpg")
        ),
    )

    objects = UserManager()


@receiver(models.signals.post_save, sender=User)
def warm_user_images(sender, instance, **kwargs):
    """Ensures Person head shots are created post-save"""
    user_img_warmer = VersatileImageFieldWarmer(
        instance_or_queryset=instance,
        rendition_key_set='user_image',
        image_attr='image'
    )
    num_created, failed_to_create = user_img_warmer.warm()
