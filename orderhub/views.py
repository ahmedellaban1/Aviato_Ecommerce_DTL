from django.shortcuts import render
from .models import Invoice, OrderItem, PaymentLog, ProductVariant
from products.models import ProductMedia, ProductColor, ProductSize, Product
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from etc.choices import INVOICE_STATUS
from decimal import Decimal
from django.contrib import messages
from django.db.models import Prefetch


@login_required
def products_cart_view(request):
    product_media_qs = ProductMedia.objects.only(
        'id', 'product_id' ,'file_url','alt_text'
    ).filter(is_main=True, media_type='image')

    invoice = Invoice.objects.filter(
        user=request.user,
        status=INVOICE_STATUS[0][0]
    ).latest('created_at')
    
    orders = OrderItem.objects.only('id', 'product__product').filter(invoice=invoice)
    product_ids = tuple(orders.values_list('product__product', flat=True).distinct())
    product_qs = Product.objects.prefetch_related(
        Prefetch('productmedia_set', product_media_qs)
    ).filter(id__in=product_ids)
    context = {
        'page_title': "Your cart",
        'orders': product_qs,
    }
    return render(request, 'cart.html', context)


@login_required
def add_to_cart_view(request, *args, **kwargs):
    if request.method == 'POST':
        data = {key: int(request.POST[key]) for key in request.POST if key != 'csrfmiddlewaretoken'}
        
        product = get_object_or_404(Product, id=data['product_id'])
        product_color = get_object_or_404(ProductColor, id=data['color_id'])
        product_size = get_object_or_404(ProductSize, id=data['size_id'])

        invoice, created = Invoice.objects.get_or_create(
            user=request.user,
            status=INVOICE_STATUS[0][0],
            defaults={
                'status': INVOICE_STATUS[0][0],
                'total_price': 0,
                'shipping_fee': 0,
                'shipping_address': None,
                'paid_at': None,
                'updated_at': timezone.now(),
            }
        )

        product_variant = ProductVariant.objects.create(
            product=product,
            color=product_color,
            size=product_size,
        )

        total_price = product.price * data['quantity']

        OrderItem.objects.create(
            invoice=invoice,
            product=product_variant,
            quantity=data['quantity'],
            total_price=total_price,
        )

        invoice.total_price += total_price
        invoice.shipping_fee = invoice.total_price * Decimal(0.1)
        invoice.updated_at = timezone.now()
        invoice.save()
        
        # alert if product successfully added to the cart
        messages.success(request,"Item added to cart successfully!")
        # Redirect to avoid re-submission (PRG)
        return redirect('products-main-url:product-details-url', pk=product.id)  # replace with your cart or success page URL name


    messages.error(request,"something went wrong")
    # Redirect to avoid re-submission (PRG)
    return redirect('products-main-url:product-details-url', pk=product.id)  # replace with your cart or success page URL name
