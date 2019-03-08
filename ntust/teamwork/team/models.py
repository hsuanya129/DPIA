# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django_mysql.models import Bit1BooleanField

class User(models.Model):
    user_id = models.AutoField(primary_key=True) #用戶id
    account = models.CharField(max_length=20) #用戶帳號
    password = models.CharField(max_length=20) #用戶密碼
    permission_level = models.IntegerField() #用戶權限等級
    name = models.CharField(max_length=20) #用戶姓名
    activity_id = models.IntegerField() #用戶參與之專案id

    class Meta:
        db_table = 'user'

class Activity(models.Model): #pia專案簡介表
    activity_id = models.AutoField(primary_key=True) #pia專案id,pk
    name = models.CharField(max_length=60) #pia專案名字
    pia_manager_name = models.CharField(max_length=20) #pia專案負責人姓名
    pia_manager_email = models.CharField(max_length=35) #pia專案負責人email
    activity_manager_name = models.CharField(max_length=20) #系統負責人姓名
    activity_manager_email = models.CharField(max_length=35) #系統負責人email
    date = models.DateTimeField() #pia專案日期
    description = models.CharField(max_length=512) #pia專案簡短描述

    class Meta:
        db_table = 'activity'


class Questionary1Answer(models.Model): #問卷第一大題答案表
    answer_id = models.AutoField(primary_key=True) #個別答案id
    questionary_id = models.IntegerField() #問卷id,對應至問卷第一大題題目表第n小題
    questionary_ans = models.CharField(max_length=512) #答案內容
    activity_id = models.CharField(max_length=512) #專案id

    class Meta:
        db_table = 'questionary1_answer'


class Questionary1Template(models.Model):
    questionary_id = models.IntegerField(primary_key=True)
    questionary_description = models.CharField(max_length=512)

    class Meta:
        db_table = 'questionary1_template'


class Questionary2Answer(models.Model):
    questionary_id = models.IntegerField()
    answer_id = models.AutoField(primary_key=True)
    questionary_ans = models.CharField(max_length=512)
    activity_id = models.CharField(max_length=512)

    class Meta:
        db_table = 'questionary2_answer'


class Questionary2Template(models.Model):
    questionary_id = models.IntegerField(primary_key=True)
    questionary_description = models.CharField(max_length=512)

    class Meta:
        db_table = 'questionary2_template'


class Questionary3Answer(models.Model):
    answer_id = models.AutoField(primary_key=True)
    questionary_id = models.IntegerField()
    questionary_ans = models.CharField(max_length=512)
    activity_id = models.CharField(max_length=512)

    class Meta:
        db_table = 'questionary3_answer'


class Questionary3Template(models.Model):
    questionary_id = models.IntegerField(primary_key=True)
    questionary_description = models.CharField(max_length=512)

    class Meta:
        db_table = 'questionary3_template'


class Questionary4Answer(models.Model):
    answer_id = models.AutoField(primary_key=True)
    questionary_id = models.IntegerField()
    questionary_ans = models.CharField(max_length=512)
    activity_id = models.CharField(max_length=512)

    class Meta:
        db_table = 'questionary4_answer'


class Questionary4Template(models.Model):
    questionary_id = models.IntegerField(primary_key=True)
    questionary_description = models.CharField(max_length=512)

    class Meta:
        db_table = 'questionary4_template'


