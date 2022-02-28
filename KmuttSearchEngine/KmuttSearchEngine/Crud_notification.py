import datetime
from app.models import *
from KmuttSearchEngine.Query import *


class Result:
    code = ''
    context = {}
    query = ''


current_time = datetime.datetime.now().replace(microsecond=0)


def update_reminder(request, id):
    try:
        query = notification_reminder.objects.filter(
            request_id=id, user_id=request.user.id)
        for noti in query:
            noti.read_date = current_time
            noti.read_time = current_time
            noti.is_read = True
            noti.save()
    except:
        query = "Error"

    return query


def create_reminder(operation,id):

    try:
        if (operation == "update") or (operation == "editquestion"):
            request_query = QArequest.objects.last()
            user_query = userinfo.objects.filter(role_code=1).only('id')
            for user_data in user_query:
                save_reminder = notification_reminder()
                save_reminder.request_id = request_query.request_id
                save_reminder.user_id = user_data.id
                save_reminder.is_read = False
                save_reminder.save()

        elif (operation == "reject") or (operation == "saveapprove"):

            user_query = userinfo.objects.filter(role_code=1).only('id')
            request_query = QArequest.objects.filter(request_id = id)
            
            for user in user_query:
                noti_data = notification_reminder.objects.get(request_id = id, user_id = user.id)
                noti_data.user_id = user.id
                noti_data.read_date = current_time
                noti_data.read_time = current_time
                noti_data.is_read = True
                noti_data.save()

            for request in request_query:
                save_reminder = notification_reminder()
                save_reminder.request_id = id
                save_reminder.user_id = request.user_id
                save_reminder.is_read = False
                save_reminder.save()

        elif operation == 'saveedit':
            user_query = userinfo.objects.filter(role_code=1).only('id')
            for user_data in user_query :
                save_reminder = notification_reminder()
                save_reminder.request_id = id
                save_reminder.read_date= None
                save_reminder.read_time = None
                save_reminder.user_id = user_data.id
                save_reminder.is_read = False
                save_reminder.save()

        Result.code = 200

    except:
        Result.code = "Error"

    return Result

def delete_reminder(request,id):

    try:
        request_query = notification_reminder.objects.filter(request_id = id)
        request_query.delete()
    except:
        Result.code = "Error"

    return Result