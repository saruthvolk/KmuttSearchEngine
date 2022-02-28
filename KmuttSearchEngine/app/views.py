"""
Definition of views.
"""
from pyexpat.errors import messages
import oskut
import os
import datetime
import re
from django.shortcuts import render, redirect
from django.http import HttpRequest
from KmuttSearchEngine.SearchEngine import searchengine
from KmuttSearchEngine.SearchEngine import train_dictionary
from KmuttSearchEngine.Crud_QA import *
from KmuttSearchEngine.Crud_User import *
from KmuttSearchEngine.Crud_Request import *
from KmuttSearchEngine.Crud_notification import *
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

    print("Creating Dict")
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

    search = request.POST.get('search')

    page = request.GET.get('page', 1)

    if page == 1:
        query = queryDb_QA()
        result = searchengine(search, query)
        Search_result.search = search
        Search_result.query = result.query
        Search_result.Correct = result.Correct
        Search_result.percentage = result.percentage

    length = Search_result.percentage
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
        return render(request, 'app/search.html', {'Correct': Search_result.Correct, 'Question': pre_search, 'query': query1, 'Percentage': query2, 'length': length})
    else:
        check = 0
        return render(request, 'app/search.html', {'Question': pre_search, 'query': query1, 'Question': pre_search, 'Percentage': query2, 'length': length})


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
    result = questionanswer.objects.get(id=id)
    return render(
        request,
        'app/question.html',
        {
            'title': 'Question Detail',
            'query': result,
        }
    )


@login_required(login_url='/login')
def Admin(request):

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


def Crud_QA(request, operation, id):

    if operation == "Add":
        result = Add_QA(request)
        department = queryDb_department()
        if result.code == 200:
            return render(request, 'app/index.html')
        else:
            return render(request, 'app/CRUDquestion.html', {'department': department})

    elif operation == "View":

        result = View_QA(request, id)

        return render(request, 'app/Viewquestion.html', {'query': result.query})

    elif operation == "Remove":

        if request.method == 'POST':
            id = request.POST.getlist('id_check')

        result = Remove_QA(request, id)

        if result.code == 200:
            return render(request, 'app/index.html')
        else:
            return render(request, 'app/Viewquestion.html', {'query': result.query})

    elif operation == "Edit":

        if request.method == 'POST':
            id = request.POST.getlist('id_check')

        result = Edit_QA(request, id)

        if result.code == 200:
            return render(request, 'app/index.html')
        else:
            json_id = json.dumps(id)
            return render(request, 'app/Editquestion.html', {'query': result.query, 'id_list': json_id})

    elif operation == "Update":

        if request.method == 'POST':
            id = request.POST.getlist('id_check')

        result = Update_QA(request, id)

        if result.code == 200:
            return render(request, 'app/index.html')
        else:
            return render(request, 'app/Viewquestion.html', {'query': result.query})


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
                return redirect('user')

    else:
        return redirect('user')


def user(request):

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
            if result.code is 200:
                messages.info(request, _("Your profile has been successfully updated."))
                return redirect('profile', operation='view')
        else:
            operation = 'view'
            return render(request, 'app/profile.html', {'title': 'My Profile', 'query': user_query, 'operation': operation})
    else:
        return render(request, 'app/profile.html', {'title': 'My Profile', 'query': user_query, 'operation': operation})


