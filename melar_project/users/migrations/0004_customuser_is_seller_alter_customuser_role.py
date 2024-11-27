# Generated by Django 5.1.2 on 2024-10-29 23:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_customuser_is_active_customuser_is_staff'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='is_seller',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='role',
            field=models.CharField(blank=True, choices=[('admin', 'Admin')], max_length=50),
        ),
    ]