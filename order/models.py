from django.db import models

class Order(models.Model):
    user = models.ForeignKey('user.User', on_delete=models.CASCADE, verbose_name='사용자')
    product = models.ForeignKey('product.Product', on_delete=models.CASCADE, verbose_name='상품')
    quantity = models.IntegerField(verbose_name='수량')
    status = models.CharField(
        choices=(
            ('대기중', '대기중'),
            ('결제대기', '결제대기중'),
            ('결제완료', '결제완료'),
            ('환불', '환불'),
        ),
        default='대기중', max_length=32, verbose_name='상태'
    )
    memo = models.TextField(null=True, blank=True, verbose_name='메모')
    register_date = models.DateTimeField(auto_now_add=True, verbose_name='등록날짜')

    def __str__(self):
        return str(self.user) + ' ' + str(self.product)

    class Meta:
        db_table = 'order'
        verbose_name = '주문'
        verbose_name_plural = '주문'
