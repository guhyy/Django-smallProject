# Generated by Django 4.0.4 on 2022-05-04 05:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assignment01', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='buyerinfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('phone', models.CharField(max_length=32)),
                ('address', models.CharField(max_length=64)),
            ],
        ),
    ]
