from apps.cart.models import Cart, CartItem
from rest_framework.response import Response
from rest_framework import status

def add_product_to_cart(user, product, quantity):
    cart, cart_created = Cart.objects.get_or_create(
    user=user
    )

    cart_item, cart_item_created = CartItem.objects.get_or_create(
        product=product,
        cart=cart,
        defaults={"quantity": quantity}
    )

    if not cart_item_created:
        cart_item.quantity += quantity
        cart_item.save()

    # Step 4: Return cart item
    return cart_item

def get_user_cart(user):
    cart = Cart.objects.filter(user=user).first()
    if cart is None:
        return Response(
            {"message": "Your cart is empty."},
            status=status.HTTP_200_OK
        )
    return cart

def delete_cart_item(user, item_id):

    cart_item = CartItem.objects.filter(
        id=item_id,
        cart__user=user
    ).first()

    if cart_item is None:
        return False

    cart_item.delete()

    return True