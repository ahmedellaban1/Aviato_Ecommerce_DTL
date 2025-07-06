from django.db import models
from accounts.models import CustomUser
from etc.choices import PRODUCT_SIZE, COLOR_CHOICES, MEDIA_TYPE_CHOICES
from etc.helper_functions import product_media_uploader, category_media_uploader
from django.utils.text import slugify
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.db.models import Q



class Product(models.Model):
    # Main product model containing essential product information
    # Links to a user (seller) who created the product
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=30, blank=False, null=False)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(max_length=500, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        # String representation for admin interface and debugging
        return f"{self.title}-{self.user}"


class Size(models.Model):
    # Model to store available product sizes
    # Uses predefined choices from PRODUCT_SIZE
    name = models.CharField(max_length=9,choices=PRODUCT_SIZE, null=False, blank=False, unique=True)

    def __str__(self):
        return self.name


class Color(models.Model):
    # Model to store available product colors
    # Stores both color name and hex code
    name = models.CharField(max_length=20, choices=[(v, v) for _, v in COLOR_CHOICES], unique=True)
    color_code = models.CharField(max_length=8, choices=COLOR_CHOICES, unique=True)

    def __str__(self):
        return f"{self.name} - code : {self.color_code}"


class ProductColor(models.Model):
    # Junction table to create many-to-many relationship between Product and Color
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            # Ensure each color is only added once per product
            models.UniqueConstraint(fields=['product', 'color'], name='unique_product_color')
        ]

    def __str__(self):
        return f"product : {self.product} - color : {self.color}"


class ProductSize(models.Model):
    # Junction table to create many-to-many relationship between Product and Size
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            # Ensure each size is only added once per product
            models.UniqueConstraint(fields=['product', 'size'], name='unique_product_size')
        ]

    def __str__(self):
        return f"product : {self.product} - size : {self.size}"


class ProductMedia(models.Model):
    # Store media files (images/videos) related to products
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPE_CHOICES)
    file_url = models.FileField(null=False, blank=False, upload_to=product_media_uploader)
    alt_text = models.CharField(max_length=100, null=False, blank=False)
    is_main = models.BooleanField(default=False)  # Flag for primary product image
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['product'],
                condition=Q(is_main=True),
                name='unique_main_image_per_product'
            )
        ]

    def __str__(self):
        return str(self.file_url)


class FavoriteProduct(models.Model):
    # Tracks which products users have marked as favorites
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            # Ensure a user can only favorite a product once
            models.UniqueConstraint(fields=['user', 'product'], name='unique_user_favorite_product')
        ]

    def __str__(self):
        return f"product : {self.product} - user : {self.user}"


class Category(models.Model):
    # Store product categories
    title = models.CharField(max_length=20, null=False, blank=False, unique=True)
    description = models.TextField(
        max_length=1000, null=False, blank=False,
        help_text="explain info about product in this category" # Help text for admin
    )
    slug = models.SlugField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Auto-generate slug from title if not provided
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} - tags : {self.slug}"


class CategoryMedia(models.Model):
    # Store media related to categories (e.g., category banner images)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPE_CHOICES)
    file_url = models.FileField(null=False, blank=False, upload_to=category_media_uploader)
    alt_text = models.CharField(max_length=100, null=False, blank=False)
    is_main = models.BooleanField(default=False, help_text="cover image in case of true")   # Main category image flag
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.file_url)


class Tag(models.Model):
    # Store tags for categorizing products
    name = models.CharField(max_length=10, null=False, blank=False, unique=True)

    def clean(self):
        # Custom validation to ensure tags don't contain spaces
        if ' ' in self.name:
            raise ValidationError("Tag name must be a single word without spaces.")

    def save(self, *args, **kwargs):
        self.full_clean()  # ensures clean() and field validation runs
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class CategoryTag(models.Model):
    # Junction table for many-to-many relationship between Category and Tag
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            # Ensure each tag is only used once per category
            models.UniqueConstraint(fields=['category', 'tag'], name='unique_category_tag')
        ]
    def __str__(self):
        return f"category : {self.category} - tag : {self.tag}"


class ProductCategory(models.Model):
    # Junction table for many-to-many relationship between Product and Category
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            # Ensure a product is only in each category once
            models.UniqueConstraint(fields=['product', 'category'], name='unique_product_category')
        ]
    def __str__(self):
        return f"product : {self.product} - category : {self.category}"


class Sale(models.Model):
    # Track product discounts and promotions
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    discount_percent = models.DecimalField(max_digits=5, decimal_places=2)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=False, blank=False)
    is_active = models.BooleanField(default=True)

    def is_currently_active(self):
        # Helper method to check if sale is currently valid
        now = timezone.now()
        return self.is_active and self.start_date <= now <= self.end_date

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['product'],
                condition=Q(is_active=True),
                name='only_one_active_sale_per_product'
            )
        ]
    def __str__(self):
        return f"{self.product} - {self.discount_percent}% off"


class Review(models.Model):
    # Store product reviews with ability to have threaded comments
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    comment = models.CharField(max_length=100, null=False, blank=False)
    parent = models.ForeignKey(
        'self',   # Self-reference for comment threading
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='replies' # How to access child comments
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            # Ensure a user can only leave one parent-level review per product
            models.UniqueConstraint(
                fields=['product'],
                condition=models.Q(parent__isnull=True),
                name='unique_parent_comment_per_product'
            )
        ]

    def __str__(self):
        return f"{self.user} - {self.comment[:30]}{' (reply)' if self.parent else ''}"


