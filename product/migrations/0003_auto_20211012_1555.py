# Generated by Django 3.2.7 on 2021-10-12 06:55

from django.db import migrations, models
import django.db.models.deletion
import product.models


class Migration(migrations.Migration):

    dependencies = [
        ('seller', '0001_initial'),
        ('product', '0002_product_seller_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='image',
        ),
        migrations.AlterField(
            model_name='product',
            name='seller_id',
            field=models.ForeignKey(db_column='seller_id', null=True, on_delete=django.db.models.deletion.RESTRICT, to='seller.seller'),
        ),
        migrations.CreateModel(
            name='ProductSubcategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_id', models.ForeignKey(db_column='product_id', on_delete=django.db.models.deletion.RESTRICT, to='product.product')),
            ],
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to=product.models.PathAndRename('product/'))),
                ('product_id', models.ForeignKey(db_column='product_id', on_delete=django.db.models.deletion.RESTRICT, to='product.product')),
            ],
        ),
        migrations.CreateModel(
            name='ProductCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=16)),
                ('product_id', models.ForeignKey(db_column='product_id', on_delete=django.db.models.deletion.RESTRICT, to='product.product')),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='category_id',
            field=models.ForeignKey(db_column='category_id', null=True, on_delete=django.db.models.deletion.RESTRICT, to='product.productcategory'),
        ),
        migrations.AddField(
            model_name='product',
            name='image_id',
            field=models.ForeignKey(db_column='image_id', null=True, on_delete=django.db.models.deletion.RESTRICT, to='product.productimage'),
        ),
        migrations.AddField(
            model_name='product',
            name='subcategory_id',
            field=models.ForeignKey(db_column='subcategory_id', null=True, on_delete=django.db.models.deletion.RESTRICT, to='product.productsubcategory'),
        ),
    ]
