from django.contrib import admin
from .models import Invoice, OrderItem, ProductVariant, PaymentLog
# Register your models here.


# Admin configuration for the Invoice model
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('user', 'status', 'paid_at', 'created_at')
    search_fields = ('user', 'status', 'shipping_address')
    list_filter = ('status', )


# Admin configuration for the OrderItem model
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('invoice', 'quantity',)
    search_fields = ('product', 'invoice',)
    # list_filter = ('invoice__status', )


# Admin configuration for the ProductVariant model
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ('product', 'color', 'size')
    search_fields = ('product',)


# Admin configuration for the PaymentLog model
class PaymentLogAdmin(admin.ModelAdmin):
    list_display = ('invoice', 'payment_method_info', 'status')
    search_fields = ('payment_method_info', 'status', 'user_ip_address')
    list_filter = ('payment_method_info', 'status')


admin.site.register(Invoice, InvoiceAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(ProductVariant, ProductVariantAdmin)
admin.site.register(PaymentLog, PaymentLogAdmin)
