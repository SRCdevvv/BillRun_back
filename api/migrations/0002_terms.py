# Generated by Django 3.1.7 on 2021-06-07 16:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Terms',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service', models.DateTimeField(default=None, null=True)),
                ('privacy', models.DateTimeField(default=None, null=True)),
                ('location', models.DateTimeField(default=None, null=True)),
                ('marketing', models.DateTimeField(blank=True, default=None, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='api.billrunuser')),
            ],
        ),
    ]
