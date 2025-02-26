import stripe
from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings
from django.http import JsonResponse
from .models import Item, Order

stripe.api_key = settings.STRIPE_SECRET_KEY


def create_order(request):
    item_ids = request.GET.getlist("items")
    if not item_ids:
        return JsonResponse({"error": "No items selected"}, status=400)

    items = Item.objects.filter(id__in=item_ids)
    if not items:
        return JsonResponse({"error": "Invalid items"}, status=400)

    order = Order.objects.create()
    order.items.set(items)

    return JsonResponse({"order_id": order.id, "total_price": order.total_price})


def item_detail(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    return render(request, 'payments/item.html', {
        'item': item,
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY
    })


def create_checkout_session(request, item_id):
    item = get_object_or_404(Item, id=item_id)

    if not item.stripe_product_id:
        stripe_product = stripe.Product.create(name=item.name)
        stripe_price = stripe.Price.create(
            unit_amount=int(item.price * 100),
            currency=item.currency,
            product=stripe_product.id
        )
        item.stripe_product_id = stripe_product.id
        item.save()

    checkout_session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': item.currency,
                'product': item.stripe_product_id,
                'unit_amount': int(item.price * 100),
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url="http://127.0.0.1:8000/success/",
        cancel_url="http://127.0.0.1:8000/cancel/",
    )
    return JsonResponse({'session_id': checkout_session.id})


def buy_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if order.paid:
        return JsonResponse({"error": "Order already paid"}, status=400)

    line_items = [
        {
            "price_data": {
                "currency": item.currency,
                "product_data": {"name": item.name},
                "unit_amount": int(item.price * 100),
            },
            "quantity": 1,
        }
        for item in order.items.all()
    ]

    discounts = []
    if order.discount and order.discount.stripe_coupon_id:
        discounts.append({"coupon": order.discount.stripe_coupon_id})

    tax_rates = []
    if order.tax and order.tax.stripe_tax_id:
        tax_rates.append(order.tax.stripe_tax_id)

    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[{
            **line_item,
            "tax_rates": tax_rates
        } for line_item in line_items],
        mode="payment",
        discounts=discounts,
        success_url="http://127.0.0.1:8000/success/",
        cancel_url="http://127.0.0.1:8000/cancel/",
    )

    return redirect(session.url)