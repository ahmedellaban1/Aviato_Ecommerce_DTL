from django.db import models
from django.contrib.auth.models import AbstractUser
from etc.choices import USER_TYPE_CHOICES
# Create your models here.
class CustomUser(AbstractUser):
    type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username