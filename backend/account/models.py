from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from .managers import CustomUserManager

def get_profile_image_path(self, filename):
    return f"profile_images/{self.pk}/{filename}"

def get_default_profile_image():
    return "default/default_profile.svg"


class Account(AbstractBaseUser):
    email           = models.EmailField(verbose_name="email", max_length=60, unique=True)
    username        = models.CharField(verbose_name="user name", max_length=40, unique=True)
    date_joined     = models.DateTimeField(verbose_name="date joined", auto_now_add=True)
    last_login      = models.DateTimeField(verbose_name="last login", auto_now=True)
    is_admin        = models.BooleanField(default=False)
    is_active       = models.BooleanField(default=True)
    is_staff        = models.BooleanField(default=False)
    is_superuser    = models.BooleanField(default=False)
    profile_image   = models.ImageField(max_length=200, upload_to=get_profile_image_path, default=get_default_profile_image, blank=True, null=True)
    hide_email      = models.BooleanField(default=True)

    objects = CustomUserManager()

    USERNAME_FIELD  = "email"
    REQUIRED_FIELDS = ["username"]


    def __str__(self) -> str:
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, app_lebel):
        return True
