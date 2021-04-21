from decimal import Decimal

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from api.models import Product, Category
from api.serializers import ProductSerializer


class ProductTest(APITestCase, ):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.c1 = Category.objects.create(name='Категория 1')
        cls.c2 = Category.objects.create(name='Категория 2')
        cls.c3 = Category.objects.create(name='Категория 3')
        cls.c = Category.objects.create(name='Категория без товаров')

        cls.product = Product.objects.create(name='Товар 1', price=123)

        cls.product.category.add(cls.c1)
        cls.product.category.add(cls.c2)
        cls.product.category.add(cls.c3)

    def test_get_products_list(self):
        """
        Проверка GET запроса к /products/
        """
        url = reverse('products-list')
        response = self.client.get(url, format='json')

        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_get_product_detail(self):
        """
        Проверка GET запроса к /products/<int:id>/
        """
        url = reverse('products-detail', kwargs={'pk': self.product.pk})
        response = self.client.get(url, format='json')
        serializer = ProductSerializer(self.product)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_product(self):
        """
        Проверка POST запроса к /products/ (создание товара)
        """
        current_products = Product.objects.all().count()
        url = reverse('products-list')
        data = {'name': 'Товар 2', 'price': '123', 'category': [self.c1.name,
                                                                self.c2.name,
                                                                self.c3.name]}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(current_products + 1, Product.objects.all().count())

    def test_edit_product(self):
        """
        Проверка редактировния товара
        """
        url = reverse('products-detail', kwargs={'pk': self.product.pk})

        data = {'name': 'Товар Измененный', 'price': '100',
                'category': [self.c1.name,
                             self.c2.name, ]}
        response = self.client.put(url, data, format='json')
        product = Product.objects.get(pk=self.product.pk)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(product.name,
                         response.data['name'])  # навзание изменилось
        self.assertEqual(product.price,
                         Decimal(response.data['price']))  # Цена изменилась
        self.assertEqual(product.category.count(),
                         len(response.data[
                                 'category']))  # Кол-во категорий изменились

    def test_delete_product(self):
        """
        Удаление товара
        """
        url = reverse('products-detail', kwargs={'pk': self.product.pk})
        response = self.client.delete(url, format='json')
        product = Product.objects.get(pk=self.product.pk)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertTrue(product.deleted, True)

    def test_product_categories_count(self):
        """
        Тест неправильного количества категорий у товара
        """
        url = reverse('products-list')
        data = {'name': 'Товар 2', 'price': '123',
                'category': [self.c1.name, ]}

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['category'][0],
                         'У товара должно быть от 2х до 10 категорий')

    def test_category_create(self):
        """
        Проверка создания категории
        """
        categories_count = Category.objects.count()
        url = reverse('categories-list')
        data = {'name': 'Категория 4'}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(categories_count + 1, Category.objects.count())

    def test_category_create_unique(self):
        """
        Проверка уникальности категории
        """
        categories_count = Category.objects.count()
        url = reverse('categories-list')
        data = {'name': 'Категория 3'}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertEqual(response.json()['name'][0],
                         'category with this Название категории already '
                         'exists.')
        self.assertEqual(categories_count, Category.objects.count())

    def test_delete_category_without_products(self):
        """
        Удаление категории без товаров
        """
        categories_count = Category.objects.count()

        url = reverse('categories-detail', kwargs={'pk': self.c.id})
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(categories_count - 1, Category.objects.count())

    def test_delete_category_with_products(self):
        """
        Удаление категории с товарами
        """
        url = reverse('categories-detail', kwargs={'pk': self.c1.id})
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()[0], 'Нельзя удалить категории '
                                             'к которой привязаны товары')

    def test_filter_products(self):
        """
        Тест фильтров
        """
        get_params = f'?name={self.product.name}&category_id={self.c1.id}' \
                     f'&price_min=120'
        url = reverse('products-list') + get_params
        response = self.client.get(url, format='json')

        products = Product.objects.filter(name=self.product.name,
                                          category__id=self.c1.id,
                                          price__gte=120)
        serializer = ProductSerializer(products, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
