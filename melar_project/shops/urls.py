from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'shops', views.ShopViewSet)  # 'shops' adalah bagian dari URL

urlpatterns = [
    path('', include(router.urls)),  # URL dasar untuk mengakses router
]
