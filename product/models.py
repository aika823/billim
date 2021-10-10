from django.db import models
import datetime
import os
from django.utils.deconstruct import deconstructible

@deconstructible
class PathAndRename(object):
    def __init__(self, sub_path):
        self.path = sub_path
    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        now = datetime.datetime.now()
        date_time = now.strftime("%y%m%d_%H%M%S")
        filename = 'img_product_'+str(date_time)+str(ext)
        return os.path.join(self.path, filename)

class Product(models.Model):
    seller_id       = models.ForeignKey(to='seller.Seller',db_column='seller_id', on_delete=models.RESTRICT)
    name            = models.CharField(max_length=256, verbose_name='상품명')
    price           = models.IntegerField(verbose_name='상품가격')
    description     = models.TextField(verbose_name='상품설명')
    stock           = models.IntegerField(verbose_name='재고')
    register_date   = models.DateTimeField(auto_now_add=True, verbose_name='등록날짜')
    image           = models.ImageField(upload_to=PathAndRename("product/"),blank=True, null=True)    

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'product'
        verbose_name = '상품'
        verbose_name_plural = '상품입니다'