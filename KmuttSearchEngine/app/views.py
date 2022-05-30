"""
Definition of views.
"""
import codecs
from pyexpat.errors import messages
import oskut
import os
import datetime
import re
from html.parser import HTMLParser
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from torch import result_type
from KmuttSearchEngine.SearchEngine import searchengine
from KmuttSearchEngine.SearchEngine import train_dictionary
from KmuttSearchEngine.Crud_QA import *
from django.core.exceptions import PermissionDenied
from KmuttSearchEngine.Crud_User import *
from KmuttSearchEngine.Crud_Request import *
from KmuttSearchEngine.Crud_notification import *
from KmuttSearchEngine.Crud_Department import *
from KmuttSearchEngine.Crud_search import *
from KmuttSearchEngine.Query import *
from app.models import questionanswer, userinfo, QArequest
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.utils.translation import gettext as _
import json
import csv
import xlwt

class Search_result:
    Retry = 0
    Correct = None
    code = ''
    query = ''
    percentage = ''
    search = ''
    ans = ''

    oskut.load_model(engine='deepcut')
    tokenized = oskut.OSKut("Process", k=1)


error_Message = _("There was something wrong while processing your recent request, Please try again or contact Administrator")

@login_required(login_url='/login')
def home(request):
    """Renders the home page."""

    assert isinstance(request, HttpRequest)

    query = queryDb_QA()
    question = query.question
    json_question = json.dumps(question)

    feature_question = list(
        questionanswer.objects.all().order_by('view_count').reverse())[:5]

    return render(
        request,
        'app/index.html',
        {
            'title': 'Home Page',
            'question': json_question,
            'feature_question': feature_question
            #'year':datetime.now().year,#
        }
    )


@login_required(login_url='/login')
def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title': 'Contact',
            'message': 'Your contact page.',
            'year': datetime.now().year,
        }
    )


@login_required(login_url='/login')
def train_dict(request):

    assert isinstance(request, HttpRequest)

    query = queryDb_QA()
    for answer in query.answer:
        (query.question).append(answer)

    result = train_dictionary(query.question)

    if result.code == 200:
        return render(request, 'app/index.html')
    else:
        message = 'Done'
        return render(request, 'app/index.html', {'message': 'Done'})


@login_required(login_url='/login')
def search(request):

    assert isinstance(request, HttpRequest)

    try:
        search = request.POST.get('search')
        result_seach_history = create_search_history(request, search)
        query = queryDb_QA()
        question = query.question
        json_question = json.dumps(question)

        if result_seach_history == "Error":
            return render(request, 'app/index.html')

        page = request.GET.get('page', 1)

        if page == 1:
            query = queryDb_QA()
            result = searchengine(search, query)
            Search_result.search = search
            Search_result.query = result.query
            Search_result.Correct = result.Correct
            Search_result.percentage = result.percentage

        paginator = Paginator(Search_result.query, 10)
        paginator1 = Paginator(Search_result.percentage, 10)

        try:
            query1 = paginator.page(page)
            query2 = paginator1.page(page)

        except PageNotAnInteger:
            query1 = paginator.page(1)
            query2 = paginator1.page(1)

        except EmptyPage:
            query1 = paginator.page(paginator.num_pages)
            query2 = paginator1.page(paginator1.num_pages)

        if search:
            pre_search = search
        else:
            pre_search = Search_result.search

        if Search_result.Correct is not None:
            check = 1
            return render(request, 'app/search.html', {'Correct': Search_result.Correct, 'Question': pre_search, 
            'query': query1, 'Percentage': query2,'question':json_question})
        else:
            check = 0
            return render(request, 'app/search.html', {'Question': pre_search, 'query': query1, 'Question': pre_search, 
            'Percentage': query2, 'question':json_question})
    except:
        messages.error(request, _(error_Message))
        return redirect('home')


@login_required(login_url='/login')
def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title': 'About',
            'message': 'Your application description page.',
            'year': datetime.now().year,
        }
    )


