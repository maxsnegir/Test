from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from api.models import Product, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','name', ]


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(slug_field='name',
                                            queryset=Category.objects.all(),
                                            many=True, )

    def validate_category(self, category):
        if 2 > len(set(category)) or len(category) > 10:
            raise ValidationError(
                'У товара должно быть от 2х до 10 категорий')
        return category

    class Meta:
        model = Product
        fields = ['id', 'name', 'category', 'price', 'published']
