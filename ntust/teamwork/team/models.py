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
    description = models.TextField()
    date = models.DateTimeField()

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

class Pii(models.Model):
    name = models.TextField()
    activity = models.ForeignKey(Activity, models.DO_NOTHING)
    value = models.IntegerField()

    def __str__(self):
        return str(self.activity_id)+","+self.name

    class Meta:
        db_table = 'pii'


class Process(models.Model):
    name = models.TextField()
    activity = models.ForeignKey(Activity, models.DO_NOTHING)

    def __str__(self):
        return str(self.activity_id)+","+self.name

    class Meta:
        db_table = 'process'

class Participant(models.Model):
    name = models.TextField(blank=True, null=True)
    activity = models.ForeignKey(Activity, models.DO_NOTHING)

    def __str__(self):
        return str(self.activity_id)+","+self.name

    class Meta:
        db_table = 'participant'        

class System(models.Model):
    name = models.TextField(blank=True, null=True)
    activity = models.ForeignKey(Activity, models.DO_NOTHING)

    def __str__(self):
        return str(self.activity_id)+","+self.name

    class Meta:
        db_table = 'system'


class Evaluation(models.Model):
    activity = models.ForeignKey(Activity, models.DO_NOTHING)
    process = models.ForeignKey(Process, models.DO_NOTHING)
    pii = models.ForeignKey(Pii, models.DO_NOTHING)
    participant = models.ForeignKey(Participant, models.DO_NOTHING)
    system = models.ForeignKey(System, models.DO_NOTHING)
    value = models.IntegerField(blank=True, null=True)
    applicable = models.BooleanField(default=0)


    def __str__(self):
        return self.id

    class Meta:
        db_table = 'evaluation'

class EvaluationItem(models.Model):
    probability = models.IntegerField(blank=True, null=True)
    risk = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    evaluation = models.ForeignKey(Evaluation, models.DO_NOTHING)

    def __str__(self):
        return self.id

    class Meta:
        db_table = 'evaluation_item'

class ProcessHasParticipant(models.Model):
    process = models.ForeignKey(Process, models.DO_NOTHING)
    participant = models.ForeignKey(Participant, models.DO_NOTHING)

    class Meta:
        db_table = 'process_has_participant'
        unique_together = (('process', 'participant'),)


class ProcessHasPii(models.Model):
    process = models.ForeignKey(Process, models.DO_NOTHING)
    pii = models.ForeignKey(Pii, models.DO_NOTHING)

    class Meta:
        db_table = 'process_has_pii'
        unique_together = (('process', 'pii'),)




class ProcessHasSystem(models.Model):
    process = models.ForeignKey(Process, models.DO_NOTHING)
    system = models.ForeignKey(System, models.DO_NOTHING)

    class Meta:
        db_table = 'process_has_system'
        unique_together = (('process', 'system'),)


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

class Stakeholder(models.Model):
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


class Swimlane(models.Model):
    swimlane_json = JSONField(blank=True, null=True) 
    activity = models.ForeignKey(Activity, models.DO_NOTHING)

    def __str__(self):
        return "activity id:"+str(self.activity)

    class Meta:
        db_table = 'swimlane'



class User(models.Model):
    account = models.TextField()
    password = models.TextField()
    name = models.TextField()
    permission_level = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.account


    class Meta:
        db_table = 'user'


class UserHasActivity(models.Model):
    user = models.ForeignKey(User, models.DO_NOTHING)
    activity = models.ForeignKey(Activity, models.DO_NOTHING)

    def __str__(self):
        return str(self.user_id)+","+str(self.activity_id)

    class Meta:
        db_table = 'user_has_activity'
        unique_together = (('user', 'activity'),)