@login_required(login_url='/login')
def question(request, id):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)

    #================ Update view count ==================#
    result = questionanswer.objects.get(id=id)
    result.view_count = result.view_count+1
    result.save(update_fields=["view_count"])

    #================ Query ==================#
    try:
        result = questionanswer.objects.get(id=id)
        result_create_view = create_view_history(request,id)
        query_view = view_view_history(request,request.user.id)[:5]
    except:
        result = "Error"
    
    if (result != "Error"):
        return render(request,'app/question.html',{'query': result, 'recent_view': query_view})
    else:
        return redirect('home')

@login_required(login_url='/login')
def Admin(request):
    
    if request.user.role_code != 1:
        raise PermissionDenied()

    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/Admin.html',
        {
            'title': 'Admin Panel',
        }
    )


@csrf_exempt
def upload_image(request):
    if request.method == "POST":
        file_obj = request.FILES['file']
        file_name_suffix = file_obj.name.split(".")[-1]
        if file_name_suffix not in ["jpg", "png", "gif", "jpeg", ]:
            return JsonResponse({"message": "Wrong file format"})

        upload_time = timezone.now()
        path = os.path.join(
            settings.MEDIA_ROOT,
            'static',
            'img',
            str(upload_time.year),
            str(upload_time.month),
            str(upload_time.day)
        )
        # If there is no such path, create
        if not os.path.exists(path):
            os.makedirs(path)

        file_path = os.path.join(path, file_obj.name)

        file_url = f'/static/img/{upload_time.year}/{upload_time.month}/{upload_time.day}/{file_obj.name}'

        if os.path.exists(file_path):
            return JsonResponse({
                "message": "file already exist",
                'location': file_url
            })

        with open(file_path, 'wb+') as f:
            for chunk in file_obj.chunks():
                f.write(chunk)

        return JsonResponse({
            'message': 'Image uploaded successfully',
            'location': file_url
        })
    return JsonResponse({'detail': "Wrong request"})

def user_question_view(request, operation):
    
    user_id = request.user.id
    query = queryDb_QA()
    question = query.question
    json_question = json.dumps(question)
    query_department = queryDb_department()
    query_view = view_view_history(request,user_id)[:5]
    department_id_list = [dept.department_id for dept in query_department]

    if operation == "question":
        query_question = queryDb_QA_All()
    elif operation == "faq":
        query_question = queryDb_QA_All_FAQ()
    elif operation == "recent_update":
        query_question = queryDb_QA_All_Recent()
    elif (operation in dept.department_id for dept in query_department):
        query_question = queryDb_QA_Dept(operation)

    page = request.GET.get('page', 1)
    if page == 1:
        if operation == "question":
            query_question = queryDb_QA_All()
        elif operation == "faq":
            query_question = queryDb_QA_All_FAQ()
        elif operation == "recent_update":
            query_question = queryDb_QA_All_Recent()
        elif (operation in dept.department_id for dept in query_department):
            query_question = queryDb_QA_Dept(operation)

    paginator = Paginator(query_question, 7)
    try:
        query = paginator.page(page)
    except PageNotAnInteger:
        query = paginator.page(1)
    except EmptyPage:
        query = paginator.page(paginator.num_pages)
    if query != "Error":
        return render(request, 'app/user_question_view.html',{'question':json_question,'query':query,
        'operation':operation,'department':query_department,'recent_view':query_view, 'department_id':department_id_list})
    else:
        return render(request, 'app/index.html')

