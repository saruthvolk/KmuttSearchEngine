import datetime
from django.http import HttpRequest
from torch import save
from app.models import search_history
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

	try:
		if request.method == "POST" :
			if  (request.POST.get('question') and request.POST.get('answer')) or (request.POST.get('question_en') or request.POST.get('answer_en')) and request.POST.get('department_id'):
				question_en = request.POST.getlist('question_en')
				question = request.POST.getlist('question')
				answer = request.POST.getlist('answer')
				answer_en = request.POST.getlist('answer_en')
				department = request.POST.getlist('department_id')

				for i in range(len(question)):
					saverecord = questionanswer()
					saverecord.question = question[i]
					saverecord.answer = answer[i]
					saverecord.question_en = question_en[i]
					saverecord.answer_en = answer_en[i]
					saverecord.created_by = request.user.id
					saverecord.updated_by = request.user.id
					saverecord.status = True
					saverecord.view_count = request.user.id
					saverecord.department_id = department[i]
					saverecord.updated_date = current_time
					saverecord.updated_time = current_time
					saverecord.created_date = current_time
					saverecord.created_time = current_time
					saverecord.save()

					Result.code = 200
					Result.message = 'Successful'

			else:
				Result.code = 400
				Result.message = 'Error'
				return Result

	except:
		Result.code = 400
		Result.message = 'Error'

	return Result

def View_QA(reuqest,id):

	query = queryDb_QA_All()

	Result.query = query
	Result.code = 300

	return (Result)

def Edit_QA(request,id):
	
	try:
		temp = []
		if (request.method == "POST"):
			temp = questionanswer.objects.filter(id__in=id)
		elif (request.method == "GET"):
			temp = questionanswer.objects.filter(id=id)
		Result.query = temp
		Result.code = 200
	except:
		Result.code = "Error"

	return (Result)

def Remove_QA(request,id):

	try:
		temp = questionanswer.objects.filter(id__in=id)
		temp.delete()
	
		query = list(questionanswer.objects.all())

		Result.query = query
		Result.code = 200
	except:
		Result.code = "Error"

	return (Result)

def Update_QA(request,id):

	try:
		if request.method == "POST" :
			if request.POST.get('id_check') and request.POST.get('question') and request.POST.get('answer') and request.POST.get('department_id'):
				saverecord = edit_questionanswer()
				question_en = request.POST.getlist('question_en')
				question = request.POST.getlist('question')
				answer = request.POST.getlist('answer')
				answer_en = request.POST.getlist('answer_en')
				department = request.POST.getlist('department_id')

				current_time = datetime.datetime.now().replace(microsecond=0) 
				for i in range(len(id)):
					saverecord.id = id[i]
					saverecord.question = question[i]
					saverecord.answer = answer[i]
					saverecord.question_en = question_en[i]
					saverecord.answer_en = answer_en[i]
					saverecord.department_id = department[i]
					saverecord.updated_by = request.user.id
					saverecord.updated_date = current_time
					saverecord.updated_time = current_time
					saverecord.save()
					Result.code = 200
					query = list(questionanswer.objects.all())
					Result.query = query
			else:
				Result.code = "Error"
		else:
			Result.code = "Error"
	except:
			Result.code = "Error"

	return (Result)