# Generated by Django 3.2.7 on 2021-10-10 04:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('seller', '0001_initial'),
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='seller_id',
            field=models.ForeignKey(db_column='seller_id', default=1, on_delete=django.db.models.deletion.RESTRICT, to='seller.seller'),
            preserve_default=False,
        ),
    ]
