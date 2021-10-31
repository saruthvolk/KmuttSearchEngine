"""
Definition of models.
"""

from django.db import models
import datetime

# Create your models here.

now = datetime.datetime.now().replace(microsecond=0)

class questionanswer (models.Model):
    id = models.AutoField(primary_key=True)
    question = models.CharField(max_length = 1000)
    answer = models.CharField(max_length = 1000)
    question_en = models.CharField(max_length = 1000)
    answer_en = models.CharField(max_length = 1000)
    created_time = models.DateTimeField(default=now, editable=True)
    created_date = models.DateTimeField(default=now, editable=True)
    user_id = models.IntegerField()
    updated_date = models.DateTimeField(default=now, editable=True)
    updated_time = models.DateTimeField(default=now, editable=True)
    updated_by = models.CharField(max_length = 1000)
    status = models.BooleanField()
    view_count = models.IntegerField()
    department_id = models.IntegerField()

    class Meta:
        db_table="questionanswer"
        ordering = ('id',)

class edit_questionanswer (models.Model):

    id = models.AutoField(primary_key=True)
    question = models.CharField(max_length = 1000)
    answer = models.CharField(max_length = 1000)
    question_en = models.CharField(max_length = 1000)
    answer_en = models.CharField(max_length = 1000)
    updated_date = models.DateTimeField(default=now, editable=True)
    updated_time = models.DateTimeField(default=now, editable=True)

    class Meta:
        db_table="questionanswer"
        managed = False
        ordering = ('id',)