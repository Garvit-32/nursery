# Generated by Django 3.0.7 on 2020-08-10 21:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0022_auto_20200810_1726'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='SellerAccount',
        ),
        migrations.AddField(
            model_name='product',
            name='sellerId',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]
