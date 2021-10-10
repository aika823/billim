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

class Seller(models.Model):
    name            = models.CharField(max_length=256, verbose_name='상품명')
    user_id         = models.ForeignKey(to='user.User',db_column='user_id', on_delete=models.RESTRICT)
    address         = models.TextField(verbose_name='주소')
    address_detail  = models.TextField(verbose_name='상세주소')
    phone_number    = models.TextField(verbose_name='전화번호')
    mobile_number   = models.TextField(verbose_name='휴대전화 번호')
    image           = models.ImageField(upload_to=PathAndRename("seller/"),blank=True, null=True)    

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'seller'
        verbose_name = '상품'
        verbose_name_plural = '상품입니다'