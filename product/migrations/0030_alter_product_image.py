# Generated by Django 3.2.6 on 2021-09-30 12:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0029_alter_product_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, default='uploads/images/indir.jpg', null=True, upload_to='images/'),
        ),
    ]
