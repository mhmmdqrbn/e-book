# Generated by Django 3.2.6 on 2021-09-30 12:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0028_alter_product_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, default='uploads/images/indir.jpg', upload_to='images'),
        ),
    ]
