# Generated by Django 5.0.6 on 2024-06-28 08:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_remove_cartitem_product_id_cartitem_product_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('product_name', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('category', models.CharField(max_length=255, null=True)),
                ('price', models.FloatField(default=0)),
            ],
        ),
        migrations.RemoveField(
            model_name='cartitem',
            name='product_name',
        ),
        migrations.AddField(
            model_name='cart',
            name='priceTotal',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='cartitem',
            name='product_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.product'),
        ),
    ]
