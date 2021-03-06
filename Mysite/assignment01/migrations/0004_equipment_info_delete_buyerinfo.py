# Generated by Django 4.0.4 on 2022-05-09 05:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assignment01', '0003_alter_admin_password_alter_admin_username_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='equipment_info',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='名称')),
                ('specification', models.CharField(max_length=64, verbose_name='规格')),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='单价')),
                ('date', models.DateTimeField(verbose_name='日期')),
                ('Manufacturer', models.CharField(max_length=32, verbose_name='生产厂家')),
                ('buyer', models.CharField(max_length=32, verbose_name='购买人')),
                ('state', models.SmallIntegerField(choices=[(1, '完好'), (2, '待修理'), (3, '报废')], verbose_name='状态')),
            ],
        ),
        migrations.DeleteModel(
            name='buyerinfo',
        ),
    ]
