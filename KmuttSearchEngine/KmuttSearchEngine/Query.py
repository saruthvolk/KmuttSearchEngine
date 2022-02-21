from datetime import datetime
from django.shortcuts import render
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
    suspended_by = []
    suspended_date = []
    suspended_time = []
    status = []
    first_name = []
    last_name = []
    email = []
    last_login = []
    path_profile_pic = []
    role_code =[]
    gender =[]
    date_of_birth = []

class departmentDto:
     department_id = []
     department_name = []

class QArequestDto:

    request_id = []
    question = []
    answer = []
    question_en = []
    answer_en = []
    status_id = []
    created_date = []
    request_type = []
    department_id = []
    user_id = []
    question_id =  []
    remark = []
    created_time = []
    updated_date = []
    updated_time = []
    updated_by = []
    rejected_date = []
    rejected_time = []
    rejected_by = []
    path = []
    def reset():
          QArequestDto.request_id = []
          QArequestDto.question = []
          QArequestDto.answer = []
          QArequestDto.question_en = []
          QArequestDto.answer_en = []
          QArequestDto.status_id = []
          QArequestDto.created_date = []
          QArequestDto.request_type = []
          QArequestDto.department_id = []
          QArequestDto.user_id = []
          QArequestDto.question_id =  []
          QArequestDto.remark = []
          QArequestDto.created_time = []
          QArequestDto.updated_date = []
          QArequestDto.updated_time = []
          QArequestDto.updated_by = []
          QArequestDto.rejected_date = []
          QArequestDto.rejected_time = []
          QArequestDto.rejected_by = []
          QArequestDto.path = []

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

       if   user.suspended_by is not None:
            user.suspended_by = query[int(user.suspended_by)-1].username+" (ID: "+str(user.suspended_by)+")"
       elif user.created_by is not None:
            user.created_by = query[int(user.created_by)-1].username+" (ID: "+str(user.created_by)+")"
       elif user.updated_by is not None:
            user.updated_by = query[int(user.updated_by)-1].username+" (ID: "+str(user.updated_by)+")"
       else:
            user.suspended_by = user.suspended_by
            user.created_by = user.created_by 
            user.updated_by= user.updated_by

   return query

def queryDb_User(id):
   
   query = userinfo.objects.filter(id=id)

   for user in query:   
       role = user_role.objects.get(role_code=user.role_code)
       user.role_code = role.role_name

   return query

def queryDb_department():
     try:
          query = list(department.objects.all()) 
     except:
          query = "Error"
     
     return query

def queryDb_request():
     try:
          QArequestDto.reset()
          query = list(QArequest.objects.order_by('-created_date','-created_time')) 
          for noti in query:
               QArequestDto.request_id.append(noti.request_id)
               QArequestDto.question.append(noti.question)
               QArequestDto.answer.append(noti.answer)
               QArequestDto.question_en.append(noti.question_en)
               QArequestDto.answer_en.append(noti.answer_en)
               QArequestDto.status_id.append(noti.status_id)
               QArequestDto.created_date.append(noti.created_date)
               QArequestDto.request_type.append(noti.request_type)
               QArequestDto.department_id.append(noti.department_id)
               QArequestDto.user_id.append(noti.user_id)
               QArequestDto.question_id.append(noti.question_id)
               QArequestDto.remark.append(noti.remark)
               QArequestDto.created_time.append(noti.created_time)
               QArequestDto.updated_date.append(noti.updated_date)
               QArequestDto.updated_time.append(noti.updated_time)
               QArequestDto.updated_by.append(noti.updated_by)
               QArequestDto.rejected_date.append(noti.rejected_date)
               QArequestDto.rejected_time.append(noti.rejected_time)
               QArequestDto.rejected_by.append(noti.rejected_by)
               QArequestDto.path.append(noti.user_id)

     except:
          query = "Error"

     return QArequestDto

def queryDb_Request_user(id):
 
     try:
          query = list(QArequest.objects.order_by('-created_date','-created_time')) 
     except:
          query = "Error"

     return query