# Generated by Django 5.1.2 on 2024-12-09 04:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("seller_requests", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="sellerrequest",
            name="status",
            field=models.CharField(
                choices=[
                    ("pending", "Pending"),
                    ("approved", "Approved"),
                    ("rejected", "Rejected"),
                ],
                default="pending",
                max_length=10,
            ),
        ),
    ]
