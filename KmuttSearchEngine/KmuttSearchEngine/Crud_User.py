import datetime
from django.http import HttpRequest
from app.models import *
from KmuttSearchEngine.Query import *


class Result:
  code = ''
  context = ''
  query = ''

def update_status_User(request,id):

	query = userinfo.objects.filter(id=id)

	current_time = datetime.datetime.now().replace(microsecond=0)


	for user in query:

		if (user.is_active == True):
			user.is_active = False
			user.deleted_by = request.user.id
			user.deleted_date = current_time
			user.deleted_time = current_time
			user.save()
		else:
			user.is_active = True
			user.deleted_by = request.user.id
			user.deleted_date = current_time
			user.deleted_time = current_time
			user.save()


	Result.code = 200
	Result.query = queryDb_User_All()

	return Result

def update_user_profile(request,id):

	current_time = datetime.datetime.now().replace(microsecond=0)
	if (request.POST.get('first_name_'+str(id)) and request.POST.get('last_name_'+str(id)) and request.POST.get('date_of_birth_'+str(id)) 
		and request.POST.get('gender_'+str(id)) and request.POST.get('email_'+str(id)) and request.POST.get('phone_no_'+str(id))):

		first_name = request.POST.get('first_name_'+str(id))
		last_name = request.POST.get('last_name_'+str(id))
		date_of_birth = request.POST.get('date_of_birth_'+str(id))
		gender = request.POST.get('gender_'+str(id))
		email = request.POST.get('email_'+str(id))
		phone_no = request.POST.get('phone_no_'+str(id))

	else:
		Result.code = 404
		return Result

	query = userinfo.objects.filter(id=id)

	for user in query:
		user.first_name = first_name
		user.last_name = last_name
		user.date_of_birth = date_of_birth
		user.gender = gender
		user.updated_by = request.user.id
		user.email = email
		user.phone_no = phone_no
		user.updated_date = current_time
		user.updated_time = current_time
		user.save()

	Result.code = 200
	Result.query = queryDb_User_All()

	return Result