# Generated by Django 3.2.7 on 2021-10-07 09:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('product', '0001_initial'),
        ('user', '0003_alter_user_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(verbose_name='수량')),
                ('status', models.CharField(choices=[('대기중', '대기중'), ('결제대기', '결제대기중'), ('결제완료', '결제완료'), ('환불', '환불')], default='대기중', max_length=32, verbose_name='상태')),
                ('memo', models.TextField(blank=True, null=True, verbose_name='메모')),
                ('register_date', models.DateTimeField(auto_now_add=True, verbose_name='등록날짜')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.product', verbose_name='상품')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.user', verbose_name='사용자')),
            ],
            options={
                'verbose_name': '주문',
                'verbose_name_plural': '주문',
                'db_table': 'order',
            },
        ),
    ]
