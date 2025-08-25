from django.shortcuts import render, get_object_or_404, redirect
from django.db.models.functions import Concat
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Prefetch, Count, F, Subquery, OuterRef, Value, CharField
from decimal import Decimal
from .models import Invoice, OrderItem, PaymentLog, ProductVariant
from products.models import ProductMedia, ProductColor, ProductSize, Product
from etc.choices import INVOICE_STATUS
from django.conf import settings



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
    if request.method=='POST':
        order_id = {order.product.product.id: order.id for order in orders if order.product.product.id==int(request.POST['order_item_id'])}
        try:
            order = get_object_or_404(OrderItem, id=order_id[int(request.POST['order_item_id'])])
            get_object_or_404(ProductVariant, id=order.product.id).delete()
            order.delete()
            messages.success(request,"Item removed from cart successfully!")
            # Redirect to avoid re-submission (PRG)
            return redirect('orderhub-main-url:products-cart-url')
        except:
            messages.error(request,"something went wrong please contact to support if you face any problem")
            # Redirect to avoid re-submission (PRG)
            return redirect('orderhub-main-url:products-cart-url')
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
        return redirect('products-main-url:product-details-url', pk=product.id)


    messages.error(request,"something went wrong")
    # Redirect to avoid re-submission (PRG)
    return redirect('products-main-url:product-details-url', pk=product.id)


@login_required
def all_invoice_view(request):
    invoices = (
        Invoice.objects
        .filter(user=request.user)
        .annotate(order_count=Count('order_items')) 
        .only(
            'id', 'total_price', 'status', 'created_at'
        ).order_by('-created_at')[:5]
    )
    
    context = {
        "page_title": 'My Orders',
        "invoices": invoices,

    }
    return render(request, 'orders.html', context)


@login_required
def invoice_details_view(request):
    invoice_id = int(request.POST.get('invoice_id'))

    # Subquery for main image
    main_image_sq = ProductMedia.objects.filter(
        product=OuterRef('product__product'),
        is_main=True
    ).values('file_url')[:1]

    invoice_items = (
        OrderItem.objects
        .filter(invoice__id=invoice_id, invoice__user=request.user)
        .select_related(
            'invoice',
            'product__product',
            'product__color__color__name',
            'product__size__size__name',
        )
        .annotate(
            inv_id=F("invoice__id"),
            invoice_status=F("invoice__status"),
            invoice_created_at=F("invoice__created_at"),
            product_title=F("product__product__title"),
            roduct_fk_id=F("product_id"),
            product_real_id=F("product__product__id"),        
            product_price=F("product__product__price"),
            size_name=F("product__size__size__name"),
            color_name=F("product__color__color__name"), 
            main_image=Concat(
            Value(settings.MEDIA_URL),
            Subquery(main_image_sq),
            output_field=CharField()

        ),        )
        .values(
            "inv_id", "invoice_status", "invoice_created_at",
            "id", "quantity", "total_price", "product_real_id",
            "product_title", "product_price",
            "color_name", "size_name",
            "main_image"
        )
        .order_by("-invoice_created_at", "-inv_id", "-id")
    )

    context = {
        "page_title": f"Order #{invoice_id}",
        "invoice_id": invoice_id,
        "invoice_items": invoice_items,
    }
    return render(request, "invoices_details.html", context)
