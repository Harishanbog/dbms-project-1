# Generated by Django 3.2 on 2021-06-05 15:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0013_alter_userotp_otp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userotp',
            name='otp',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]