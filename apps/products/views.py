from rest_framework.viewsets import ModelViewSet

from .models import Product
from .serializers import ProductSerializer
from apps.categories.permissions import IsAdminOrReadOnly


class ProductViewSet(ModelViewSet):

    queryset = Product.objects.select_related("category").all() #Query optimization for ex. to avaoid N+1 query
    serializer_class = ProductSerializer
    permission_classes = [IsAdminOrReadOnly]