from django.shortcuts import render
from products.models import Sale, Product, ProductMedia
from django.utils import timezone
from django.db.models import Prefetch
from django.core.paginator import Paginator


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

    context = {
        'products': queryset,
        'sale': last_sale_product,
        'sale_media': last_sale_product.productmedia_set.all().first(),
        "page_title": 'Home',
    }
    print(product_media_qs.all())
    return render(request, 'index.html', context)


def shop_products_view(request, *args, **kwargs):
    product_media_qs = ProductMedia.objects.only(
        'id', 'product_id' ,'file_url','alt_text'
    ).filter(is_main=True, media_type='image')

    products_queryset = Product.objects.only(
        'id', 'title', 'price', 'description'
    ).prefetch_related(
        Prefetch('productmedia_set', queryset=product_media_qs)
    ).order_by('-created_at')

    paginator = Paginator(products_queryset, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        "page_title": "Shop",
        'products': page_obj,
    }
    return render(request, 'shop.html', context)
