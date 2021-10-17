"""
Definition of models.
"""

from django.db import models

# Create your models here.
class questionanswer (models.Model):
    question = models.CharField(max_length = 1000)
    answer = models.CharField(max_length = 1000)
    class Meta:
        db_table="questionanswer"
