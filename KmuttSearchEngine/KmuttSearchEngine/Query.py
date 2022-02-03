from datetime import datetime
from django.shortcuts import render
from django.http import HttpRequest
from app.models import *
from django.http import HttpRequest


class questionanswerDto:

     id = []
     question = []
     answer = []
     question_en = []
     question_sw = []
     answer_en =[]
     created_time = []
     created_date =[]
     user_id = []
     updated_date = []
     updated_time = []
     status = []
     view_count = []
     def reset():
         questionanswerDto.id = []
         questionanswerDto.question = []
         #questionanswerDto.question_sw = []
         questionanswerDto.questionanswer = []
         questionanswerDto.question_en = []
         questionanswerDto.answer_en =[]
         questionanswerDto.created_time = []
         questionanswerDto.created_date =[]
         questionanswerDto.user_id = []
         questionanswerDto.updated_date = []
         questionanswerDto.updated_time = []
         questionanswerDto.status = []
         questionanswerDto.view_count = []
         #questionanswerDto.question_tokenized = []

class UserDto:

    id = []
    username = []
    password = []
    created_by = []
    created_time = []
    created_date = []
    updated_by = []
    updated_time = []
    updated_date = []
    deleted_by = []
    deleted_date = []
    deleted_time = []
    status = []
    first_name = []
    last_name = []
    email = []
    last_login = []
    path_profile_pic = []
    role_code =[]
    gender =[]
    date_of_birth = []

def queryDb_QA():

   questionanswerDto.reset()
   print (len(questionanswerDto.question))
   query = list(questionanswer.objects.all())

   for result in query:
        (questionanswerDto.id).append(result.id)
        (questionanswerDto.question).append(result.question)
        #(questionanswerDto.question_sw).append(result.question_sw)
        #(questionanswerDto.question_tokenized).append(result.question_tokenized)
        (questionanswerDto.answer).append(result.answer)
        (questionanswerDto.question_en).append(result.question_en)
        (questionanswerDto.answer_en).append(result.answer_en)
        (questionanswerDto.created_time).append(result.created_time)
        (questionanswerDto.created_date).append(result.created_date)
        (questionanswerDto.user_id).append(result.user_id)
        (questionanswerDto.updated_date).append(result.updated_date)
        (questionanswerDto.updated_time).append(result.updated_time)
        (questionanswerDto.status).append(result.status)
        (questionanswerDto.view_count).append(result.view_count)

   return questionanswerDto

def queryDb_QA_All():
   
   class questionanswerDto:
        id = []
        question = []
        question_sw = []
        answer = []
        question_en = []
        #question_tokenized = []
        answer_en =[]
        created_time = []
        created_date =[]
        user_id = []
        updated_date = []
        updated_time = []
        status = []
        view_count = []
 
   query = list(questionanswer.objects.all())  

   return query

def queryDb_User_All():
   
   query = list(userinfo.objects.all()) 

   for user in query:   
       role = user_role.objects.get(role_code=user.role_code)
       user.role_code = role.role_name

   return query