from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from django_filters import rest_framework as filters

from api.filters import ProductFilter
from api.models import Product, Category
from api.serializers import ProductSerializer, CategorySerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter(deleted=False, )
    serializer_class = ProductSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ProductFilter

    def perform_destroy(self, product):
        product.deleted = True
        product.save()


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def perform_destroy(self, category):
        if category.product_set.all():
            raise ValidationError(
                "Нельзя удалить категории к которой привязаны товары")
        super().perform_destroy(category)
