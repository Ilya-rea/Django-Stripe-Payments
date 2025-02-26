from django.urls import path
from .views import item_detail, create_checkout_session, create_order, buy_order

urlpatterns = [
    path('item/<int:item_id>/', item_detail, name='item_detail'),
    path('buy/<int:item_id>/', create_checkout_session, name='buy_item'),
    path("create_order/", create_order, name="create_order"),
    path("buy/order/<int:order_id>/", buy_order, name="buy_order"),
]

