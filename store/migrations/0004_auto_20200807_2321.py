# Generated by Django 3.0.7 on 2020-08-07 17:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_selleraccount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='selleraccount',
            name='sellerId',
            field=models.CharField(blank=True, max_length=15),
        ),
    ]
