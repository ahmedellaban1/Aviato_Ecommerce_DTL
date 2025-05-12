from django.contrib import admin
from .models import CustomUser, Profile, Address
# Register your models here.
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'type', 'email', 'is_superuser', 'is_staff', 'is_active')
    search_fields = ('username', 'email')
    list_filter = ('type', 'is_superuser', 'is_staff', 'is_active')

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'country', 'gender')
    search_fields = ('country', 'gender')
    list_filter = ('gender',)

class AddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'country', 'company')
    search_fields = ('country', 'company')
    list_filter = ('country',)

admin.site.register(CustomUser, CustomAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Address, AddressAdmin)