from datetime import datetime
from django.shortcuts import render
from django.http import HttpRequest
from app.models import questionanswer
from django.http import HttpRequest

def queryDb_QA():
   
   class questionanswerDto:
       question = []
       answer = []

   query = list(questionanswer.objects.all())

   for result in query:
        (questionanswerDto.question).append(result.question)
        (questionanswerDto.answer).append(result.answer)

   return questionanswerDto