# Generated by Django 3.2.6 on 2021-09-27 20:48

from django.db import migrations
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0021_alter_product_favorite'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='product',
            managers=[
                ('newmanager', django.db.models.manager.Manager()),
            ],
        ),
    ]
