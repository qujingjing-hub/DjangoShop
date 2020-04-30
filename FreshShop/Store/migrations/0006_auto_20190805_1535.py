# Generated by Django 2.1.1 on 2019-08-05 07:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Store', '0005_auto_20190725_1919'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='goods',
            name='store_id',
        ),
        migrations.AddField(
            model_name='goods',
            name='store_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='Store.Store', verbose_name='商品店铺'),
            preserve_default=False,
        ),
    ]