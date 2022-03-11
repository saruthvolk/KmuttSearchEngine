import datetime
from app.models import *
from KmuttSearchEngine.Query import *


class Result:
    code = ''
    context = {}
    query = ''


def update_status_User(request, id):

    try:
        try:
            query = userinfo.objects.filter(id=id)
        except:
            Result.code = "Error"
            
        current_time = datetime.datetime.now().replace(microsecond=0)
        for user in query:

            if (user.is_active == True):
                user.is_active = False
                user.suspended_by = request.user.id
                user.suspended_date = current_time
                user.suspended_time = current_time
                user.updated_time = current_time
                user.updated_date = current_time
                user.updated_by = request.user.id
                user.save()
            else:
                user.is_active = True
                user.suspended_by = None
                user.suspended_date = None
                user.suspended_time = None
                user.updated_time = current_time
                user.updated_date = current_time
                user.updated_by = request.user.id
                user.save()

        Result.code = 200
        Result.query = queryDb_User(id)
    except:
        Result.code = "Error"

    return Result


def update_user_profile(request, id):

    try:
        current_time = datetime.datetime.now().replace(microsecond=0)
        if (request.POST.get('first_name_edit_'+str(id)) and request.POST.get('last_name_edit_'+str(id)) and request.POST.get('date_of_birth_edit_'+str(id))
                and request.POST.get('gender_edit_'+str(id)) and request.POST.get('email_edit_'+str(id)) and request.POST.get('phone_no_edit_'+str(id))):

            first_name = request.POST.get('first_name_edit_'+str(id))
            last_name = request.POST.get('last_name_edit_'+str(id))
            date_of_birth = request.POST.get('date_of_birth_edit_'+str(id))
            gender = request.POST.get('gender_edit_'+str(id))
            email = request.POST.get('email_edit_'+str(id))
            phone_no = request.POST.get('phone_no_edit_'+str(id))

            query = userinfo.objects.filter(id=id)

            for user in query:
                user.first_name = first_name
                user.last_name = last_name
                user.date_of_birth = date_of_birth
                user.gender = gender
                user.updated_by
                user.email = email
                user.phone_no = phone_no
                user.updated_date = current_time
                user.updated_time = current_time
                user.save()

            Result.code = 200
            Result.query = queryDb_User(id)
        else:
            Result.code = "Error"
            return Result
    except:
        Result.code = "Error"

    return Result


def edit_user_profile(request):

    try:
        current_time = datetime.datetime.now().replace(microsecond=0)
        if (request.POST.get('first_name_edit') and request.POST.get('last_name_edit') and request.POST.get('email_edit')
            and request.POST.get('gender_edit') and request.POST.get('date_of_birth_edit') and request.POST.get('dep_profile_edit') and request.POST.get('phone_no_edit')):

            first_name = request.POST.get('first_name_edit')
            last_name = request.POST.get('last_name_edit')
            date_of_birth = request.POST.get('date_of_birth_edit')
            gender = request.POST.get('gender_edit')
            email = request.POST.get('email_edit')
            phone_no = request.POST.get('phone_no_edit')

            query = userinfo.objects.filter(id=request.user.id)

            for user in query:
                user.first_name = first_name
                user.last_name = last_name
                user.date_of_birth = date_of_birth
                user.gender = gender
                user.updated_by
                user.email = email
                user.phone_no = phone_no
                user.updated_date = current_time
                user.updated_time = current_time
                user.save()

            Result.code = 200
            Result.query = queryDb_User_All()
        else:
            Result.code = "Error"
            return Result
    except:
        Result.code = "Error"

    return Result
