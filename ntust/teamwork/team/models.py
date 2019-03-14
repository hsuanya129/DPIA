# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django_mysql.models import Bit1BooleanField

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
    question_id = models.IntegerField()
    context = models.TextField()
    activity_id = models.IntegerField()

    def __str__(self):
        return self.id

    class Meta:
        db_table = 'answer'


class Question(models.Model):
    description = models.TextField()
    inner_id = models.IntegerField()
    questionary_type_id = models.IntegerField()

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


class User(models.Model):
    account = models.TextField()
    password = models.TextField()
    permission_level = models.IntegerField()
    name = models.TextField()
    activity_id = models.IntegerField()

    def __str__(self):
        return self.account

    class Meta:
        db_table = 'user'
