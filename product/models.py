from django.db import models
import datetime
import os



def path_and_rename(path):
    def wrapper(instance, filename):
        ext = filename.split('.')[-1]
        print("###################################")
        print(ext)
        print(instance.pk)
        if instance.pk:
            filename = '{}.{}'.format(instance.pk, ext)
        else:
            now = datetime.datetime.now()
            date_time = now.strftime("%y%m%d_%H%M%S")
            filename = 'img_user_'+str(date_time)+str(ext)
        return os.path.join(path, filename)
    return wrapper

class Product(models.Model):
    name = models.CharField(max_length=256, verbose_name='상품명')
    price = models.IntegerField(verbose_name='상품가격')
    description = models.TextField(verbose_name='상품설명')
    stock = models.IntegerField(verbose_name='재고')
    register_date = models.DateTimeField(auto_now_add=True, verbose_name='등록날짜')
    image = models.ImageField(upload_to=path_and_rename('product/'),blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'product'
        verbose_name = '상품'
        verbose_name_plural = '상품'