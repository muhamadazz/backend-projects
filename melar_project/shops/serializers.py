# serializers.py

from rest_framework import serializers
from .models import Shop

class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = ['id', 'user', 'shop_name', 'description', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['user', 'created_at', 'updated_at']  # 'user' hanya diisi otomatis dari request
