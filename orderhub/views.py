from django.shortcuts import render


def add_to_card_view(request, *args, **kwargs):
    print(kwargs, request.POST)
    context = {
        'page_title': 'Add to card',
    }
    return render(request, 'cart.html', context)