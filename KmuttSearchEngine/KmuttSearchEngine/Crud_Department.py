import datetime
from urllib import request
from django.http import HttpRequest
from app.models import *
from KmuttSearchEngine.Query import *


class Result:
    code = ''
    context = {}
    query = ''

def update_department(request):

    try:
        department_id = request.POST.get('departmentid')
        edit_department_name = request.POST.get('department_name_'+str(department_id))

        if request.POST.get('departmentid') and request.POST.get('department_name_'+str(department_id)):
            try:
                query = department.objects.get(department_id = department_id)
                query.department_name = edit_department_name
                query.save()
            except:
                query = "Error"
        else:
            query = "Error"
    except:
        query = "Error"

    return query

def delete_department(request):

    if request.POST.get('departmentid'):
        try:
            department_id = request.POST.get('departmentid')
            query = department.objects.get(department_id = department_id)
            query.delete()
        except:
            query = "Error"
    else:
        query = "Error"

    return query

def save_department(request):

    if request.POST.get('department_name'):
        try:
            saverecord = department()
            saverecord.department_name = request.POST.get('department_name')
            saverecord.save()
        except:
           Result.query = "Error" 
    else:
        Result.query = "Error"

    return Result.query