def Crud_QA(request, operation, id):

    if request.user.role_code != 1:
        raise PermissionDenied()

    if operation == "Add":
        result = Add_QA(request)
        department = queryDb_department()
        if result.code == 200:
            messages.info(request, _("Successfully added the question(s)"),extra_tags='Add')
            return redirect('Crud_QA', operation = "View",id ='0')
        else:
            return render(request, 'app/CRUDquestion.html', {'department': department})

    elif operation == "View":

        question_all = queryDb_QA_All()
        page = request.GET.get('page', 1)
        if page == 1:
            question_all = queryDb_QA_All()
        paginator = Paginator(question_all, 5)
        try:
            query1 = paginator.page(page)
        except PageNotAnInteger:
            query1 = paginator.page(1)
        except EmptyPage:
            query1 = paginator.page(paginator.num_pages)
        if question_all is "Error":
            messages.error(request, _(error_Message))
            return redirect('home')
        else:
            return render(request, 'app/Viewquestion.html', {'query': query1})

    elif operation == "Remove":

        if request.method == 'POST':
            id = request.POST.getlist('id_check')

        result = Remove_QA(request, id)

        if result.code == 200:
            messages.info(request, _("Successfully removed the question(s)"))
            return redirect('Crud_QA', operation = "View" , id='0')
        else:
            messages.error(request, _(error_Message))
            return redirect('Crud_QA', operation = "View",id ='0')

    elif operation == "Edit":
        department = queryDb_department()
        if request.method == 'POST':
            id = request.POST.getlist('id_check')

        result = Edit_QA(request, id)

        if result.code == 200:
            json_id = json.dumps(id)
            return render(request, 'app/Editquestion.html', {'query': result.query, 'id_list': json_id, 'department': department})
        else:
            messages.error(request, _(error_Message))
            return redirect('Crud_QA', operation = "View",id ='0')

    elif operation == "Update":

        if request.method == 'POST':
            id = request.POST.getlist('id_check')

        result = Update_QA(request, id)

        if result.code == 200:
            messages.info(request, _("Successfully edited the question(s)"))
            return redirect('Crud_QA', operation = "View" , id='0')
        else:
            messages.error(request, _(error_Message))
            return redirect('Crud_QA', operation = "View",id ='0')


def signin(request):

    if request.method == 'POST':
        username1 = request.POST['username']
        password1 = request.POST['password']
        user = authenticate(username=username1, password=password1)
        if user is not None:
            login(request, user)
            if request.user.role_code is 1:
                return render(request, 'app/Admin.html')
            else:
                return redirect('/')
        else:
            context = {"error": "Invalid Username or Password"}
            return render(request, 'app/login.html', context)
    else:
        return render(request, 'app/login.html')


def signout(request):
    logout(request)
    return redirect('signin')


def usermanagement(request, operation):

    if request.user.role_code != 1:
        raise PermissionDenied()

    if operation == 'status':
        print(operation)
        if request.method == 'POST':
            id = request.POST.get('userid')
            result = update_status_User(request, id)
            if result.code is 200:
                for user in result.query:
                    if (user.is_active == False):
                        messages.info(request, _("Successfully suspended "  + str(user.username)  + " account's."))
                    elif(user.is_active == True):
                        messages.info(request, _("Successfully unsuspended "+str(user.username)+"  account's."))
                return redirect('user')
            else:
                messages.error(request, _(error_Message))
                return redirect('user')

    elif operation == 'update':
        if request.method == 'POST':
            id = request.POST.get('userid_confirm')
            result = update_user_profile(request, id)
            if result.code is 200:
                for user in result.query:
                    messages.info(request, _("Successfully update "+str(user.username)+"  profile's."))
                return redirect('user')
            else:
                messages.error(request, _(error_Message))
                return redirect('user')

    else:
        messages.error(request, _(error_Message))
        return redirect('user')


def user(request):

    if request.user.role_code != 1:
        raise PermissionDenied()

    assert isinstance(request, HttpRequest)
    user_info = queryDb_User_All()

    page = request.GET.get('page', 1)

    if page == 1:
        user_info = queryDb_User_All()

    paginator = Paginator(user_info, 5)

    try:
        query1 = paginator.page(page)

    except PageNotAnInteger:
        query1 = paginator.page(1)

    except EmptyPage:
        query1 = paginator.page(paginator.num_pages)

    return render(
        request,
        'app/Usermanagement.html',
        {
            'title': 'User Management',
            'message': 'Your application description page.',
            'user': user_info,
            'query': query1
        }
    )


