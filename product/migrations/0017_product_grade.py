# Generated by Django 3.2.7 on 2021-10-13 09:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0016_auto_20211013_1751'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='grade',
            field=models.IntegerField(default=None, null=True),
        ),
    ]
