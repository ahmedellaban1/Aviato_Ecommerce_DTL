from django.contrib import admin
from .models import(
    Product, Size, Color, ProductColor, ProductSize, ProductMedia,
    Category, Tag, CategoryTag, ProductCategory, Sale, Review, FavoriteProduct
)


admin.site.register(Product)
admin.site.register(Size)
admin.site.register(Color)
admin.site.register(ProductColor)
admin.site.register(ProductSize)
admin.site.register(ProductMedia)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(CategoryTag)
admin.site.register(ProductCategory)
admin.site.register(Sale)
admin.site.register(Review)
admin.site.register(FavoriteProduct)
