from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render

from adminapp.models import Student,Faculty


#from smsproject.adminapp.models import Admin,Course,Faculty,Student

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

