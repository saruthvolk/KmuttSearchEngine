"""
Definition of models.
"""

from django.db import models
import datetime
from django.contrib.auth.models import User 
from django.contrib.auth.models import AbstractUser

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
    #question_sw = models.CharField(max_length = 1000)
    #question_tokenized = models.CharField(max_length = 1000)

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
    #question_sw = models.CharField(max_length = 1000)
    #question_tokenized = models.CharField(max_length = 1000)

    class Meta:
        db_table="questionanswer"
        managed = False
        ordering = ('id',)

class userinfo(models.Model):

    id = models.AutoField(primary_key=True,unique=True)
    username = models.CharField(max_length = 1000,unique=True)
    password = models.CharField(max_length = 1000)
    created_by = models.CharField(max_length = 1000)
    created_time = models.DateTimeField(default=now, editable=True)
    created_date = models.DateTimeField(default=now, editable=True)
    updated_by = models.CharField(max_length = 1000)
    updated_time = models.DateTimeField(default=now, editable=True)
    updated_date = models.DateTimeField(default=now, editable=True)
    deleted_by = models.CharField(max_length = 1000)
    deleted_date = models.DateTimeField(default=None, editable=True)
    deleted_time = models.DateTimeField(default=None, editable=True)
    status = models.BooleanField()
    first_name = models.CharField(max_length = 1000)
    last_name = models.CharField(max_length = 1000)
    email = models.CharField(max_length = 1000)
    last_login = models.DateTimeField(default=now, editable=True)
    path_profile_pic = models.CharField(max_length = 1000)
    role_code = models.IntegerField()


    class Meta:  
      db_table="user"
      managed = False
      ordering = ('id',)