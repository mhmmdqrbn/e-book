# Generated by Django 3.2.6 on 2021-10-01 12:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0005_alter_orderproduct_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Yeni', 'Yeni'), ('Qəbul olundu', 'Qəbul olundu'), ('Yolda', 'Yolda'), ('Tamamlandı', 'Tamamlandı'), ('Ləğv olundu', 'Ləğv olundu')], default='Yeni', max_length=155),
        ),
    ]
