from app.models import *
from KmuttSearchEngine.Query import *
from django.http import JsonResponse

def get_notification(request):

    if request.method == "POST":
        query = queryDb_request()

        for count, id  in enumerate(query.user_id):
            user_query = userinfo.objects.get(id=id)
            query.user_id[count] = user_query.username

        length = len(query.request_id)
        return JsonResponse({'user_id':query.user_id,'question':query.question,'type':query.request_type,'length':length},safe=False)
    else:
        return JsonResponse("Error",safe=False)