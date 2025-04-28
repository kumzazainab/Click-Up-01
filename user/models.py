from django.db import models
import uuid
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from home.models import UUIDModel
from user.utils import ROLE_CHOICES, APPEARANCE_CHOICES, LanguageSelector, THEME_COLORS, TIMEZONE_CHOICES


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True, null=True, blank=True)
    role = models.CharField(max_length=200, choices=ROLE_CHOICES)
    password = models.CharField(max_length=128)

    def __str__(self):
        return self.email


class Profile(UUIDModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    full_name = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    password = models.CharField(max_length=128)
    appearance = models.CharField(max_length=20, choices=APPEARANCE_CHOICES)
    theme_color = models.CharField(max_length=20, choices=THEME_COLORS, default='green')
    language = models.CharField(max_length=20, choices=LanguageSelector, default='English')
    timezone = models.CharField(max_length=250, choices=TIMEZONE_CHOICES)

    def __str__(self):
        return self.full_name