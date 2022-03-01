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