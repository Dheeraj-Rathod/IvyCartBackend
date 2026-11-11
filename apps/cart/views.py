from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

# from apps.cart.models import Cart, CartItem
from apps.cart.serializers import AddToCartSerializer, CartItemsSerializer
from apps.cart.services import add_product_to_cart, get_user_cart, delete_cart_item

class AddToCartAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        # Step 1: Validate incoming request data
        serializer = AddToCartSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Step 2: Get validated product and quantity
        product = serializer.validated_data["product"]
        quantity = serializer.validated_data["quantity"]

        # Step 3: Add product to user's cart
        cart_item = add_product_to_cart(
            user=request.user,
            product=product,
            quantity=quantity
        )

        # Step 4: Prepare response
        response_serializer = AddToCartSerializer(cart_item)

        return Response(
            {
                "message": "Product added to cart successfully.",
                "cart_item": response_serializer.data
            },
            status=status.HTTP_201_CREATED
        )
class GetCartItems(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        cart = get_user_cart(request.user)
        cart_items = cart.items.all()
        serializer = CartItemsSerializer(cart_items, many=True)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

class DeleteCartItemAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def delete(self, request, item_id):

        deleted = delete_cart_item(
            user=request.user,
            item_id=item_id
        )

        if not deleted:
            return Response(
                {"message": "Cart item not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        return Response(
            {"message": "Cart item deleted successfully."},
            status=status.HTTP_200_OK
        )
    