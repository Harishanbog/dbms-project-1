# Generated by Django 3.2 on 2021-05-16 13:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0009_alter_order_total_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='items',
            name='category',
            field=models.CharField(blank=True, choices=[('Cashew', 'Cashew'), ('Grapes', 'Grapes'), ('Icecream', 'Icecream')], max_length=10),
        ),
        migrations.AddField(
            model_name='items',
            name='description',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
    ]
