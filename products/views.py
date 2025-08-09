from django.shortcuts import render
from products.models import Sale, Product, ProductMedia, Color, Size, Category, Review
from django.utils import timezone
from django.db.models import Prefetch
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from .filters import ProductFilter


# index page 
def home_page_view(request):
    product_media_qs = ProductMedia.objects.only(
        'id', 'product_id' ,'file_url','alt_text'
    ).filter(is_main=True, media_type='image')

    # Prefetch media for the latest 5 products
    queryset = Product.objects.prefetch_related(
        Prefetch('productmedia_set', queryset=product_media_qs)
    ).order_by('-created_at')[:5]

    last_sale = (
        Sale.objects.select_related('product')
        .filter(
            is_active=True,
            start_date__lte=timezone.now(),
            end_date__gte=timezone.now()
        )
        .order_by('-start_date')
        .first()
    )

    # Prefetch media for the sale product
    last_sale_product = None
    if last_sale:
        last_sale_product = Product.objects.prefetch_related(
            Prefetch('productmedia_set', queryset=product_media_qs)
        ).get(pk=last_sale.product.pk)
        sale_media = last_sale_product.productmedia_set.get(is_main=True),
    else:
        sale_media = None

    context = {
        'products': queryset,
        'sale': last_sale_product,
        'sale_media': sale_media[0] or None,
        "page_title": 'Home',
    }
    return render(request, 'index.html', context)


# View to retrieve and display all products in the shop
def shop_products_view(request, *args, **kwargs):
    # Prefetch only main product images (type: image) to reduce DB hits
    product_media_qs = ProductMedia.objects.only(
        'id', 'product_id' ,'file_url','alt_text'
    ).filter(is_main=True, media_type='image')

    # Retrieve products with limited fields and prefetch related media
    products_queryset = Product.objects.only(
        'id', 'title', 'price', 'description'
    ).prefetch_related( # depend on media queryset get product images
        Prefetch('productmedia_set', queryset=product_media_qs)
    ).order_by('-created_at')

    # filtered product depends on category if user pass it
    filtered_product = ProductFilter(request.GET, queryset=products_queryset)

    # Apply pagination for performance and UI usability
    paginator = Paginator(filtered_product.qs, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        "page_title": "Shop",
        'products': page_obj,
    }
    return render(request, 'shop.html', context)


# View to retrieve and display specific product in the shop
def product_details_view(request, *arg, **kwargs):
    # try to retrieve product object or rise 404 ERROR
    product = get_object_or_404(Product, pk=kwargs['pk'])
    next_product = Product.objects.only('id').filter(id__gt=product.id).order_by('id').first()
    previous_product = Product.objects.only('id').filter(id__lt=product.id).order_by('id').last()

    # try to retrieve product media objects with filter to avoid errors if not exists
    product_media_set = ProductMedia.objects.only(
        'id', 'file_url', 'alt_text'
    ).filter(product=product)

    # Colors directly from Color model (linked via ProductColor)
    product_colors = Color.objects.filter(productcolor__product=product)

    # Sizes directly from Size model (linked via ProductSize)
    product_sizes = Size.objects.filter(productsize__product=product)

    # Categories directly from Category model (linked via ProductCategory)
    product_categories = Category.objects.filter(productcategory__product=product)

    # Reviews directly from Review model
    product_reviews = Review.objects.select_related('user', 'user__profile').only(
        'id', 'comment', 'created_at',
        'user__first_name', 'user__last_name', 'user__username',
        'user__profile__image'
    ).filter(product=product)

    context = {
        'product': product,
        'images': product_media_set,
        'page_title': f'ditails of product {product.id}',
        'product_colors': product_colors,
        'product_sizes': product_sizes,
        'product_categories': product_categories,
        'product_reviews':product_reviews,
        'next_product': next_product,
        'previous_product': previous_product,
    }
    return render(request, 'product_details.html', context)


# View to retrieve and display all categories
def categories_view(request, *args):
    categories = Category.objects.all().only('id', 'title')
    context = {
        "page_title": "All Categories",
        "categories": categories,
    }
    return render(request, 'all_categories.html', context=context)
