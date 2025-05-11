from django.db import models
from accounts.models import CustomUser
from etc.choices import PRODUCT_SIZE, COLOR_CHOICES, MEDIA_TYPE_CHOICES
from etc.helper_functions import product_media_uploader

class Product(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=30, blank=False, null=False)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(max_length=500, null=False, blank=False)


class Size(models.Model):
    name = models.CharField(max_length=9,choices=PRODUCT_SIZE, null=False, blank=False, unique=True)


class Color(models.Model):
    name = models.CharField(max_length=20, choices=[(v, v) for _, v in COLOR_CHOICES], unique=True)
    color_code = models.CharField(max_length=8, choices=COLOR_CHOICES, unique=True)


class ProductColor(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['product', 'color'], name='unique_product_color')
        ]


class ProductSize(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['product', 'size'], name='unique_product_size')
        ]


class ProductMedia(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPE_CHOICES)
    file_url = models.FileField(null=False, blank=False, upload_to=product_media_uploader)
    alt_text = models.CharField(max_length=100, null=False, blank=False)
    is_main = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.file_url)

class FavoriteProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'product'], name='unique_user_favorite_product')
        ]


class Category(models.Model):
    pass


class Tag(models.Model):
    pass


class CategoryTag(models.Model):
    pass


class ProductCategory(models.Model):
    pass


class Sale(models.Model):
    pass

class Review(models.Model):
    pass

