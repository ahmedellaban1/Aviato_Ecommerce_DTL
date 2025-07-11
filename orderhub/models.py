# Importing necessary modules from Django and other apps
from django.db import models
from accounts.models import CustomUser, Address
from etc.choices import INVOICE_STATUS, PAYMENT_LOG_STATUS # Enum-like status choices
from products.models import Product, ProductSize, ProductColor


# Represents a customer invoice / order
class Invoice(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=8, decimal_places=2, null=True)
    status = models.CharField(max_length=9, choices=INVOICE_STATUS, default=INVOICE_STATUS[0][0])
    shipping_fee = models.DecimalField(max_digits=8, decimal_places=2, null=True)
    shipping_address_id = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True)
    paid_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


# Represents a specific product variant (e.g., red T-shirt, size M)
class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    color = models.ForeignKey(ProductColor, on_delete=models.SET_NULL, null=True)
    size = models.ForeignKey(ProductSize, on_delete=models.SET_NULL, null=True)


# Represents a single item in an invoice (can have multiple per invoice)
class OrderItem(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(ProductVariant, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveSmallIntegerField()
    total_price = models.DecimalField(max_digits=8, decimal_places=2, null=True)


# Stores information about a payment attempt related to an invoice
class PaymentLog(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.SET_NULL, null=True)
    payment_method_info = models.CharField(max_length=4, null=False, blank=False)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    status = models.CharField(max_length=20, choices=PAYMENT_LOG_STATUS, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    user_ip_address = models.GenericIPAddressField(null=True, blank=True)
