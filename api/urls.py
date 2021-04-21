from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router_v1 = DefaultRouter()
router_v1.register('products', views.ProductViewSet, basename='products')
router_v1.register('categories', views.CategoryViewSet, basename='categories')

urlpatterns = [
    path('v1/', include(router_v1.urls)),
]
