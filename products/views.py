from django.shortcuts import render
from products.models import Sale, Product, ProductMedia, ProductColor, ProductSize
from django.utils import timezone
from django.db.models import Prefetch
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404


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
        'sale_media': sale_media[0],
        "page_title": 'Home',
    }
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


def product_details_view(requst, *arg, **kwargs):
    product = get_object_or_404(Product, pk=kwargs['pk'])

    product_media_set = ProductMedia.objects.only(
        'id', 'file_url', 'alt_text'
    ).filter(product=product)

    # TODO: get color and size 

    context = {
        'product': product,
        'images': product_media_set, 
        'page_title': f'ditails of product {product.id}'
    }
    return render(requst, 'product_details.html', context)