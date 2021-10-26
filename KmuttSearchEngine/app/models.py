"""
Definition of models.
"""

from django.db import models
import datetime

# Create your models here.

now = datetime.datetime.now().replace(microsecond=0)

class questionanswer (models.Model):
    id = models.IntegerField(primary_key=True)
    question = models.CharField(max_length = 1000)
    answer = models.CharField(max_length = 1000)
    question_en = models.CharField(max_length = 1000)
    answer_en = models.CharField(max_length = 1000)
    created_time = models.DateTimeField(default=now, editable=False)
    created_date = models.DateTimeField(default=now, editable=False)
    user_id = models.IntegerField()
    updated_date = models.DateTimeField(default=now, editable=False)
    updated_time = models.DateTimeField(default=now, editable=False)
    updated_by = models.CharField(max_length = 1000)
    status = models.BooleanField()
    view_count = models.IntegerField()
    department_id = models.IntegerField()

    class Meta:
        db_table="questionanswer"

class edit_questionanswer (models.Model):

    id = models.IntegerField(primary_key=True)
    question = models.CharField(max_length = 1000)
    answer = models.CharField(max_length = 1000)
    question_en = models.CharField(max_length = 1000)
    answer_en = models.CharField(max_length = 1000)

    class Meta:
        db_table="questionanswer"
        managed = False