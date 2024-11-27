from django.db import models
from django.conf import settings
from django.utils import timezone

class Shop(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='shops',
        on_delete=models.CASCADE,
        verbose_name='Pemilik Toko'
    )
    shop_name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)  # Deskripsi toko
    is_active = models.BooleanField(default=True)  # Status aktif/inaktif
    created_at = models.DateTimeField(default=timezone.now)  # Waktu pembuatan
    updated_at = models.DateTimeField(auto_now=True)  # Waktu pembaruan

    def __str__(self):
        return self.shop_name
