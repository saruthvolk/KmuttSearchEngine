from datetime import datetime
from django.shortcuts import render
from numpy import append
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
     created_by = []
     updated_date = []
     updated_time = []
     status = []
     view_count = []
     def reset():
         questionanswerDto.id = []
         questionanswerDto.question = []
         questionanswerDto.answer = []
         questionanswerDto.question_en = []
         questionanswerDto.answer_en =[]
         questionanswerDto.created_time = []
         questionanswerDto.created_date =[]
         questionanswerDto.created_by = []
         questionanswerDto.updated_date = []
         questionanswerDto.updated_time = []
         questionanswerDto.status = []
         questionanswerDto.view_count = []

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

class notification_reminderDto:
    reminder_id = []
    request_id = []
    user_id = []
    read_date =  []
    read_time =  []
    is_read = []
    def reset():
         notification_reminderDto.reminder_id = []
         notification_reminderDto.request_id = []
         notification_reminderDto.user_id = []
         notification_reminderDto.read_date = []
         notification_reminderDto.read_time = []
         notification_reminderDto.is_read= []
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
   query = list(questionanswer.objects.all())

   for result in query:
        (questionanswerDto.id).append(result.id)
        (questionanswerDto.question).append(result.question)
        (questionanswerDto.answer).append(result.answer)
        (questionanswerDto.question_en).append(result.question_en)
        (questionanswerDto.answer_en).append(result.answer_en)
        (questionanswerDto.created_time).append(result.created_time)
        (questionanswerDto.created_date).append(result.created_date)
        (questionanswerDto.created_by).append(result.created_by)
        (questionanswerDto.updated_date).append(result.updated_date)
        (questionanswerDto.updated_time).append(result.updated_time)
        (questionanswerDto.status).append(result.status)
        (questionanswerDto.view_count).append(result.view_count)

   return questionanswerDto

def queryDb_QA_All():
   
   try:
     query = list(questionanswer.objects.all())  
   except:
     query = "Error"

   return query

def queryDb_QA_All_FAQ():
   
   try:
     query = list(questionanswer.objects.all().order_by('-view_count'))  
   except:
     query = "Error"

   return query

def queryDb_QA_All_Recent():
   
   try:
     query = list(questionanswer.objects.all().order_by('-updated_date','-updated_time'))  
   except:
     query = "Error"

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

def queryDb_multi_User(id):

   query = [userinfo.objects.filter(id= x).only('username','path_profile_pic') for x in id]
   query = [data for user in query for data in user]

   return query

def queryDb_department():
     try:
          query = list(department.objects.all()) 
     except:
          query = "Error"
     
     return query

def queryDb_request_noti(noti_reminder):
     try:
          QArequestDto.reset()
          query = list(QArequest.objects.filter(request_id__in = noti_reminder.request_id).order_by('-created_date','-created_time')) 
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
          query = list(QArequest.objects.filter(user_id=id).order_by('-created_date','-created_time'))

     except:
          query = "Error"

     return query

def queryDb_request_all():

     try:

          query = list(QArequest.objects.order_by('-created_date','-created_time'))

     except:
          query = "Error"

     return query

def queryDb_onerequest(id):
 
     try:
          query = list(QArequest.objects.filter(request_id = id))

     except:
          query = "Error"

     return query

def queryDb_onequestion(id):
 
     try:
          query = questionanswer.objects.get(id = id) 
     except:
          query = "Error"

     return query

def queryDb_notification_reminder(id):

     try:
          query = notification_reminder.objects.filter(user_id = id, is_read = False).only('request_id')
          notification_reminderDto.request_id = [data.request_id for data in query]
          query = queryDb_request_noti(notification_reminderDto)

     except:
          query = "Error"

     return query