# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django_mysql.models import Bit1BooleanField
from django_mysql.models import JSONField

class Activity(models.Model):
    name = models.TextField()
    pia_manager_name = models.TextField()
    pia_manager_email = models.TextField()
    activity_manager_name = models.TextField()
    activity_manager_email = models.TextField()
    date = models.DateTimeField()
    description = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'activity'


class Answer(models.Model):
    question = models.ForeignKey('Question', models.DO_NOTHING)
    context = models.TextField()
    activity = models.ForeignKey(Activity, models.DO_NOTHING)

    def __str__(self):
        return self.id

    class Meta:
        db_table = 'answer'

class Asset(models.Model):
    id = models.IntegerField(primary_key=True)
    type = models.TextField()
    name = models.TextField()
    impact_level = models.IntegerField()
    risk = models.TextField()
    likelihood = models.IntegerField()
    activity = models.ForeignKey(Activity, models.DO_NOTHING)

    def __str__(self):
        return self.id+"/"+self.type+"/"+self.name


    class Meta:
        db_table = 'asset'


class Question(models.Model):
    description = models.TextField()
    inner_id = models.IntegerField()
    questionary_type = models.ForeignKey('QuestionaryType', models.DO_NOTHING)

    def __str__(self):
        return self.description

    class Meta:
        db_table = 'question'


class QuestionaryType(models.Model):
    name = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'questionary_type'

class Swimlane(models.Model):
    swimlane_json = JSONField(blank=True, null=True)  
    activity = models.ForeignKey(Activity, models.DO_NOTHING)

    def __str__(self):
        return "activity id:"+self.activity

    class Meta:
        db_table = 'swimlane'


class User(models.Model):
    account = models.TextField()
    password = models.TextField()
    permission_level = models.IntegerField()
    name = models.TextField()
    activity = models.ForeignKey(Activity, models.DO_NOTHING)

    def __str__(self):
        return self.account

    class Meta:
        db_table = 'user'

class Stakeholder(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.TextField()
    role = models.TextField()
    email = models.TextField()
    part = models.TextField()
    feedback = models.TextField()
    activity = models.ForeignKey(Activity, models.DO_NOTHING)

    def __str__(self):
        return self.id

    class Meta:
        db_table = 'stakeholder'
