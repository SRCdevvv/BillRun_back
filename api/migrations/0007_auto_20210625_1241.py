# Generated by Django 3.1.7 on 2021-06-25 12:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_auto_20210618_0127'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.CharField(choices=[('woman', '여성의류/잡화'), ('man', '남성의류/잡화'), ('digital', '디지털/가전'), ('majorBook', '전공도서'), ('majorEtc', '전공기타'), ('game', '게임'), ('sports', '스포츠'), ('household', '생활잡화'), ('etc', '기타')], max_length=10),
        ),
    ]
