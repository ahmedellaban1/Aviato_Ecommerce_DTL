from django.contrib import admin
from .models import CustomUser, Profile
# Register your models here.
class CustomAdmin(admin.ModelAdmin):
    list_display = ('username', 'type', 'email', 'is_superuser', 'is_staff', 'is_active')
    search_fields = ('username', 'email')
    list_filter = ('type', 'is_superuser', 'is_staff', 'is_active')

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'country', 'gender')
    search_fields = ('user', 'country', 'gender')
    list_filter = ('gender',)

admin.site.register(CustomUser, CustomAdmin)
admin.site.register(Profile, ProfileAdmin)