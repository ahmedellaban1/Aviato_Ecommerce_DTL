from django.db import models
from django.contrib.auth.models import AbstractUser
from django_countries.fields import CountryField
from django.db.models.signals import post_save
from django.dispatch import receiver
from etc.choices import USER_TYPE_CHOICES, GENDER_CHOICES
# Create your models here.
class CustomUser(AbstractUser):
    type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username

class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    image = models.ImageField(upload_to='', null=True, blank=True)
    country = CountryField(blank_label='(select country)')
    phone = models.CharField(max_length=15)
    date_of_birth = models.DateField(help_text="Format: YYYY-MM-DD")
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @receiver(post_save, sender=CustomUser)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    def __str__(self):
        return f"{self.user.username}'s profile"


