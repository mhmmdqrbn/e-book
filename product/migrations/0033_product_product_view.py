# Generated by Django 3.2.6 on 2021-10-07 07:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0032_rename_newprice_product_oldprice'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='product_view',
            field=models.PositiveIntegerField(blank=True, default=0, null=True),
        ),
    ]
