"""
Definition of views.
"""

from datetime import date
from datetime import time
from django.shortcuts import render
from django.http import HttpRequest
from KmuttSearchEngine.SearchEngine import searchengine
from KmuttSearchEngine.Crud_QA import *
from KmuttSearchEngine.Query import queryDb_QA
from app.models import questionanswer
from KmuttSearchEngine.SearchEngine import return_Result
from django.contrib import messages

def home(request):
	"""Renders the home page."""
	assert isinstance(request, HttpRequest)
	return render(
		request,
		'app/index.html',
		{
			'title':'Home Page',
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

def search(request):
	"""Renders the contact page."""
	assert isinstance(request, HttpRequest)
	table = "questionanswer"
	query = queryDb_QA()

	search = request.POST.get('search')
	result = searchengine(search, query)

	if result.Correct is not None:
	   pre_seach = search
	   search = result.Correct
	   check = 1
	   return render(request,'app/search.html', {'Correct': result.Correct, 'Question': pre_seach, 'Result': result.res, 'Position': result.pos})
	else:
	   check = 0
	   return render(request,'app/search.html', {'Result': result.res, 'Question': search, 'Answer':result.ans})

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

def Crud_QA (request):

	operation = 'Add'
	if operation == "Add":
		result = Add_QA(request)
		if result.code == 200:
			return render(request,'app/index.html')
		else:
			return render(request,'app/CRUDquestion.html')

	elif operation == "Edit":
		result = Edit_QA()

	elif operation == "Remove":
		result = Remove_QA()


#def insertques(request):

#	assert isinstance(request, HttpRequest)
#	if request.method == "POST" :
#		if request.POST.get('question_id') and request.POST.get('question') and request.POST.get('answer') and request.POST.get('question_en') and request.POST.get('answer_en') and request.POST.get('create_time') and request.POST.get('create_date') and request.POST.get('user_id') and request.POST.get('update_date') and request.POST.get('update_time') and request.POST.get('status') and request.POST.get('view_count'):
#			saverecord = questionanswer()
#			saverecord.question_id = request.POST.get('question_id')
#			saverecord.question = request.POST.get('question')
#			saverecord.answer = request.POST.get('answer')
#			saverecord.question_en = request.POST.get('question_en')
#			saverecord.answer_en = request.POST.get('answer_en')
#			saverecord.create_time = request.POST.get('create_time')
#			saverecord.create_date = request.POST.get('create_date')
#			saverecord.user_id = request.POST.get('user_id')
#			saverecord.update_date = request.POST.get('update_date')
#			saverecord.update_time = request.POST.get('update_time')
#			saverecord.status = request.POST.get('status')
#			saverecord.view_count = request.POST.get('view_count')
#			saverecord.save()
			#messages.success(request,'question '+saverecord.question_id+ 'is saved in the datebase')#
#			return render(request,'app/CRUDquestion.html')
#	else:
#		return render(request,'app/CRUDquestion.html')