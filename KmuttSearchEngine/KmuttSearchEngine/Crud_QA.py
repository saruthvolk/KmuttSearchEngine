import datetime
from django.http import HttpRequest
from app.models import questionanswer
from app.models import edit_questionanswer
from KmuttSearchEngine.Query import queryDb_QA_All

class Result:
  code = ''
  message = ''
  query = ''

def Add_QA(request):
	assert isinstance(request, HttpRequest)
	current_time = datetime.datetime.now().replace(microsecond=0)
	if request.method == "POST" :
		if  (request.POST.get('question') and request.POST.get('answer')) or (request.POST.get('question_en') and request.POST.get('answer_en')) and request.POST.get('department_id'):
			saverecord = questionanswer()
			saverecord.question = request.POST.get('question')
			#saverecord.question_sw = stopwords1(saverecord.question)
			saverecord.answer = request.POST.get('answer')
			saverecord.question_en = request.POST.get('question_en')
			saverecord.answer_en = request.POST.get('answer_en')
			saverecord.user_id = request.user.id
			saverecord.updated_by = 1 #waiting for user function
			saverecord.status = True
			saverecord.view_count = 1 #waiting for user function
			saverecord.department_id = request.POST.get('department_id')
			saverecord.updated_date = current_time
			saverecord.updated_time = current_time
			saverecord.created_date = current_time
			saverecord.created_time = current_time
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

def View_QA(reuqest,id):

	query = queryDb_QA_All()

	Result.query = query
	Result.code = 300

	return (Result)

def Edit_QA(request,id):
	temp = []

	temp = questionanswer.objects.filter(id__in=id)

	Result.query = temp
	Result.code = 300

	return (Result)

def Remove_QA(request,id):

	temp = questionanswer.objects.filter(id__in=id)
	temp.delete()
	
	query = list(questionanswer.objects.all())

	Result.query = query
	Result.code = 300

	return (Result)

def Update_QA(request,id):

	if request.method == "POST" :
		if request.POST.get('id_check') and request.POST.get('question') and request.POST.get('answer') and request.POST.get('question_en') and request.POST.get('answer_en') :
			saverecord = edit_questionanswer()
			question = request.POST.getlist('question')
			#question_sw = stopwords1(question)
			#question_tokenized = tokenized(question)
			answer = request.POST.getlist('answer')
			question_en = request.POST.getlist('question_en')
			answer_en = request.POST.getlist('answer_en')
			saverecord.updated_by = 1 #waiting for user function
		
		current_time = datetime.datetime.now().replace(microsecond=0) 
		for i in range(len(id)):
			saverecord.id = id[i]
			saverecord.question = question[i]
			#saverecord.question_sw = question_sw[i]
			#saverecord.question_tokenized = question_tokenized[i]
			saverecord.answer = answer[i]
			saverecord.question_en = question_en[i]
			saverecord.answer_en = answer_en[i]
			saverecord.updated_by = 1 #waiting for user function
			saverecord.updated_date = current_time
			saverecord.updated_time = current_time
			saverecord.save()

	query = list(questionanswer.objects.all())
	Result.code = 300
	Result.query = query
	return (Result)