# Generated by Django 3.1.7 on 2021-07-01 17:58

import api.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_auto_20210701_1755'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='photo1',
            field=models.ImageField(default='default/no_image.png', upload_to=api.models.Product.upload_photo),
        ),
    ]
