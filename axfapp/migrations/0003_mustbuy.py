# Generated by Django 2.0.6 on 2018-07-03 15:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('axfapp', '0002_nav'),
    ]

    operations = [
        migrations.CreateModel(
            name='Mustbuy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.CharField(max_length=150)),
                ('name', models.CharField(max_length=20)),
                ('trackid', models.CharField(max_length=20)),
            ],
        ),
    ]