# Generated by Django 3.1.7 on 2021-04-17 23:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0021_auto_20210416_1625'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='like_count',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