def register(request):
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
                context = {"error": "Username already exist."}
                return render(request, 'app/register.html', context)
            elif not username1.isalpha():
                context = {"error": "Username can conatain only alphabets."}
                return render(request, 'app/register.html', context)
            elif not re.fullmatch(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$', password1):
                context = {"error": "Invalide password format"}
                return render(request, 'app/register.html', context)
            elif not validate_eng.search(firstname) and not validate_thai.search(firstname):
                context = {"error": "Firstname can conatain only alphabets."}
                return render(request, 'app/register.html', context)
            elif not validate_eng.search(lastname) and not validate_thai.search(lastname):
                context = {"error": "Lastname can conatain only alphabets."}
                return render(request, 'app/register.html', context)
            elif not phone_no.isdecimal() or int(len(phone_no)) is not 10:
                context = {"error": "Invalid phone number"}
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
                path = None

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

            return redirect('user')
        else:

            return redirect('register')
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
        if request_info is "Error":
            return redirect('home')
        else:
            return render(request, 'app/request_user.html', {'user_info': user_query, 'query': query1 })
        
    elif operation == 'edit':
        request_id = request.POST.get('request_id')
        result =  queryDb_onerequest(request_id)
        department = queryDb_department()
        user_query = queryDb_User(request.user.id)

        if result is "Error":
            return redirect('home')
        else:
            return render(request, 'app/editrequest.html',{'query': user_query, 'request_data': result,'department': department})

    elif operation == 'update':
        result = request_update(request, operation)
        result_reminder = create_reminder(operation,None)
        if (result.code and result_reminder.code) == 200 :
            messages.info(request, _("Your request has been successfully created, admin will review it shortly."))
            return redirect('request', operation='view_user',)
        else:
            return render(request, 'app/requestadd.html')

    elif operation == 'saveedit':
        result = request_update(request, operation)
        request_id = request.POST.get('request_id')
        result_reminder = create_reminder(operation,request_id)

        if result is "Error":
            return redirect('home')
        else:
            messages.info(request, _("Your request has been successfully edited."))
            return redirect('request', operation='view_user')

    elif operation == 'editquestion':
        result = request_update(request, operation)
        result_reminder = create_reminder(operation,None)
        if (result.code and result_reminder.code) == "Error":
            return redirect('home')
        else:
            return redirect('request', operation='view_user')

    elif operation == 'delete':
        if request.method == "POST":
            id = request.POST.get('request_id')
            result_delete = request_delete(request,id)
            result_noti_delete = delete_reminder(request,id)
            if (result_delete or result_noti_delete) is "Error":
                return redirect('home')
            else:
                messages.info(request, _("Your request has been successfully deleted."))
                return redirect('request', operation='view_user')

        if result is "Error":
                return redirect('home')

    elif operation == 'request_edit':
        question_id = request.POST.get('question_id')
        result = queryDb_onequestion(question_id)
        department = queryDb_department()
        user_query = queryDb_User(request.user.id)

        if result is "Error":
            return redirect('home')
        else:
            return render(request, 'app/requesteditquestion.html',{'query': user_query, 'question_data': result,'department': department})
            
    else:
        return redirect('home')

def request_admin(request, operation):

    if operation == 'view':
        query_request, QArequestDto = queryDb_request_all()
        query_user = queryDb_multi_User(QArequestDto.user_id)

        page = request.GET.get('page', 1)
        if page == 1:
            query_request, QArequestDto = queryDb_request_all()
        paginator1 = Paginator(query_request, 7)
        try:
            query1 = paginator1.page(page)
        except PageNotAnInteger:
            query1 = paginator1.page(1)
        except EmptyPage:
            query1 = paginator1.page(paginator1.num_pages)

        page = request.GET.get('page', 1)
        if page == 1:
            query_request, QArequestDto = queryDb_request_all()
            query_user = queryDb_multi_User(QArequestDto.user_id)
        paginator2 = Paginator(query_user, 7)
        try:
            query2 = paginator2.page(page)
        except PageNotAnInteger:
            query2 = paginator2.page(1)
        except EmptyPage:
            query2 = paginator2.page(paginator2.num_pages)

        if query_request is "Error":
            return redirect('home')
        else:
            return render(request, 'app/request_admin.html',{'query': query1,'query2':query2})
        
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
        result = queryDb_onerequest(id)
        department = queryDb_department()
        if (result and department) is "Error":
            return redirect('home')
        else:
            return render(request, 'app/admin_approve.html',{ 'request_data': result,'department': department})

    elif operation == 'saveapprove':
        admin_id = request.user.id
        request_id = request.POST.get('request_id')
        result = admin_approve(request, admin_id, request_id)
        if result.code == 200:
            result_reminder = create_reminder(operation,request_id)
            messages.info(request, ("Successfully approved the request"))
            return redirect('request_admin', operation='view')
        else:
            return redirect('home')