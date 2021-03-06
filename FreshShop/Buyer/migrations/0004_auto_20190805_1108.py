# Generated by Django 2.1.1 on 2019-08-05 03:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Buyer', '0003_order_orderdetail'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orderdetail',
            old_name='Goods_id',
            new_name='goods_id',
        ),
        migrations.RenameField(
            model_name='orderdetail',
            old_name='Goods_name',
            new_name='goods_name',
        ),
        migrations.RenameField(
            model_name='orderdetail',
            old_name='Goods_price',
            new_name='goods_price',
        ),
        migrations.RenameField(
            model_name='orderdetail',
            old_name='Goods_store',
            new_name='goods_store',
        ),
        migrations.RenameField(
            model_name='orderdetail',
            old_name='Goods_total',
            new_name='goods_total',
        ),
        migrations.RemoveField(
            model_name='orderdetail',
            name='Goods_number',
        ),
        migrations.AddField(
            model_name='orderdetail',
            name='goods_number',
            field=models.IntegerField(default=1, verbose_name='商品购买数量'),
            preserve_default=False,
        ),
    ]
