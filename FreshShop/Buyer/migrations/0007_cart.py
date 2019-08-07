# Generated by Django 2.1.1 on 2019-08-05 12:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Buyer', '0006_orderdetail_goods_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('goods_name', models.CharField(max_length=32, verbose_name='商品名称')),
                ('goods_price', models.FloatField(verbose_name='商品价格')),
                ('goods_total', models.FloatField(verbose_name='商品总价')),
                ('goods_number', models.IntegerField(verbose_name='商品数量')),
                ('goods_picture', models.ImageField(upload_to='buyer/images', verbose_name='商品图片')),
                ('goods_id', models.IntegerField(verbose_name='商品id')),
                ('goods_store', models.IntegerField(verbose_name='商品商店id')),
                ('user_id', models.IntegerField(verbose_name='用户id')),
            ],
        ),
    ]
