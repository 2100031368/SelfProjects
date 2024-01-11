from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render

from adminapp.models import Student,Faculty


#from smsproject.adminapp.models import Admin,Course,Faculty,Student


def demofunction(request):
    return HttpResponse("PFSD")

def demofunction1(request):
    return HttpResponse("<h3> SREE </h3>")

def demofunction2(request):
    return HttpResponse("<font color='blue' > SREE </font>")

def home(request):
    return render(request, "index.html")

def about(request):
    return render(request, "about.html")

def login(request):
    return render(request, "login.html")

def contactus(request):
    return render(request, "contactus.html")

def studentlogin(request):
    return render(request, "studentlogin.html")

def facultylogin(request):
    return render(request, "facultylogin.html")

def checkstudentlogin(request):
    sid= request.POST["uid"]
    spwd= request.POST["pwd"]
    flag= Student.objects.filter(Q(studentid=sid)&Q(password=spwd))

    if(flag):
        request.session["sid"] = sid
        return render(request, "studenthome.html", {"sid": sid})
    else:
        msg = "Login Failed"
        return render(request, "studentlogin.html", {"msg": msg})

def checkfacultylogin(request):
    fid=request.POST["uid"]
    fpwd=request.POST["pwd"]
    flag=Faculty.objects.filter(Q(facultyid=fid)&Q(password=fpwd))

    if(flag):
        request.session["fid"]=fid
        return render(request, "facultyhome.html", {"fid":fid})
    else:
        msg="Login Failed"
        return render(request, "facultylogin.html", {"msg":msg})

