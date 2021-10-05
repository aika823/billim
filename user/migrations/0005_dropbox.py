# Generated by Django 3.2.7 on 2021-10-04 08:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_user_profile_img'),
    ]

    operations = [
        migrations.CreateModel(
            name='DropBox',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30)),
                ('document', models.FileField(max_length=30, upload_to='')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'Drop Boxes',
            },
        ),
    ]