def profile(request, operation):

    assert isinstance(request, HttpRequest)

    user_query = queryDb_User(request.user.id)

    if operation == 'view':
        return render(request, 'app/profile.html', {'title': 'My Profile', 'query': user_query, 'operation': operation})
    elif operation == 'edit':
        return render(request, 'app/profile.html',{'title': 'My Profile', 'query': user_query, 'operation': operation})
    elif operation == 'update':
        if request.method == 'POST':
            result = edit_user_profile(request)

            print(result.context)
            
            if result.code is 200:
                messages.info(request, _("Your profile has been successfully updated."))
                return redirect('profile', operation='view')

            elif result.context != None:
                messages.error(request, _(result.context))
                return redirect('profile', operation='view')

            else:
                operation = 'view'
                messages.error(request, _(error_Message))
                return render(request, 'app/profile.html', {'title': 'My Profile', 'query': user_query, 'operation': operation})
        else:
            operation = 'view'
            messages.error(request, _(error_Message))
            return render(request, 'app/profile.html', {'title': 'My Profile', 'query': user_query, 'operation': operation})
    else:
        messages.error(request, _(error_Message))
        return render(request, 'app/profile.html', {'title': 'My Profile', 'query': user_query, 'operation': operation})


def register(request):

    if request.user.role_code != 1:
        raise PermissionDenied()

    current_time = datetime.datetime.now().replace(microsecond=0)
    validate_eng = re.compile("^[a-zA-Z]+$")
    validate_thai = re.compile("^[\u0E00-\u0E7F]+$")

    if request.method == "POST":

        if (request.POST.get('username') and request.POST.get('password') and request.POST.get('first_name') and request.POST.get('last_name') and request.POST.get('email') and
                request.POST.get('date_of_birth') and request.POST.get('gender') and request.POST.get('phone_no')):
            saverecord = userinfo()
            password1 = request.POST.get('password')
            username1 = request.POST.get('username')
            email1 = request.POST.get('email')
            firstname = request.POST.get('first_name')
            lastname = request.POST.get('last_name')
            phone_no = request.POST.get('phone_no')
            department = request.POST.get('department')

            print(len(phone_no))

            if userinfo.objects.filter(username=username1).exists():
                context = {"error": _("Username already exist.")}
                return render(request, 'app/register.html', context)
            elif not username1.isalpha():
                context = {"error": _("Username can contain only alphabets.")}
                return render(request, 'app/register.html', context)
            elif not re.fullmatch(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$', password1):
                context = {"error": _("Invalid password format")}
                return render(request, 'app/register.html', context)
            elif not validate_eng.search(firstname) and not validate_thai.search(firstname):
                context = {"error": _("Firstname can contain only alphabets.")}
                return render(request, 'app/register.html', context)
            elif not validate_eng.search(lastname) and not validate_thai.search(lastname):
                context = {"error": _("Lastname can contain only alphabets.")}
                return render(request, 'app/register.html', context)
            elif not phone_no.isdecimal() or int(len(phone_no)) is not 10:
                context = {"error": _("Invalid phone number")}
                return render(request, 'app/register.html', context)

            if userinfo.objects.filter(email=email1).exists():
                context = {"error": "Email already exist"}
                return render(request, 'app/register.html', context)
            try:
                img = request.FILES['avatar']
                print(img)
                img_extension = os.path.splitext(img.name)[1]
                print(img_extension)
                user_folder = 'static/img/Profile_Pic/' + \
                    str(request.POST.get('username'))
                if not os.path.exists(user_folder):
                    os.mkdir(user_folder)
                destination = open('static/img/Profile_Pic/'+str(request.POST.get(
                    'username'))+'/'+str(request.POST.get('username'))+str(img_extension), 'wb+')
                path = ('img/Profile_Pic/'+str(request.POST.get('username'))+'/'+str(request.POST.get('username'))+str(img_extension))
                for chunk in img.chunks():
                    print('1')
                    destination.write(chunk)
                destination.close()
            except:
                path = "img/user.png"

            try:
                saverecord.path_profile_pic = path
                saverecord.username = request.POST.get('username')
                saverecord.gender = request.POST.get('gender')
                saverecord.date_of_birth = request.POST.get('date_of_birth')
                saverecord.phone_no = request.POST.get('phone_no')
                saverecord.password = make_password(password1)
                saverecord.first_name = request.POST.get('first_name')
                saverecord.last_name = request.POST.get('last_name')
                saverecord.email = request.POST.get('email')
                saverecord.created_by = request.user.id
                saverecord.updated_by = request.user.id
                saverecord.suspended_by = None
                saverecord.is_active = True
                saverecord.updated_date = current_time
                saverecord.updated_time = current_time
                saverecord.created_date = current_time
                saverecord.created_time = current_time
                saverecord.last_login = current_time
                saverecord.role_code = department
                saverecord.save()

                messages.info(request, _("You has been successfully registered to the website"))
                return redirect('user')
            except:
                messages.error(request, _(error_Message))
                return redirect('user')
    else:
        return render(request, 'app/register.html')

def requestmanagement(request, operation):

    if operation == 'add':
        department = queryDb_department()
        return render(request, 'app/requestadd.html', {'department': department})

    elif operation == 'view':
        request_id = request.POST.get('request_id')
        result_update = update_reminder(request, request_id)
        result =  queryDb_onerequest(request_id)
        department = queryDb_department()
        user_query = queryDb_User(request.user.id)
        if (result or result_update or department or user_query) == "Error":
            messages.error(request, _(error_Message))
            return redirect('home')
        else:
            return render(request, 'app/view_request.html',{'query': user_query, 'request_data': result,'department': department,'opertaion':operation})

    elif operation == 'view_user':
        request_info = queryDb_Request_user(request.user.id)
        user_query = queryDb_User(request.user.id)
        page = request.GET.get('page', 1)
        if page == 1:
            request_info = queryDb_Request_user(request.user.id)
        paginator = Paginator(request_info, 7)
        try:
            query1 = paginator.page(page)
        except PageNotAnInteger:
            query1 = paginator.page(1)
        except EmptyPage:
            query1 = paginator.page(paginator.num_pages)
        if (request_info or user_query) == "Error":
            messages.error(request, _(error_Message))
            return redirect('home')
        else:
            return render(request, 'app/request_user.html', {'user_info': user_query, 'query': query1 })
        
    elif operation == 'edit':
        request_id = request.POST.get('request_id')
        result =  queryDb_onerequest(request_id)
        department = queryDb_department()
        user_query = queryDb_User(request.user.id)

        if result is "Error":
            messages.error(request, _(error_Message))
            return redirect('request', operation='view_user')
        else:
            return render(request, 'app/editrequest.html',{'query': user_query, 'request_data': result,'department': department})

    elif operation == 'update':
        result = request_update(request, operation)
        result_reminder = create_reminder(operation,None)
        if (result.code == 200) and (result_reminder.code == 200):
            messages.info(request, _("Your request has been successfully created, admin will review it shortly."))
            return redirect('request', operation='view_user',)
        else:
            messages.error(request, _(error_Message))
            return redirect('request', operation='view_user')

    elif operation == 'saveedit':
        result = request_update(request, operation)
        request_id = request.POST.get('request_id')
        result_reminder = create_reminder(operation,request_id)

        if (result.code == 200) and (result_reminder.code == 200):
            messages.info(request, _("Your request has been successfully edited."))
            return redirect('request', operation='view_user')
        else:
            messages.error(request, _(error_Message))
            return redirect('request', operation='view_user')

    elif operation == 'editquestion':
        result = request_update(request, operation)
        result_reminder = create_reminder(operation,None)
        if (result.code or result_reminder.code) == "Error":
            messages.error(request, _(error_Message))
            return redirect('request', operation='view_user')
        else:
            messages.info(request, _("Your request has been successfully created, admin will review it shortly."))
            return redirect('request', operation='view_user')

    elif operation == 'delete':
        if request.method == "POST":
            id = request.POST.get('request_id')
            result_delete = request_delete(request,id)
            result_noti_delete = delete_reminder(request,id)
            if (result_delete or result_noti_delete) is "Error":
                messages.error(request, _(error_Message))
                return redirect('request', operation='view_user')
            else:
                messages.info(request, _("Your request has been successfully deleted."))
                return redirect('request', operation='view_user')

        if result is "Error":
            messages.error(request, _(error_Message))
            return redirect('request', operation='view_user')

    elif operation == 'request_edit':
        question_id = request.POST.get('question_id')
        result = queryDb_onequestion(question_id)
        department = queryDb_department()
        user_query = queryDb_User(request.user.id)

        if (result or department or user_query) == "Error":
            messages.error(request, _(error_Message))
            return redirect('home')
        else:
            return render(request, 'app/requesteditquestion.html',{'query': user_query, 'question_data': result,'department': department})
            
    else:
        messages.error(request, _(error_Message))
        return redirect('home')

def request_admin(request, operation):

    if request.user.role_code != 1:
        raise PermissionDenied()

    if operation == 'view':
        query_request = queryDb_request_all()

        page = request.GET.get('page', 1)
        if page == 1:
            query_request = queryDb_request_all()
        paginator1 = Paginator(query_request, 7)
        try:
            query1 = paginator1.page(page)
        except PageNotAnInteger:
            query1 = paginator1.page(1)
        except EmptyPage:
            query1 = paginator1.page(paginator1.num_pages)

        if query_request is "Error":
            messages.error(request, _(error_Message))
            return redirect('home')
        else:
            return render(request, 'app/request_admin.html',{'query': query1})
        
    elif operation == 'reject':

        request_id = request.POST.get('request_id')
        reject_reason = request.POST.get('reject_reason')
        admin_id = request.user.id
        result = admin_reject(request,request_id,reject_reason,admin_id)
        if result.code == 200:
            result_reminder = create_reminder(operation,request_id)
            if result_reminder.code is "Error":
                return redirect('home')
            else:
                messages.info(request, _("Successfully rejected the request"))
                return redirect('request_admin', operation = "view")
        else:
            return redirect('home')
    
    elif operation == 'approve':

        id = request.POST.get('request_id')
        admin_id = request.user.id
        result_update = update_reminder(request, id)
        result = queryDb_onerequest(id)
        department = queryDb_department()
        if (result and department and result_update) is "Error":
            return redirect('home')
        else:
            return render(request, 'app/admin_approve.html',{ 'request_data': result,'department': department})

    elif operation == 'saveapprove':
        admin_id = request.user.id
        request_id = request.POST.get('request_id')
        result = admin_approve(request, admin_id, request_id)
        if result.code == 200:
            result_reminder = create_reminder(operation,request_id)
            messages.info(request, _("Successfully approved the request"))
            return redirect('request_admin', operation='view')
        else:
            messages.error(request, _(error_Message))
            return redirect('request_admin', operation='view')

def department_management (request,operation):
    
    if request.user.role_code != 1:
        raise PermissionDenied()

    if operation == "View":

        query_department = queryDb_department()
        department_question = queryDb_department_question()

        page = request.GET.get('page', 1)
        if page == 1:
            query_department = queryDb_department()
            department_question = queryDb_department_question()

        paginator = Paginator(query_department, 7)
        paginator1 = Paginator(department_question, 7)
        
        try:
            result = paginator.page(page)
            department_question = paginator1.page(page)
        except PageNotAnInteger:
            result = paginator.page(1)
            department_question = paginator1.page(1)
        except EmptyPage:
            result = paginator.page(paginator.num_pages)
            department_question = paginator1.page(paginator.num_pages)

        if result != "Error":
           return render(request, 'app/department_admin.html',{ 'departments': result, 'departments_question':department_question})
        else:
            messages.error(request, _(error_Message))
            return redirect('Admin')

    elif operation == "update":
        result = update_department(request)
        if result == "Error":
            messages.error(request, _(error_Message))
            return redirect('department_admin',operation="View")
        else:
            messages.info(request, _("Successfully updated department name"))
            return redirect('department_admin',operation="View")
            
    elif operation == "delete":
        result = delete_department(request)
        if result == "Error":
            messages.error(request, _(error_Message))
            return redirect('department_admin',operation="View")
        else:
            messages.info(request, _("Successfully removed department"))
            return redirect('department_admin',operation="View")

    elif operation == "Add":
        result = save_department(request)
        if result == "Error":
            messages.error(request, _(error_Message))
            return redirect('department_admin',operation="View")
        else:
            messages.info(request, _("Successfully added department"))
            return redirect('department_admin',operation="View")


def history_user(request,operation):

    if operation == "search":
        user_id = request.user.id
        query_search = view_search_history(request,user_id)
        user_query = queryDb_User(request.user.id)
        
        page = request.GET.get('page', 1)

        if page == 1:
            query_search = view_search_history(request,user_id)
        paginator = Paginator(query_search, 7)
        try:
            query = paginator.page(page)
        except PageNotAnInteger:
            query = paginator.page(1)
        except EmptyPage:
            query = paginator.page(paginator.num_pages)

        if (query != "Error"):
            return render(request, 'app/search_history.html',{ 'query': query, 'user_info':user_query})
        else:
            return redirect('home')
    
    elif operation == "view":

        user_id = request.user.id
        query_view = view_view_history(request,user_id)
        user_query = queryDb_User(request.user.id)
        
        page = request.GET.get('page', 1)

        if page == 1:
            query_view = view_view_history(request,user_id)
        paginator = Paginator((query_view), 7)
        try:
            query = paginator.page(page)
        except PageNotAnInteger:
            query = paginator.page(1)
        except EmptyPage:
            query = paginator.page(paginator.num_pages)

        if (query != "Error"):
            return render(request, 'app/view_history.html',{ 'query': query, 'user_info':user_query})
        else:
            return redirect('home')

class HTMLFilter(HTMLParser):
    text = ""
    def handle_data(self, data):
        self.text += data

def export_excel(request,action):

    rows = []
    if action == 'request':
        response = HttpResponse(content_type='text/csv')
        response ['Content-Disposition'] = 'attachment; filename= User_Request_'+ \
            str(datetime.datetime.now())+'.xls'
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Users Request Data')
        row_num = 0 
        font_style = xlwt.XFStyle()
        font_style.font.bold = True
        columns = ['Request ID','Type','Request By','Status','Created date','Last updated', 'Question TH','Answer TH','Question EN','Answer EN','Remark']
        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)
            ws.col(0).width = 2000
            ws.col(1).width = 2000
            ws.col(2).width = 6000
            ws.col(3).width = 4000
            ws.col(4).width = 3500
            ws.col(5).width = 3500
            ws.col(6).width = 9000
            ws.col(7).width = 9000
            ws.col(8).width = 9000
            ws.col(9).width = 9000
            ws.col(10).width = 9000

        font_style = xlwt.XFStyle()
        font_style.alignment.wrap = 1

        query_request = queryDb_request_all()

        for request_info in query_request:
            if request_info.status_id == 1:
                request_info.status_id = _("Waiting for approval")
            elif request_info.status_id == 2:
                request_info.status_id = _("Approved")
            elif request_info.status_id == 2:
                request_info.status_id = _("Rejected")

            f = HTMLFilter()
            f.feed(request_info.answer) 
            request_info.answer = f.text

            f = HTMLFilter()
            f.feed(request_info.answer_en) 
            request_info.answer_en = f.text

            temp =  [request_info.request_id,request_info.request_type,request_info.user.first_name + " " + request_info.user.last_name,request_info.status_id, str(request_info.created_date),
            str(request_info.updated_date),request_info.question,request_info.answer,request_info.question_en,request_info.answer_en,request_info.remark]
            rows.append(temp)
        
        for row in rows:
            row_num += 1
            for col_num in range(len(row)):
                ws.write(row_num, col_num, row[col_num], font_style)

        wb.save(response)
        return response
    
    elif action == 'user_info':
        response = HttpResponse(content_type='text/csv')
        response ['Content-Disposition'] = 'attachment; filename= Userinfo_'+ \
            str(datetime.datetime.now())+'.xls'
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Users Request Data')
        row_num = 0 
        font_style = xlwt.XFStyle()
        font_style.font.bold = True
        columns = ['User ID','First Name','Last Name','Status','Role','Date of Birth','Gender','Email', 'Phone Number','Last Login','Created Date','Created Time',
        'Created By','Updated Date','Updated Time','Update By','Suspended Date','Suspended Time','Suspended By']
        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)
            ws.col(0).width = 1900
            ws.col(1).width = 3000
            ws.col(2).width = 4200
            ws.col(3).width = 2000
            ws.col(4).width = 3000
            ws.col(5).width = 3800
            ws.col(6).width = 3000
            ws.col(7).width = 8000
            ws.col(8).width = 3800
            ws.col(9).width = 3800
            ws.col(10).width = 3800
            ws.col(11).width = 3800
            ws.col(12).width = 3800
            ws.col(13).width = 3800
            ws.col(14).width = 3800
            ws.col(15).width = 3800
            ws.col(16).width = 3800
            ws.col(17).width = 3800
            ws.col(18).width = 3800

        font_style = xlwt.XFStyle()
        font_style.alignment.wrap = 1

        user_info = queryDb_User_All()

        for user_data in user_info:

            if user_data.is_active is False:
                user_data.is_active = 'Suspended'
            elif user_data.is_active is True:
                user_data.is_active = 'Active'
            
            temp =  [user_data.id,user_data.first_name,user_data.last_name,user_data.is_active,user_data.role_code,str(user_data.date_of_birth),user_data.gender,str(user_data.email),"0"+ str(user_data.phone_no),
            str(user_data.last_login),str(user_data.created_date),str(user_data.created_time),str(user_data.created_by),str(user_data.updated_date),str(user_data.updated_time),str(user_data.updated_by),
            str(user_data.suspended_date),str(user_data.suspended_time),str(user_data.suspended_by)]
            rows.append(temp)

        for row in rows:
            row_num += 1
            for col_num in range(len(row)):
                ws.write(row_num, col_num, row[col_num], font_style)

        wb.save(response)
        return response

    elif action == "question":
        response = HttpResponse(content_type='text/csv')
        response ['Content-Disposition'] = 'attachment; filename= QA_'+ \
            str(datetime.datetime.now())+'.xls'
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('QA_data')
        row_num = 0 
        font_style = xlwt.XFStyle()
        font_style.font.bold = True
        columns = ['Quesiton ID','Department','Question TH','Answer TH','Question EN','Answer EN','Created date','Created time', 'Created By','Updated Date','Updated Time','Updated By','status','View Count']
        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)
            ws.col(0).width = 3000
            ws.col(1).width = 4000
            ws.col(2).width = 9000
            ws.col(3).width = 9000
            ws.col(4).width = 9000
            ws.col(5).width = 9000
            ws.col(6).width = 3500
            ws.col(7).width = 3500
            ws.col(8).width = 3500
            ws.col(9).width = 3500
            ws.col(10).width = 3500
            ws.col(11).width = 3500
            ws.col(12).width = 3500
            ws.col(13).width = 3500
            ws.col(14).width = 3500

        font_style = xlwt.XFStyle()
        font_style.alignment.wrap = 1

        query_request = queryDb_QA_All()

        for QA_info in query_request:
            department_info = department.objects.get(department_id=QA_info.department_id)
            user_created_by = userinfo.objects.get(id=int(QA_info.created_by))
            user_updated_by = userinfo.objects.get(id=int(QA_info.updated_by))

            QA_info.created_by = user_created_by.username
            QA_info.updated_by = user_updated_by.username
            QA_info.department_id = department_info.department_name

            if QA_info.status == 1:
                QA_info.status = _("Active")

            f = HTMLFilter()
            f.feed(QA_info.answer) 
            QA_info.answer = f.text

            f = HTMLFilter()
            f.feed(QA_info.answer_en) 
            QA_info.answer_en = f.text

            temp =  [QA_info.id,QA_info.department_id,QA_info.question,QA_info.answer,QA_info.question_en,QA_info.answer_en,str(QA_info.created_date),str(QA_info.created_time),QA_info.created_by,
            str(QA_info.updated_date),str(QA_info.updated_time),QA_info.updated_by,QA_info.status,QA_info.view_count]
            rows.append(temp)
        
        for row in rows:
            row_num += 1
            for col_num in range(len(row)):
                ws.write(row_num, col_num, row[col_num], font_style)

        wb.save(response)
        return response
    
    else:
        return redirect('home')



