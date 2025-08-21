from django.db import models
from django.contrib.auth.models import AbstractUser
from django_countries.fields import CountryField
from django.db.models.signals import post_save
from django.dispatch import receiver
from etc.choices import USER_TYPE_CHOICES, GENDER_CHOICES
from etc.helper_functions import profile_image_uploader
from django.utils import timezone
from django.contrib.auth.hashers import make_password
from datetime import timedelta  


class CustomUser(AbstractUser):
    type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.is_active = False
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.username

class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    image = models.ImageField(upload_to=profile_image_uploader, null=True, blank=True)
    country = CountryField(blank_label='(select country)')
    phone = models.CharField(max_length=15)
    date_of_birth = models.DateField(help_text="Format: YYYY-MM-DD")
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def country_name(self):
        return self.country.name
    
    @receiver(post_save, sender=CustomUser)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance,date_of_birth='2000-01-01')

    def __str__(self):
        return f"{self.user.username}'s profile"


class Address(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    company = models.CharField(max_length=20)
    address = models.CharField(max_length=255)
    country = CountryField(blank_label='(select country)')
    phone = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_appear = models.DateTimeField(null=True, blank=True)
    
    @property
    def country_name(self):
        return self.country.name
    
    def __str__(self):
        return f"{self.user}-{self.address}"
    

class OTP(models.Model):
    user = models.ForeignKey(CustomUser, related_name="user_otp", null=False, blank=False, on_delete=models.CASCADE)
    otp_code = models.CharField(max_length=6, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    updated_at = models.DateTimeField(auto_now=True)
    is_used = models.BooleanField(default=False)
    attempts_count = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        # Only generate OTP if this is a new object (no pk yet)
        if not self.pk:
            self.otp_code = make_password(self.otp_code)
            self.expires_at = timezone.now() + timedelta(minutes=5)
            super().save(*args, **kwargs)
            return None
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user} - {self.is_used}"
    