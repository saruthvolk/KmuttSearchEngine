"""
Definition of views.
"""
import oskut
import os
from django.shortcuts import render
from django.http import HttpRequest
from KmuttSearchEngine.SearchEngine import searchengine
from KmuttSearchEngine.SearchEngine import train_dictionary
from KmuttSearchEngine.Crud_QA import *
from KmuttSearchEngine.Query import *
from app.models import questionanswer
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
import json

class Search_result:
  Retry = 0
  Correct = None
  code = ''
  query = ''
  percentage = ''
  search = ''
  ans = ''

  oskut.load_model(engine='deepcut')
  tokenized = oskut.OSKut("Process",k=1)

def home(request):

	"""Renders the home page."""
	assert isinstance(request, HttpRequest)

	query = queryDb_QA()
	question = query.question;
	json_question = json.dumps(question)

	feature_question = list(questionanswer.objects.all().order_by('view_count').reverse())[:5]

	return render(
		request,
		'app/index.html',
		{
			'title':'Home Page',
			'question':json_question,
			'feature_question': feature_question
			#'year':datetime.now().year,#
		}
	)

def contact(request):
	"""Renders the contact page."""
	assert isinstance(request, HttpRequest)
	return render(
		request,
		'app/contact.html',
		{
			'title':'Contact',
			'message':'Your contact page.',
			'year':datetime.now().year,
		}
	)

def train_dict(request):

	assert isinstance(request, HttpRequest)

	print ("Creating Dict")
	query = queryDb_QA()
	for answer in query.answer:
		(query.question).append(answer)

	result = train_dictionary(query.question)
	
	if result.code == 200:
		return render(request,'app/index.html')
	else:
		message = 'Done'
		return render(request,'app/index.html', {'message':'Done'})

def search(request):

	assert isinstance(request, HttpRequest)

	search = request.POST.get('search')

	page = request.GET.get('page', 1)

	if page == 1:
		query = queryDb_QA()
		result = searchengine(search, query)
		Search_result.search = search
		Search_result.query = result.query
		Search_result.Correct = result.Correct
		Search_result.percentage = result.percentage

	length = Search_result.percentage;
	paginator = Paginator(Search_result.query, 10)
	paginator1 = Paginator(Search_result.percentage, 10)

	try:
		query1 = paginator.page(page)
		query2 =paginator1.page(page)

	except PageNotAnInteger:
		query1 = paginator.page(1)
		query2 = paginator1.page(1)

	except EmptyPage:
		query1 = paginator.page(paginator.num_pages)
		query2 =paginator1.page(paginator1.num_pages)
	
	if search:
		pre_search = search
	else:
		pre_search = Search_result.search

	if Search_result.Correct is not None:
	   check = 1
	   return render(request,'app/search.html', {'Correct': Search_result.Correct, 'Question': pre_search, 'query': query1, 'Percentage': query2, 'length': length})
	else:
	   check = 0
	   return render(request,'app/search.html', {'Question': pre_search, 'query': query1, 'Question': pre_search, 'Percentage': query2, 'length': length })


def about(request):
	"""Renders the about page."""
	assert isinstance(request, HttpRequest)
	return render(
		request,
		'app/about.html',
		{
			'title':'About',
			'message':'Your application description page.',
			'year':datetime.now().year,
		}
	)

def question(request,id):
	"""Renders the about page."""
	assert isinstance(request, HttpRequest)

	#================ Update view count ==================#
	result = questionanswer.objects.get(id=id)
	result.view_count = result.view_count+1;
	result.save(update_fields=["view_count"]) 

	#================ Query ==================#
	result = questionanswer.objects.get(id=id)
	return render(
		request,
		'app/question.html',
		{
			'title':'Question Detail',
			'query': result,
			'year':datetime.now().year,
		}
	)

def Admin(request):
	"""Renders the about page."""
	assert isinstance(request, HttpRequest)
	return render(
		request,
		'app/Admin.html',
		{
			'title':'Admin Panel',
			'year':datetime.now().year,
		}
	)

@csrf_exempt
def upload_image(request):
	if request.method == "POST":
		file_obj = request.FILES['file']
		file_name_suffix = file_obj.name.split(".")[-1]
		if file_name_suffix not in ["jpg", "png", "gif", "jpeg", ]:
			return JsonResponse({"message": "Wrong file format"})

		upload_time = timezone.now()
		path = os.path.join(
			settings.MEDIA_ROOT,
			'static',
			'img',
			str(upload_time.year),
			str(upload_time.month),
			str(upload_time.day)
		)
		# If there is no such path, create
		if not os.path.exists(path):
			os.makedirs(path)

		file_path = os.path.join(path, file_obj.name)

		file_url = f'/static/img/{upload_time.year}/{upload_time.month}/{upload_time.day}/{file_obj.name}'

		if os.path.exists(file_path):
			return JsonResponse({
				"message": "file already exist",
				'location': file_url
			})

		with open(file_path, 'wb+') as f:
			for chunk in file_obj.chunks():
				f.write(chunk)

		return JsonResponse({
			'message': 'Image uploaded successfully',
			'location': file_url
		})
	return JsonResponse({'detail': "Wrong request"})


def Crud_QA (request, operation,id):

	if operation == "Add":

		result = Add_QA(request)
		if result.code == 200:
			return render(request,'app/index.html')
		else:
			return render(request,'app/CRUDquestion.html')

	elif operation == "View":

		result = View_QA(request,id)

		return render(request, 'app/Viewquestion.html', {'query': result.query})

	elif operation == "Remove":

		if request.method == 'POST':
			id = request.POST.getlist('id_check')

		result = Remove_QA(request,id)

		if result.code == 200:
			return render(request,'app/index.html')
		else:
			return render(request, 'app/Viewquestion.html', {'query': result.query})

	elif operation == "Edit":

		if request.method == 'POST':
			id = request.POST.getlist('id_check')

		result = Edit_QA(request,id)

		if result.code == 200:
			return render(request,'app/index.html')
		else:
			json_id = json.dumps(id)
			return render(request, 'app/Editquestion.html', {'query': result.query, 'id_list': json_id })

	elif operation == "Update":

		if request.method == 'POST':
			id = request.POST.getlist('id_check')

		result = Update_QA(request,id)

		if result.code == 200:
			return render(request,'app/index.html')
		else:
			return render(request, 'app/Viewquestion.html', {'query': result.query})
