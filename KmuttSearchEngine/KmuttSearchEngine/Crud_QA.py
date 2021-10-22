from datetime import datetime
from django.shortcuts import render
from django.http import HttpRequest

class Result:
  code = ''
  message = ''

def Add_QA(request):
	assert isinstance(request, HttpRequest)
	if request.method == "POST" :
		if request.POST.get('question_id') and request.POST.get('question') and request.POST.get('answer') and request.POST.get('question_en') and request.POST.get('answer_en') and request.POST.get('create_time') and request.POST.get('create_date') and request.POST.get('user_id') and request.POST.get('update_date') and request.POST.get('update_time') and request.POST.get('status') and request.POST.get('view_count'):
			saverecord = questionanswer()
			saverecord.question_id = request.POST.get('question_id')
			saverecord.question = request.POST.get('question')
			saverecord.answer = request.POST.get('answer')
			saverecord.question_en = request.POST.get('question_en')
			saverecord.answer_en = request.POST.get('answer_en')
			saverecord.create_time = request.POST.get('create_time')
			saverecord.create_date = request.POST.get('create_date')
			saverecord.user_id = request.POST.get('user_id')
			saverecord.update_date = request.POST.get('update_date')
			saverecord.update_time = request.POST.get('update_time')
			saverecord.status = request.POST.get('status')
			saverecord.view_count = request.POST.get('view_count')
			saverecord.save()

			Result.code == 200
			Result.message == 'Successful'

			return Result
	else:
		Result.code == 200
		Result.message == 'Error'
		return Result
