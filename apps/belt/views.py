from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse, redirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from .models import *
from django.db.models import Count
import bcrypt
password = b"super secret password"

def index(request):
	return render(request, 'belt/main.html')

def register(request):
	checking_db_pw = request.POST.get('first_password')
	hashed = bcrypt.hashpw(checking_db_pw.encode(), bcrypt.gensalt(14))
	user = User.objects.filter(email=request.POST.get('email'))
	errors = []
	passfail = True
	passes = []
	if len(request.POST.get('first_name')) < 2:
		errors.append('Need at least 2 characters for the first name')
		passfail = False
	if len(request.POST.get('last_name')) < 2:
		errors.append('Need at least 2 characters for the last name')
		passfail = False
	if request.POST['first_password'] != request.POST['confirmed_password']:
		errors.append('Passwords do not match')
		passfail = False
	if len(request.POST.get('first_password')) < 8:
		errors.append('Password not long enough')
		passfail = False
	if user.exists():
		errors.append('User already exists')
		passfail = False
	if passfail == True:
		#calling the function to run the save // inefficient but works better than orm create
		user = User()
		user.first_name = request.POST.get('first_name')
		user.last_name = request.POST.get('last_name')
		user.email = request.POST.get('email')
		user.date_of_birth = request.POST.get('dob')
		user.password = hashed
		user.save()
		passes.append('Registered. Log in now.')
		return render(request, 'belt/main.html', {'passes': passes})
	else:
		return render(request, 'belt/main.html', {'errors': errors})


def login(request):
	log_error = []
	checking_db_pw = request.POST.get('password')
	user = User.objects.filter(email=request.POST.get('email'))
	user1 = User.objects.get(email=request.POST.get('email'))
	if len(user)<1:
		log_error.append("This user doesn't exist")
		return render(request, 'belt/main.html', {'log_error': log_error})
	elif bcrypt.checkpw(checking_db_pw.encode(), user1.password.encode()):
		log_error.append("Email - Password combo inaccurate")
		return render(request, 'belt/main.html', {'log_error': log_error})
	else:
		request.session['user_id'] = user[0].id
		return redirect('/pokepage')

def logout(request):
	request.session.clear()
	return redirect('/')

def pokepage(request):
	if "user_id" in request.session:
		users = User.objects.all().exclude(id=request.session['user_id'])
		pokes = Poke.objects.all()
		user_poke_count = Poke.objects.all().filter(poked=request.session['user_id'])
		list_of_users = Poke.objects.all().filter(poked=request.session['user_id']).exclude(id=request.session['user_id'])
		user = User.objects.get(id=request.session['user_id'])
		current_user = User.objects.get(id=request.session['user_id'])
		context = {
			'current_user': current_user,
			'user': user, 
			'users': users, 
			'pokes': pokes, 
			'user_poke_count': user_poke_count, 
			'list_of_users': list_of_users,
			}
		return render(request, 'belt/pokes.html', context)
	else:
		return redirect('/')

def poke(request, user_id):
	#the one who does the poking
	poker = User.objects.get(id=request.session['user_id'])
	#the one who is poked
	poked = User.objects.get(id=user_id)
	#calling the function to run the save // inefficient but works better than orm create
	poke = Poke()
	poke.poker = poker
	poke.poked = poked
	poke.counter+=1
	#an attempt in pokes.html to get the names to collapse. didn't work but keeping it here to show i tried	/// poke.total = poke.counter
	poke.save()
	return redirect('/pokepage')


