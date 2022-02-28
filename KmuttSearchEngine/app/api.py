from app.models import *
from KmuttSearchEngine.Query import *
from django.http import JsonResponse
import datetime
import time

def get_notification(request):

    if request.method == "POST":
        query = queryDb_notification_reminder(request.user.id)

        for count, id  in enumerate(query.user_id):
            user_query = userinfo.objects.get(id=id)
            query.user_id[count] = user_query.username
            query.path[count] = user_query.path_profile_pic

        for count,(date,time1) in enumerate(zip(query.updated_date,query.updated_time)):
            datem = datetime.datetime.strptime(str(date)+str(time1), "%Y-%m-%d%H:%M:%S")
            date_time = datetime.datetime(datem.year, datem.month, datem.day, datem.hour, datem.minute)
            query.updated_time[count] = time.mktime(date_time.timetuple())

        length = len(query.request_id)
        return JsonResponse({'user_id':query.user_id,'question':query.question,'date':query.updated_date,'time':query.updated_time,
        'type':query.request_type,'path': query.path,'length':length, 'status': query.status_id, 'request_id':query.request_id},safe=False)
    else:
        return JsonResponse("Error",safe=False)

def get_notification_badge(request):

    if request.method == "POST":
        query = queryDb_notification_reminder(request.user.id)
        length = len(query.request_id)
        return JsonResponse({'length':length},safe=False)
    else:
        return JsonResponse("Error",safe=False)