from django.contrib import admin
from .models import(
    Product, Size, Color, ProductColor, ProductSize, ProductMedia,
    Category, Tag, CategoryTag, ProductCategory, Sale, Review, FavoriteProduct, CategoryMedia
)


# Admin configuration for the Product model
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'user')
    search_fields = ('title', 'price')


# Admin configuration for the Size model
class SizeAdmin(admin.ModelAdmin):
    list_display = ('name', )
    search_fields = ('name', )
    list_filter = ('name', )


# Admin configuration for the Color model
class ColorAdmin(admin.ModelAdmin):
    list_display = ('name', 'color_code')
    search_fields = ('name', 'color_code')


# Admin configuration for the ProductMedia model
class ProductMediaAdmin(admin.ModelAdmin):
    list_display = ('media_type', 'alt_text', 'is_main')
    search_fields = ('media_type', 'alt_text')
    list_filter = ('is_main',)


# Admin configuration for the Category model
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')
    search_fields = ('title', 'description', 'slug')


# Admin configuration for the ProductMedia model
class CategoryMediaAdmin(admin.ModelAdmin):
    list_display = ('media_type', 'alt_text', 'is_main')
    search_fields = ('media_type', 'alt_text')
    list_filter = ('is_main',)


# Admin configuration for the Tag model
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


# Admin configuration for the Sale model
class SaleAdmin(admin.ModelAdmin):
    list_display = ('product', 'discount_percent', 'start_date', 'end_date')
    search_fields = ('discount_percent', 'start_date', 'end_date')
    list_filter = ('end_date',)


# Admin configuration for the Review model
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'comment', 'parent')


# Register models with the admin site
admin.site.register(Product, ProductAdmin)
admin.site.register(Size, SizeAdmin)
admin.site.register(Color, ColorAdmin)
admin.site.register(ProductColor)
admin.site.register(ProductSize)
admin.site.register(ProductMedia, ProductMediaAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(CategoryTag)
admin.site.register(CategoryMedia, CategoryMediaAdmin)
admin.site.register(ProductCategory)
admin.site.register(Sale, SaleAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(FavoriteProduct)
