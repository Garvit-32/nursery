# Generated by Django 3.0.7 on 2020-08-09 06:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0009_auto_20200809_1122'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shippingaddress',
            name='email',
        ),
        migrations.RemoveField(
            model_name='shippingaddress',
            name='name',
        ),
        migrations.RemoveField(
            model_name='shippingaddress',
            name='phone',
        ),
        migrations.AddField(
            model_name='shippingaddress',
            name='customer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='store.Customer'),
        ),
    ]
