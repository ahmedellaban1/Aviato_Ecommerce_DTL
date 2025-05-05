from django.contrib import admin
from .models import CustomUser
# Register your models here.
class CustomAdmin(admin.ModelAdmin):
    list_display = ('username', 'type', 'email', 'is_superuser', 'is_staff', 'is_active')
    search_fields = ('username', 'email')
    list_filter = ('type', 'is_superuser', 'is_staff', 'is_active')


admin.site.register(CustomUser, CustomAdmin)