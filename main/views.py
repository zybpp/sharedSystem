from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.hashers import make_password,check_password
from account import models
import json

# Create your views here.

def index(request):
	return redirect("/login/")

def login(request):
	ret = {'status': False, 'error': "用户名或密码错误！！！", 'data': None}
	if request.session.get('is_login',None):
		return redirect("/home/")
	else:
		if request.method == "GET":
			return render(request,"login.html")
		elif request.method == "POST":
			username = request.POST.get("username")
			password = request.POST.get("password")
			if username and password:
				user = models.User.objects.filter(user=username)
				if user:
					if check_password(password,user[0].password):
						ret['status'] = True
						request.session['user'] = user[0].user
						request.session['name'] = user[0].name
						request.session['is_login'] = True
						request.session.set_expiry(5)
				else:
					ret['error'] = "用户名不存在。"
			else:
				ret['error'] = "用户名或密码不能为空。"
			return HttpResponse(json.dumps(ret))

def home(request):
	if request.session.get('is_login', None):
		print(request.method)
		return HttpResponse('Welcome Home!')
	else:
		return redirect("/login/")

def register(request):
	print(request.method)
	return render(request, "register.html")

def forgetpwd(request):
	print(request.method)
	return HttpResponse('Welcome forgetpwd!')