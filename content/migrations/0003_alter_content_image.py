# Generated by Django 3.2.6 on 2021-10-07 07:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0002_alter_content_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='content',
            name='image',
            field=models.ImageField(blank=True, default='uploads/images/indir.jpg', upload_to='images/'),
        ),
    ]
