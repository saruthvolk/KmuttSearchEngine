import datetime
from django.http import HttpRequest
from app.models import *
from KmuttSearchEngine.Query import *

class Result:
  code = ''
  context = {}
  query = ''

def request_update (request):
    current_time = datetime.datetime.now().replace(microsecond=0)
    if request.method == "POST":
        if  (request.POST.get('question') and request.POST.get('answer')) or (request.POST.get('question_en') 
        and request.POST.get('answer_en')) and request.POST.get('department_id') and request.POST.get('remark'):
                saverecord = QArequest()
                saverecord.question = request.POST.get('question')
                saverecord.answer = request.POST.get('answer')
                saverecord.question_en = request.POST.get('question_en')
                saverecord.answer_en = request.POST.get('answer_en')
                saverecord.user_id = request.user.id
                saverecord.status_id = '1'
                saverecord.request_type = "Add"
                saverecord.department_id = request.POST.get('department_id')
                saverecord.remark = request.POST.get('remark')
                saverecord.created_date = current_time
                saverecord.created_time = current_time
                question_id = None
                saverecord.save()

        Result.code = 200

    return Result

def request_saveedit (request):
    current_time = datetime.datetime.now().replace(microsecond=0)
    if request.method == "POST":
        if  (request.POST.get('question') and request.POST.get('answer')) or (request.POST.get('question_en') 
        and request.POST.get('answer_en')) and request.POST.get('department_id') and request.POST.get('remark') and request.POST.get('request_id'): 
                updaterecord = QArequest_edit.objects.get(request_id =  request.POST.get('request_id'))
                updaterecord.question = request.POST.get('question')
                updaterecord.answer = request.POST.get('answer')
                updaterecord.question_en = request.POST.get('question_en')
                updaterecord.answer_en = request.POST.get('answer_en')
                updaterecord.user_id = request.user.id
                updaterecord.status_id = '1'
                updaterecord.request_type = "Add"
                updaterecord.department_id = request.POST.get('department_id')
                updaterecord.remark = request.POST.get('remark')
                updaterecord.updated_date = current_time
                updaterecord.updated_time = current_time
                print(request.POST.get('request_id'))
                print(request.POST.get('user_id'))
                updaterecord.save()

        Result.code = 200
        query = list(QArequest.objects.all())
        Result.query = query
    return Result