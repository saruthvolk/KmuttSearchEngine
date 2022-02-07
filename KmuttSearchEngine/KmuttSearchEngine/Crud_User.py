import datetime
from django.http import HttpRequest
from app.models import *
from KmuttSearchEngine.Query import *


class Result:
  code = ''
  message = ''
  query = ''

def update_status_User(request,id):

    query = userinfo.objects.filter(id=id)

    for user in query:
        user.status = False
        user.save()

    Result.code = 200
    Result.query = queryDb_User_All()

    return Result
