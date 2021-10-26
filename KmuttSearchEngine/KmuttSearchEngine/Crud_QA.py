from datetime import date
from datetime import time
from django.utils.timezone import now
from django.shortcuts import render
from django.http import HttpRequest
from app.models import questionanswer
from app.models import edit_questionanswer
from app.forms import editform

class Result:
  code = ''
  message = ''
  query = ''

def Add_QA(request):
	assert isinstance(request, HttpRequest)
	if request.method == "POST" :
		if  request.POST.get('question') and request.POST.get('answer') and request.POST.get('question_en') and request.POST.get('answer_en') and request.POST.get('user_id') and request.POST.get('updated_by') and request.POST.get('department_id'):
			saverecord = questionanswer()
			saverecord.question = request.POST.get('question')
			saverecord.answer = request.POST.get('answer')
			saverecord.question_en = request.POST.get('question_en')
			saverecord.answer_en = request.POST.get('answer_en')
			saverecord.user_id = request.POST.get('user_id')
			saverecord.updated_by = request.POST.get('updated_by')
			saverecord.status = True
			saverecord.view_count = '0'
			saverecord.department_id = request.POST.get('department_id')
			saverecord.save()

			Result.code == 200
			Result.message == 'Successful'

			return Result
		else:
			Result.code == 300
			Result.message == 'Successful'

			return Result
	else:
		Result.code == 400
		Result.message == 'Error'
		return Result

def Edit_QA(request,id):
	temp = []

	temp = questionanswer.objects.filter(id__in=id)

	Result.query = temp
	Result.code = 300

	return (Result)

def Remove_QA(request,id):

	temp = questionanswer.objects.filter(id__in=id)
	temp.delete()
	
	Result.query = temp
	Result.code = 300

	return (Result)

def Update_QA(request,id):

	if request.method == "POST" :
		if request.POST.get('id') and request.POST.get('question') and request.POST.get('answer') and request.POST.get('question_en') and request.POST.get('answer_en') :
			saverecord = edit_questionanswer()
			saverecord.id = request.POST.get('id')
			saverecord.question = request.POST.get('question')
			saverecord.answer = request.POST.get('answer')
			saverecord.question_en = request.POST.get('question_en')
			saverecord.answer_en = request.POST.get('answer_en')
			saverecord.save()

	query = list(questionanswer.objects.all())
	Result.code = 300
	Result.query = query
	return (Result)