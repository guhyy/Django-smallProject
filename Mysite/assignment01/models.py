from django.db import models

# Create your models here.
class admin(models.Model):
    username = models.CharField(verbose_name='username', max_length=32)
    password = models.CharField(verbose_name='password',max_length=32)
    
    
    
class equipment_info(models.Model):
    name = models.CharField(verbose_name='名称',max_length=32)
    number = models.CharField(verbose_name='编号',max_length=32,default='')
    specification = models.CharField(verbose_name='规格',max_length=64)
    price = models.DecimalField(verbose_name='单价',max_digits=10,decimal_places=2,default=0)
    date = models.DateTimeField(verbose_name='日期')
    Manufacturer = models.CharField(verbose_name='生产厂家',max_length=32)
    buyer = models.CharField(verbose_name='购买人',max_length=32)
    
    state_choices = (
        (1,'完好'),
        (2,'待修理'),
        (3,'报废'),
    )
    state = models.SmallIntegerField(verbose_name='状态',choices=state_choices)
    
class Toberepaired(models.Model):
    number = models.CharField(verbose_name='编号',max_length=32,default='')
    date = models.DateTimeField(verbose_name='修理日期')
    manufacturer = models.CharField(verbose_name='修理厂家',max_length=32)
    price = models.DecimalField(verbose_name='修理单价',max_digits=10,decimal_places=2,default=0)
    responsible = models.CharField(verbose_name='责任人',max_length=32)