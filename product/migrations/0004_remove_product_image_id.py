# Generated by Django 3.2.7 on 2021-10-12 07:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_auto_20211012_1555'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='image_id',
        ),
    ]
