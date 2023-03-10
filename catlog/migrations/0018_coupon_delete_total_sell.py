# Generated by Django 4.1.4 on 2023-01-10 03:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catlog', '0017_order_slug'),
    ]

    operations = [
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=20)),
                ('description', models.CharField(max_length=255)),
                ('discount', models.DecimalField(decimal_places=2, max_digits=5)),
                ('min_purchase', models.DecimalField(blank=True, decimal_places=2, max_digits=9, null=True)),
                ('expires', models.DateField(blank=True, null=True)),
            ],
        ),
        migrations.DeleteModel(
            name='Total_sell',
        ),
    ]
