# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from api.models import Forum, Membership
import json

def login_user(request):
    response	= {}
    if request.method == 'GET':
	return render(request, 'login.html')
    if request.method == 'POST':
	username	= request.POST.get('username', '')
	pwd		= request.POST.get('pwd', '')
	response['username'] = username
	user = authenticate(username=username, password=pwd)
	if user is not None:
	    response["success"] = True
	    response["userId"] = user.id
	    response['userName'] = user.username
	    login(request, user)
	else:
	    response["success"] = False
	    response["error"] = "Username or Password doesn't match or exist!"
	    print response
	    return render(request, 'login.html', response)
	return redirect('/geodeliberator')

#below is the user's register page.
def register(request):
    response	= {}
    if request.method == 'POST':
        username	= request.POST.get('registerName', None)
        pwd		= request.POST.get('registerPwd', None)
        email	= request.POST.get('email', None)
        forumList	= request.POST.getlist('forumList', [])
        response['registerName'] = username
        response['email'] = email

	forums	= []
	for fo in forumList:
	    try:
		forum   = Forum.objects.get(name=fo)
		forums.append(forum)
	    except Forum.DoesNotExist as e:
		print e
		continue
	if username and pwd and email and len(forums) != 0:
	    try:
		user = User.objects.create_user(username=username, password=pwd)
		for forum in forums:
		    Membership.objects.create(user=user, forum=forum, role='member')
		    response["data"] = {"userId": user.id, "userName": user.username}
		    response['success'] = True
                    user.is_active = True
		    user.save()
		print 'user is anonymous? : ', user.is_anonymous()
		#print username, pwd
		user = authenticate(username=username, password=pwd)
		if user is not None:
		    login(request, user)
		    print "user logged in"
                    print response
		    return redirect('/')
		else:
		    response['success'] = False
		    response['error'] = 'User authentication failed!'
		    print "User authentication failed"
	    except Exception as e:
		response['success'] = False
		response['error'] = 'User existed!'
		print e
	else:
	    response['success'] = False
	    response['error'] = 'Required information missing'

    print response
    return render(request, "login.html", response)

def logout_user(request):
    try:
	logout(request)
	print 'log out user'
    except Exception as e:
	print e
    return redirect('/user/login')


