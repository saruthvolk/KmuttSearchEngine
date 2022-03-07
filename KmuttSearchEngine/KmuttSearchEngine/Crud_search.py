import datetime
from app.models import *
from KmuttSearchEngine.Query import *


class Result:
  code = ''
  message = ''
  query = ''


def create_search_history(request, search):

    current_time = datetime.datetime.now().replace(microsecond=0)

    try:
        if (search_history.objects.filter(user_id=request.user.id, query = search).exists()): 
            saverecord = search_history.objects.get(user_id=request.user.id,query = search)
            saverecord.created_date = current_time
            saverecord.created_time = current_time
            saverecord.save()
        else:
            saverecord = search_history()
            saverecord.query = search
            saverecord.created_date = current_time
            saverecord.created_time = current_time
            saverecord.user_id = request.user.id
            saverecord.save()

        Result.code = "200"
	
    except:

        Result.code == "Error"

    return (Result)

def view_search_history (request,id):

    try:
        query = list(search_history.objects.filter(user_id = id))
    except:
        query = "Error"

    return query

def create_view_history(request,id):

    current_time = datetime.datetime.now().replace(microsecond=0)

    try:
        if (view_history.objects.filter(user_id=request.user.id,question_id = id).exists()):       
            saverecord = view_history.objects.get(user_id=request.user.id,question_id = id)
            saverecord.view_date = current_time
            saverecord.view_time = current_time
            saverecord.save()
        else:
            saverecord = view_history()
            saverecord.question_id = id
            saverecord.view_date = current_time
            saverecord.view_time = current_time
            saverecord.user_id = request.user.id
            saverecord.save()

        Result.code = "200"
	
    except:

        Result.code == "Error"

    return (Result)

def view_view_history(request,id):


    try:
        query = list(view_history.objects.filter(user = id).order_by('-view_date','-view_time'))

    except:
        query = "Error"

    print (query)
    return query