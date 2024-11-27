# views.py

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Shop
from .serializers import ShopSerializer
from users.permissions import IsOwner

class ShopViewSet(viewsets.ModelViewSet):
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def perform_create(self, serializer):
        # Menetapkan pengguna saat ini sebagai pemilik toko
        serializer.save(user=self.request.user)
    
    def get_queryset(self):
        # Filter toko yang dimiliki oleh user saat ini
        return Shop.objects.filter(user=self.request.user)
