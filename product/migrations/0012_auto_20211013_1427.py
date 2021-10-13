# Generated by Django 3.2.7 on 2021-10-13 05:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0011_auto_20211013_1131'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(default=None, max_length=16, null=True)),
            ],
            options={
                'db_table': 'category',
            },
        ),
        migrations.CreateModel(
            name='Subcategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(default=None, max_length=16, null=True)),
                ('category_id', models.ForeignKey(db_column='category_id', default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='product.category')),
            ],
            options={
                'db_table': 'subcategory',
            },
        ),
        migrations.RemoveField(
            model_name='product',
            name='subcategory_id',
        ),
        migrations.RemoveField(
            model_name='productcategory',
            name='category',
        ),
        migrations.RemoveField(
            model_name='productcategory',
            name='product_id',
        ),
        migrations.AlterModelTable(
            name='productcategory',
            table=None,
        ),
        migrations.DeleteModel(
            name='ProductSubcategory',
        ),
        migrations.AddField(
            model_name='productcategory',
            name='category_id',
            field=models.ForeignKey(db_column='category_id', default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='product.category'),
        ),
        migrations.AddField(
            model_name='productcategory',
            name='subcategory_id',
            field=models.ForeignKey(db_column='subcategory_id', default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='product.subcategory'),
        ),
    ]