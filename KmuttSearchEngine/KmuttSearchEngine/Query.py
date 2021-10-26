from datetime import datetime
from django.shortcuts import render
from django.http import HttpRequest
from app.models import questionanswer
from django.http import HttpRequest




def queryDb_QA():
   
   class questionanswerDto:
        question = []
        answer = []
        question_en = []
        answer_en =[]
        created_time = []
        created_date =[]
        user_id = []
        updated_date = []
        updated_time = []
        status = []
        view_count = []


   query = list(questionanswer.objects.all())

   for result in query:
        (questionanswerDto.question).append(result.question)
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
        question = []
        answer = []
        question_en = []
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