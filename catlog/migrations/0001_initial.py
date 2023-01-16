# Generated by Django 4.1.4 on 2023-01-05 05:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('slug', models.SlugField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('invoice_no', models.CharField(max_length=20)),
                ('invoice_date', models.DateField()),
                ('invoice_amount', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ('customer_name', models.CharField(max_length=225)),
                ('customer_email', models.EmailField(max_length=225)),
                ('customer_phone', models.CharField(blank=True, max_length=20, null=True)),
                ('customer_address', models.CharField(blank=True, max_length=225, null=True)),
                ('products', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Userprofile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userprofile', models.ImageField(default='userprofile/avator.png', upload_to='userprofile/')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(max_length=255)),
                ('title', models.CharField(max_length=120)),
                ('product_code_number', models.IntegerField()),
                ('description', models.TextField(blank=True, null=True)),
                ('is_public', models.BooleanField(default=True)),
                ('is_discountable', models.BooleanField(default=True)),
                ('first_images', models.ImageField(upload_to='')),
                ('second_images', models.ImageField(blank=True, null=True, upload_to='')),
                ('third_images', models.ImageField(blank=True, null=True, upload_to='')),
                ('forth_images', models.ImageField(blank=True, null=True, upload_to='')),
                ('posted_at', models.DateTimeField(auto_now_add=True)),
                ('price', models.BigIntegerField()),
                ('is_stock', models.BooleanField(default=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catlog.category')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_no', models.CharField(max_length=20)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=100)),
                ('place', models.CharField(max_length=100)),
                ('phone', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('paid', models.BooleanField(default=False)),
                ('zipcode', models.CharField(max_length=100)),
                ('payment_intent', models.CharField(max_length=255)),
                ('paid_amount', models.IntegerField(blank=True, null=True)),
                ('staus', models.CharField(choices=[('Ordered', 'Ordered'), ('Shipped', 'Shipped'), ('Delivered', 'Delivered')], default='Ordered', max_length=30)),
                ('price', models.IntegerField()),
                ('quantity', models.IntegerField(default=1)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='catlog.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]
