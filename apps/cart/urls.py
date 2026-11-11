from .views import AddToCartAPIView, GetCartItems, DeleteCartItemAPIView
from django.urls import path

urlpatterns = [
    path('cart_items/', AddToCartAPIView.as_view(), name='add-to-cart-item'),
    path('cart/', GetCartItems.as_view(), name="get-cart-and-items"),
    path("cart/items/<int:item_id>/", DeleteCartItemAPIView.as_view(), name="delete-cart-item")
]
