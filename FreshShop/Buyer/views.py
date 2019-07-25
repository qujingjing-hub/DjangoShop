from django.shortcuts import render

from Buyer.models import *
from django.http import JsonResponse
from django.shortcuts import HttpResponseRedirect

from Store.views import set_password

def loginValid(fun):
    def inner(request,*args,**kwargs):
        c_user = request.COOKIES.get("username")
        s_user = request.session.get("username")
        if c_user and s_user and c_user == s_user:
            return fun(request,*args,**kwargs)
        else:
            return HttpResponseRedirect("/Buyer/login/")
    return inner

def register(request):
    if request.method == "POST":
        username = request.POST.get("user_name")
        password = request.POST.get("pwd")
        email = request.POST.get("email")

        buyer = Buyer()
        buyer.username = username
        buyer.password = set_password(password)
        buyer.email = email
        buyer.save()
        return HttpResponseRedirect("/Buyer/login/")
    return render(request,"buyer/register.html")

def ajax_userValid(request):
    result = {"status":"error","content":""}
    username = request.GET.get("username")
    if username:
        user = ajax_userValid(username)
        if user:
            result["content"] = "用户名已经存在"
        else:
            result["content"] = "用户名可以使用"
            result["status"]="success"
    else:
        result["content"] = "用户名不可以为空"
    return JsonResponse(result)

def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("pwd")
        if username and password:
            user = Buyer.objects.filter(username=username).first()
            if user:
                web_password = set_password(password)
                if user.password == web_password:
                    response = HttpResponseRedirect("/Buyer/index")
                    response.set_cookie("username",user.username)
                    request.session["username"]= user.username

                    response.set_cookie("user_id",user.id)

                    return response
    return render(request,"buyer/login.html")

def logout(request):
    response = HttpResponseRedirect("/Buyer/login/")
    for key in request.COOKIES:
        response.delete_cookie(key)
    del request.session["username"]
    return response

@loginValid
def index(request):
    return render(request,"buyer/index.html")

# Create your views here.
def base(request):
    return render(request,"buyer/base.html")