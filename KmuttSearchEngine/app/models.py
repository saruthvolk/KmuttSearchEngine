"""
Definition of models.
"""

from django.db import models
import datetime
from django.contrib.auth.models import User 
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import AbstractBaseUser,UserManager

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

class userinfo(AbstractBaseUser):

    id = models.AutoField(primary_key=True,unique=True)
    username = models.CharField(max_length = 1000,unique=True)
    password = models.CharField(max_length = 1000)
    created_by = models.CharField(max_length = 1000)
    created_time = models.DateTimeField(default=now, editable=True)
    created_date = models.DateTimeField(default=now, editable=True)
    updated_by = models.CharField(max_length = 1000)
    updated_time = models.DateTimeField(default=now, editable=True)
    updated_date = models.DateTimeField(default=now, editable=True)
    suspended_by = models.CharField(max_length = 1000)
    suspended_date = models.DateTimeField(default=None, editable=True)
    suspended_time = models.DateTimeField(default=None, editable=True)
    is_active = models.BooleanField()
    first_name = models.CharField(max_length = 1000)
    last_name = models.CharField(max_length = 1000)
    email = models.CharField(max_length = 1000)
    last_login = models.DateTimeField(default=now, editable=True)
    path_profile_pic = models.CharField(max_length = 1000)
    role_code = models.IntegerField()
    gender =models.CharField(max_length = 1000)
    date_of_birth = models.DateTimeField(default=None, editable=True)
    phone_no = models.CharField(max_length = 1000)

    REQUIRED_FIELDS = ('id',)
    USERNAME_FIELD = 'username'
    PASSWORD_FIELD = 'password'

    objects = UserManager()

    class Meta:  
      db_table="user"
      managed = False
      ordering = ('id',)

class user_role (models.Model):

    role_code = models.IntegerField(primary_key=True,unique=True)
    role_name = models.CharField(max_length = 1000)

    class Meta:
      db_table="user_role"

class QArequest (models.Model):
    request_id = models.AutoField(primary_key=True)
    question = models.CharField(max_length = 1000)
    answer = models.CharField(max_length = 1000)
    question_en = models.CharField(max_length = 1000)
    answer_en = models.CharField(max_length = 1000)
    status_id = models.IntegerField()
    created_date = models.DateTimeField(default=now, editable=True)
    request_type = models.CharField(max_length = 1000)
    department_id = models.IntegerField()
    user_id = models.IntegerField()
    question_id =  models.IntegerField()
    remark = models.CharField(max_length = 1000)
    created_time = models.DateTimeField(default=None, editable=True)
    updated_date = models.DateTimeField(default=None, editable=True)
    updated_time = models.DateTimeField(default=None, editable=True)
    updated_by = models.CharField(max_length = 1000)
    rejected_date = models.DateTimeField(default=None, editable=True)
    rejected_time = models.DateTimeField(default=None, editable=True)
    rejected_by = models.CharField(max_length = 1000)
    rejected_remark = models.CharField(max_length = 1000)
 
    class Meta:
      db_table="request"
      managed = False

class department (models.Model):
    department_id = models.AutoField(primary_key=True)
    department_name = models.CharField(max_length = 1000)

    class Meta:
      db_table="department"

class QArequest_edit (models.Model):
    request_id = models.AutoField(primary_key=True)
    question = models.CharField(max_length = 1000)
    answer = models.CharField(max_length = 1000)
    question_en = models.CharField(max_length = 1000)
    answer_en = models.CharField(max_length = 1000)
    status_id = models.IntegerField()
    request_type = models.CharField(max_length = 1000)
    department_id = models.IntegerField()
    user_id = models.IntegerField()
    question_id =  models.IntegerField()
    remark = models.CharField(max_length = 1000)
    updated_date = models.DateTimeField(default=now, editable=True)
    updated_time = models.DateTimeField(default=now, editable=True)
    updated_by = models.CharField(max_length = 1000)
    rejected_date = models.DateTimeField(default=None, editable=True)
    rejected_time = models.DateTimeField(default=None, editable=True)
    rejected_by = models.CharField(max_length = 1000)
    rejected_remark = models.CharField(max_length = 1000)
 
    class Meta:
      db_table="request"

class status (models.Model):
  status_id = models.AutoField(primary_key=True)
  status_type = models.CharField(max_length = 1000)

  class Meta:
      db_table="status"