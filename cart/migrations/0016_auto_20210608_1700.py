# Generated by Django 3.2.4 on 2021-06-08 11:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0015_auto_20210607_1439'),
    ]

    operations = [
        migrations.AddField(
            model_name='items',
            name='weight',
            field=models.CharField(choices=[('kg', 'Kg'), ('500gm', '500gm'), ('250gm', '250gm')], default='kg', max_length=100),
        ),
        migrations.AddField(
            model_name='order',
            name='bankingname',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='delivered',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='order',
            name='paymentoption',
            field=models.CharField(default='COD', max_length=100),
        ),
        migrations.AlterField(
            model_name='userotp',
            name='phonenumber',
            field=models.BigIntegerField(blank=True, null=True),
        ),
    ]
