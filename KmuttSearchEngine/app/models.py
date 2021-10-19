"""
Definition of models.
"""

from django.db import models

# Create your models here.

class questionanswer (models.Model):

    question = models.CharField(max_length = 1000)
    answer = models.CharField(max_length = 1000)
    question_en = models.CharField(max_length = 1000)
    answer_en = models.CharField(max_length = 1000)
    created_time = models.TimeField()
    created_date = models.DateField()
    user_id = models.IntegerField()
    updated_date = models.DateField()
    updated_time = models.TimeField()
    status = models.BooleanField()
    view_count = models.IntegerField()

    class Meta:
        db_table="questionanswer"
