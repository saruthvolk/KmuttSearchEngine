"""
Definition of views.
"""

from datetime import datetime
from django.shortcuts import render
from django.http import HttpRequest
from KmuttSearchEngine.SearchEngine import searchengine
from KmuttSearchEngine.SearchEngine import return_Result

def home(request):
	"""Renders the home page."""
	assert isinstance(request, HttpRequest)
	return render(
		request,
		'app/index.html',
		{
			'title':'Home Page',
			'year':datetime.now().year,
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
	search = request.POST.get('search')
	result = searchengine(search)

	if result.Correct is not None:
	   pre_seach = search
	   search = result.Correct
	   check = 1
	   return render(request,'app/search.html', {'Correct': result.Correct, 'Question': pre_seach, 'Result': result.res})
	else:
	   check = 0
	   return render(request,'app/search.html', {'Result': result.res, 'Question': search})

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