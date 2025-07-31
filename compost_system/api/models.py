from django.db import models
from django.utils import timezone


class Log(models.Model):
    userid = models.IntegerField(blank=True, null=True, db_comment='操作者')
    tables = models.CharField(max_length=255, blank=True, null=True, db_comment='操作表')
    action = models.CharField(max_length=255, blank=True, null=True, db_comment='动作')
    datas = models.TextField(blank=True, null=True, db_comment='操作数据')
    createtime = models.DateTimeField(default=timezone.now, db_comment='操作时间')

    class Meta:
        managed = False
        db_table = 'log'


class User(models.Model):
    username = models.CharField(max_length=255, blank=True, null=True, db_comment='用户名')
    phone = models.CharField(max_length=255, blank=True, null=True, db_comment='电话号码')
    email = models.CharField(max_length=255, blank=True, null=True, db_comment='邮箱')
    avatar = models.CharField(max_length=255, blank=True, null=True, db_comment='头像')
    name = models.CharField(max_length=255, blank=True, null=True, db_comment='姓名')
    password = models.CharField(max_length=255, blank=True, null=True, db_comment='密码')
    role = models.CharField(max_length=255, blank=True, null=True, db_comment='角色')
    gender = models.CharField(max_length=255, blank=True, null=True, db_comment='性别')
    createtime = models.DateTimeField(default=timezone.now, db_comment='创建时间')

    class Meta:
        managed = False
        db_table = 'user'


class Record(models.Model):
    userid = models.IntegerField(blank=True, null=True, db_comment='检测用户')
    imageurl = models.CharField(max_length=255, blank=True, null=True, db_comment='图片')
    result = models.IntegerField(blank=True, null=True, db_comment='检测结果')
    confidence = models.FloatField(blank=True, null=True, db_comment='置信度')
    timeconsuming = models.IntegerField(blank=True, null=True, db_comment='耗时')
    createtime = models.DateTimeField(default=timezone.now, db_comment='检测时间')

    class Meta:
        managed = False
        db_table = 'record'
