# Generated by Django 3.2.6 on 2021-09-22 11:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0018_alter_product_author'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='author',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
    ]