import datetime
from django.http import HttpRequest
from app.models import *
from KmuttSearchEngine.Query import *


class Result:
    code = ''
    context = {}
    query = ''


def request_update(request, operation):
    current_time = datetime.datetime.now().replace(microsecond=0)
    if request.method == "POST":
        if (request.POST.get('question') or request.POST.get('answer')) or (request.POST.get('question_en')
            or request.POST.get('answer_en')) and request.POST.get('department_id') and request.POST.get('remark'):

            if operation == 'update':
                saverecord = QArequest()
                saverecord.request_type = "Add"
            elif operation == 'saveedit':
                saverecord = QArequest_edit.objects.get(
                    request_id=request.POST.get('request_id'))
                saverecord.request_type = request.POST.get('request_type')
            elif operation == 'editquestion':
                saverecord = QArequest()
                saverecord.request_type = "Edit"
                saverecord.question_id = request.POST.get('question_id')

            saverecord.question = request.POST.get('question')
            saverecord.answer = request.POST.get('answer')
            saverecord.question_en = request.POST.get('question_en')
            saverecord.answer_en = request.POST.get('answer_en')
            saverecord.user_id = request.user.id
            saverecord.status_id = '1'
            saverecord.department_id = request.POST.get('department_id')
            saverecord.remark = request.POST.get('remark')
            saverecord.created_date = current_time
            saverecord.created_time = current_time
            saverecord.updated_date = current_time
            saverecord.updated_time = current_time
            saverecord.updated_by = request.user.id
            #saverecord.question_id = None
            saverecord.save()

        Result.code = 200

    return Result


def request_delete(request, id):
    try:
        query = QArequest.objects.get(request_id=id)
        query.delete()
    except:
        query = "Error"

    return query


def admin_reject(request, id, reject_reason, admin_id):
    try:
        current_time = datetime.datetime.now().replace(microsecond=0)
        saverecord = QArequest_edit.objects.get(request_id=id)
        saverecord.status_id = '3'
        saverecord.updated_by = admin_id
        saverecord.rejected_date = current_time
        saverecord.rejected_time = current_time
        saverecord.updated_date = current_time
        saverecord.updated_time = current_time
        saverecord.rejected_by = admin_id
        saverecord.rejected_remark = reject_reason
        saverecord.save()
        Result.code = 200
    except:
        Result.code = 300

    print(Result.code)
    return Result


def admin_approve(request, admin_id, id):

    try:
        current_time = datetime.datetime.now().replace(microsecond=0)
        if request.method == "POST":
            if (request.POST.get('question') and request.POST.get('answer')) or (request.POST.get('question_en') 
            and request.POST.get('answer_en')) and request.POST.get('department_id') and request.POST.get('remark'):

                if request.POST.get('request_type') == "Add":
                    saverecord = questionanswer()
                    saverecord.view_count = 1
                elif request.POST.get('request_type') == "Edit":
                    saverecord = questionanswer.objects.get(
                    id=request.POST.get('question_id'))

                updaterecord = QArequest_edit.objects.get(request_id= id)
                updaterecord.status_id = '2'
                updaterecord.updated_date = current_time
                updaterecord.updated_time = current_time
                updaterecord.updated_by = admin_id
                saverecord.question = request.POST.get('question')
                saverecord.answer = request.POST.get('answer')
                saverecord.question_en = request.POST.get('question_en')
                saverecord.answer_en = request.POST.get('answer_en')
                saverecord.created_by = admin_id
                saverecord.status = True
                saverecord.department_id = request.POST.get('department_id')
                saverecord.remark = request.POST.get('remark')
                saverecord.created_date = current_time
                saverecord.created_time = current_time
                saverecord.updated_date = current_time
                saverecord.updated_time = current_time
                saverecord.updated_by = admin_id
                #saverecord.question_id = None
                saverecord.save()
                updaterecord.save()

            Result.code = 200
    except:
        Result.code = "Error"

    return Result
