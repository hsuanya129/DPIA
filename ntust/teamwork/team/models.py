# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Activity(models.Model):
    activity_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=60)
    pia_manager_name = models.CharField(max_length=20)
    pia_manager_email = models.CharField(max_length=35)
    activity_manager_name = models.CharField(max_length=20)
    activity_manager_email = models.CharField(max_length=35)
    date = models.DateTimeField()
    description = models.CharField(max_length=512)

    class Meta:
        db_table = 'activity'


class Questionary1Answer(models.Model):
    questionary_id = models.IntegerField()
    questionary_ans = models.CharField(max_length=512)
    activity_id = models.CharField(max_length=512)

    class Meta:
        db_table = 'questionary1_answer'


class Questionary1Template(models.Model):
    questionary_id = models.IntegerField()
    questionary_description = models.CharField(max_length=512)

    class Meta:
        db_table = 'questionary1_template'


class Questionary2Answer(models.Model):
    questionary_id = models.IntegerField()
    questionary_ans = models.CharField(max_length=512)
    activity_id = models.CharField(max_length=512)

    class Meta:
        db_table = 'questionary2_answer'


class Questionary2Template(models.Model):
    questionary_id = models.IntegerField()
    questionary_description = models.CharField(max_length=512)

    class Meta:
        db_table = 'questionary2_template'


class Questionary3Answer(models.Model):
    questionary_id = models.IntegerField()
    questionary_ans = models.CharField(max_length=512)
    activity_id = models.CharField(max_length=512)

    class Meta:
        db_table = 'questionary3_answer'


class Questionary3Template(models.Model):
    questionary_id = models.IntegerField()
    questionary_description = models.CharField(max_length=512)

    class Meta:
        db_table = 'questionary3_template'


class Questionary4Answer(models.Model):
    questionary_id = models.IntegerField()
    questionary_ans = models.CharField(max_length=512)
    activity_id = models.CharField(max_length=512)

    class Meta:
        db_table = 'questionary4_answer'


class Questionary4Template(models.Model):
    questionary_id = models.IntegerField()
    questionary_description = models.CharField(max_length=512)

    class Meta:
        db_table = 'questionary4_template'


class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    account = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    permission_level = models.IntegerField()
    name = models.CharField(max_length=20)
    activity_id = models.IntegerField()

    class Meta:
        db_table = 'user'
