# Generated by Django 3.2 on 2021-05-07 17:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0005_totalorder'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='total_price',
            field=models.FloatField(default=0),
        ),
    ]
