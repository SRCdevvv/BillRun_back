# Generated by Django 3.1.7 on 2021-04-16 16:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0020_product_hits'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='hits',
            field=models.IntegerField(default=0),
        ),
    ]
