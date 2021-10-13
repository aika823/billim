from django.db import models
import datetime
import os
from django.db.models.fields import DateField
from django.utils.deconstruct import deconstructible
from billim.functions import get_random

@deconstructible
class PathAndRename(object):
    def __init__(self, sub_path):
        self.path = sub_path
    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        now = datetime.datetime.now()
        date_time = now.strftime("%y%m%d_%H%M%S") # EX: 950823_231758
        filename = 'img_product_'+ str(date_time)+str(ext)
        filename = 'img_product_{}_{}.{}'.format(str(date_time), str(get_random(8)) , str(ext)) 
        return os.path.join(self.path, filename)

class Product(models.Model):
    seller_id       = models.ForeignKey(to='seller.Seller',db_column='seller_id', on_delete=models.RESTRICT, null=True)
    category_id     = models.ForeignKey(to='product.ProductCategory',db_column='category_id', on_delete=models.RESTRICT, null=True, default=None)
    name            = models.CharField(max_length=256, verbose_name='상품명')
    price           = models.IntegerField(verbose_name='상품가격')
    description     = models.TextField(verbose_name='상품설명')
    stock           = models.IntegerField(verbose_name='재고')
    register_date   = models.DateTimeField(auto_now_add=True, verbose_name='등록날짜')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'product'
        verbose_name = '상품'
        verbose_name_plural = '상품입니다'

class ProductImage(models.Model):
    product_id = models.ForeignKey(to='product.Product', db_column='product_id', on_delete=models.SET_NULL, null=True, default=None)
    image = models.ImageField(upload_to=PathAndRename("product/"),blank=True, null=True)
    thumbnail = models.BooleanField(null=True, default=None)
    order = int
    def __id__(self):
        return str(self.image)
    class Meta:
        db_table = 'product_image'

class Category(models.Model):
    category = models.CharField(max_length=16, null=True, default=None)
    def __id__(self):
        return self.id
    class Meta:
        db_table = 'category'

class Subcategory(models.Model):
    category_id = models.ForeignKey(to='product.Category', db_column='category_id', on_delete=models.SET_NULL, null=True, default=None)
    category = models.CharField(max_length=16, null=True, default=None)
    def __id__(self):
        return self.id
    class Meta:
        db_table = 'subcategory'

class ProductCategory(models.Model):
    category_id = models.ForeignKey(to='product.Category', db_column='category_id', on_delete=models.SET_NULL, null=True, default=None)
    subcategory_id = models.ForeignKey(to='product.Subcategory', db_column='subcategory_id', on_delete=models.SET_NULL, null=True, default=None)
    def __id__(self):
        return self.id
    class Meta:
        db_table = 'product_category'