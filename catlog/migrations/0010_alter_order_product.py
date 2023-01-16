# Generated by Django 4.1.4 on 2023-01-06 00:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catlog', '0009_alter_order_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='product',
            field=models.OneToOneField(db_constraint=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='items', to='catlog.product'),
        ),
    ]
