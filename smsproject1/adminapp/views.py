from django.forms import modelform_factory
from django.http import HttpResponse

from urllib.parse import unquote
from django.db.models import Q

import matplotlib.pyplot as plt

import json

from django.db.models import Count

from django.shortcuts import render, redirect

from .forms import AddFacultyForm, AddStudentForm, StudentUpdateForm, FacultyUpdateForm, FacultyCourseMappingForm
from .models import Admin, Student, Course, Faculty, FacultyCourseMapping

from django.shortcuts import render, redirect

from regapp.models import RegM,RegHistoryM, FeedbackPosted
from regapp.forms import AddRegForm

from facultyapp.models import CC

from django import forms


# Create your views here.

####################################################
# student history reg -admin

def regadmin1(requset):
    auname = requset.session["auname"]
    a = RegM.objects.all()

    return render(requset, "regadmin1.html", {"adminuname": auname, "a": a})


def regadmin2(request):
    auname = request.session["auname"]
    b = RegHistoryM.objects.all()

    return render(request, "regadmin2.html", {"adminuname": auname, "b": b})


def history(request, id, ay, yr, sem):
    auname = request.session["auname"]

    print(f"id: {id}, ay: {ay}, yr: {yr}, sem: {sem}")

    c = RegHistoryM.objects.get(Q(sid=id) & Q(say=ay) & Q(syr=yr) & Q(ssem=sem))
    return render(request, "regadmin3.html", {"adminuname": auname, "c": c})


############################################

# view  reg-alloted
def regadmin4(request, dept, ay, yr, sem):
    auname = request.session["auname"]
    d = RegM.objects.get(Q(dept=dept) & Q(ay=ay) & Q(yr=yr) & Q(sem=sem))
    return render(request, "regadmin4.html", {"adminuname": auname, "d": d})


###################################################
# ADD NEW REGISTRATION

def regadmin5(request):
    auname = request.session["auname"]
    form = AddRegForm()
    if request.method == "POST":
        form = AddRegForm(request.POST)
        if form.is_valid():
            form.save()
            msg = "Added Successfully"
        return render(request, "regadmin1.html", {"adminuname": auname, "msg": msg})
    return render(request, "regadmin5.html", {"adminuname": auname, "form": form})
    #x = FacultyCourseMapping.objects.all()
    '''
    for k in c:
        cc=k.coursecode
        x = FacultyCourseMapping.objects.filter(Q(course=k))
        for j in x:
            if j.course in f:
                f[j.course].append(j.faculty)
            else:
                f[j.course]=[j.faculty]

    print(f)
    return render(request, "a-regalloted2.html", {"f":f, "adminuname":auname, "dept":dept, "ay":ay, "yr":yr, "sem":sem})
   '''
'''
def regalloted3(request):
    courses=request.POST.getlist["course"]
    faculties=request.POST.getlist["faculty"]
    for i in range(len(courses)):
        reg_allot_inst=RegAllot(
            dept=request.POST["dept"],
            ay=request.POST["ay"],
            yr=request.POST["yr"],
            sem=request.POST["sem"],
            c1=courses[i],

        )
'''




def adminhome(request):
    auname = request.session["auname"]
    return render(request, "adminhome.html", {"adminuname": auname})



def adminchangepwd(request):
    return render(request, "adminchangepwd.html")


def adminpwdupdt(request):
    an = request.session["auname"]
    oldpwd = request.POST["opwd"]
    newpwd = request.POST["npwd"]
    records = Admin.objects.all();
    '''for x in records:
        if x.username == an:
            if(x.password == oldpwd):'''

    flag = Admin.objects.filter(Q(username=an) & Q(password=oldpwd))
    if (flag):
        if (Admin.objects.filter(password=newpwd)):
            msg = "Old and New passwords are same"
        else:
            Admin.objects.filter(username=an).update(password=newpwd)
            msg = "Password Updated Successfully"
    else:
        msg = "Old Password is not matching"
    return render(request, "adminchangepwd.html", {"msg": msg})


def adminLogOut(request):
    return render(request, "login.html")


def checkadminlogin(request):
    '''if request.method == "POST":
        adminuname = request.POST["uname"] #if it is get then write request.GET
        adminpwd = request.POST["pwd"
    else:
        adminuname = request.GET["uname"]  # if it is get then write request.GET
        adminpwd = request.GET["pwd"]
    data = adminuname +" "+ adminpwd
   # return HttpResponse(adminuname, adminpwd) takes only one argu so prints only uname
    return HttpResponse(data)'''
    adminuname = request.POST["uname"]  # if it is get then write request.GET
    adminpwd = request.POST["pwd"]

    flag = Admin.objects.filter(Q(username=adminuname) & Q(password=adminpwd))

    if (flag):
        # return HttpResponse("Login Success")
        print("login success")  # prints in terminal
        request.session["auname"] = adminuname  # session is created
        return render(request, "adminhome.html", {"adminuname": adminuname})
    else:
        msg = "Login Failed"
        return render(request, "login.html", {"msg": msg})


def viewstudents(request):
    students = Student.objects.all()
    count = Student.objects.count()
    auname = request.session["auname"]
    return render(request, "viewstudents.html", {"studentsdata": students, "count": count, "adminuname": auname})


def viewcourses(request):
    courses = Course.objects.all()
    count = Course.objects.count()
    auname = request.session["auname"]
    return render(request, "viewcourses.html", {"coursesdata": courses, "count": count, "adminuname": auname})


def viewfaculty(request):
    faculty = Faculty.objects.all()
    count = Faculty.objects.count()
    auname = request.session["auname"]
    return render(request, "viewfaculty.html", {"facultydata": faculty, "count": count, "adminuname": auname})


def admincourse(request):
    auname = request.session["auname"]
    return render(request, "admincourse.html", {"adminuname": auname})


def adminfaculty(request):
    auname = request.session["auname"]
    return render(request, "adminfaculty.html", {"adminuname": auname})


def adminstudent(request):
    auname = request.session["auname"]
    return render(request, "adminstudent.html", {"adminuname": auname})


###############################################################3

def addcourse(request):
    auname = request.session["auname"]
    return render(request, "addcourse.html", {"adminuname": auname})


def insertcourse(request):
    auname = request.session["auname"]
    dept = request.POST["dept"]
    program = request.POST["program"]
    ay = request.POST["ay"]
    sem = request.POST["sem"]
    year = request.POST["year"]
    ccode = request.POST["ccode"]
    ctitle = request.POST["ctitle"]
    ltps = request.POST["ltps"]
    credits = request.POST["credits"]

    course = Course(department=dept, program=program, academicyear=ay, semester=sem, year=year, coursecode=ccode,
                    coursetitle=ctitle, ltps=ltps, credits=credits)

    Course.save(course)
    msg = "Saved successfully"
    return render(request, "addcourse.html", {"msg": msg, "adminuname": auname})


def deletecourse(request):
    auname = request.session["auname"]
    courses = Course.objects.all()
    count = Course.objects.count()
    return render(request, "deletecourse.html", {"coursesdata": courses, "count": count, "adminuname": auname})


def coursedeletion(request, cid):
    Course.objects.filter(id=cid).delete()
    # return HttpResponse("deleted successfully")
    return redirect("deletecourse")


def updatecourse1(request):
    auname = request.session["auname"]
    return render(request, "updatecourse1.html", {"adminuname": auname})


def updatecourse2(request):
    auname = request.session["auname"]
    key = request.POST["key"]
    c = Course.objects.get(coursecode=key)
    return render(request, "updatecourse2.html", {"c": c, "adminuname": auname})


def updatecourse3(request):
    auname = request.session["auname"]
    ccode = request.POST["ccode"]
    dep = request.POST["dept"]
    prgm = request.POST["program"]
    ay = request.POST["ay"]
    sem = request.POST["sem"]
    yr = request.POST["year"]
    ltps = request.POST["ltps"]
    credits = request.POST["credits"]
    # course = Course(department=dep, program=prgm, academicyear=ay, semester=sem, year=yr,coursetitle=ctitle, ltps=ltps, credits=credits)

    Course.objects.filter(coursecode=ccode).update(department=dep, program=prgm, academicyear=ay, semester=sem, year=yr,
                                                   ltps=ltps, credits=credits)
    msg = "Updated successfully"
    return render(request, "updatecourse1.html", {"msg": msg, "adminuname": auname})


###################################
def addfaculty(request):
    auname = request.session["auname"]

    form = AddFacultyForm()
    if request.method == "POST":
        form1 = AddFacultyForm(request.POST)
        if form1.is_valid():
            form1.save()
            msg = "Faculty added successfully"
            return render(request, 'adminfaculty.html', {"msg": msg, "adminuname": auname})
        else:
            msg = "Failed to add Data"
            return render(request, "addfaculty.html", {"msg": msg})

    return render(request, "addfaculty.html", {"form": form})


def deletefaculty(request):
    auname = request.session["auname"]
    faculty = Faculty.objects.all()
    count = Faculty.objects.count()
    return render(request, "deletefaculty.html", {"faculties": faculty, "count": count, "adminuname": auname})


def facultydeletion(request, fid):
    Faculty.objects.filter(facultyid=fid).delete()
    return redirect("deletefaculty")


def facultycoursemapping(request):
    auname = request.session["auname"]
    fcm = FacultyCourseMapping.objects.all()
    return render(request, "facultycoursemapping.html", {"adminuname": auname, "fcm": fcm})


def addfacultycourse(request):
    auname = request.session["auname"]
    form = FacultyCourseMappingForm()
    if request.method == "POST":
        form = FacultyCourseMappingForm(request.POST)
        if form.is_valid():
            form.save()
            msg = "Mapped Successfully"
            return render(request, "adminhome.html", {"adminuname": auname, "msg": msg})
    return render(request, "addfacultycourse.html", {"adminuname": auname, "form": form})


def updatefaculty1(request):
    auname = request.session["auname"]
    f = Faculty.objects.all()
    return render(request, "updatefaculty1.html", {"adminuname": auname, "f": f})


def updatefaculty2(request, fid):
    auname = request.session["auname"]
    f = Faculty.objects.get(facultyid=fid)
    if request.method == "POST":
        form = FacultyUpdateForm(request.POST, instance=f)
        if form.is_valid():
            form.save()
            msg = "Updated Successfully"
        else:
            msg = "Failed Updating"
        return render(request, "updatefaculty1.html", {"msg": msg, "adminuname": auname})
    else:
        form = FacultyUpdateForm(instance=f)
        return render(request, "updatefaculty2.html", {"form": form, "adminuname": auname, "f": f})


###############################

def addstudent(request):
    auname = request.session["auname"]
    form = AddStudentForm()

    if request.method == "POST":
        form1 = AddStudentForm(request.POST)
        if form1.is_valid():
            form1.save()
            msg = "insertion done"
            return render(request, "adminstudent.html", {"msg": msg, "adminuname": auname})
        else:
            msg = "Failed to add Data"
            return render(request, "addstudent.html", {"msg": msg})

    return render(request, "addstudent.html", {"form": form})


def deletestudent(request):
    auname = request.session["auname"]
    student = Student.objects.all()
    count = Student.objects.count()
    return render(request, "deletestudent.html", {"student": student, "adminuname": auname})


def studentdeletion(request, sid):
    Student.objects.filter(id=sid).delete()
    return redirect("deletestudent")


def updatestudent1(request):
    auname = request.session["auname"]
    studentdata = Student.objects.all()
    return render(request, "updatestudent1.html", {"adminuname": auname, "studentsdata": studentdata})


def updatestudent2(request, sid):
    auname = request.session["auname"]
    s = Student.objects.get(studentid=sid)
    if (request.method == "POST"):
        form1 = StudentUpdateForm(request.POST, instance=s)
        if form1.is_valid():
            form1.save()
            msg = "Updated successfully"
        else:
            msg = "Invalid"
        return render(request, "updatestudent1.html", {"msg": msg, "adminuname": auname})

    else:
        form = StudentUpdateForm(instance=s)
        return render(request, "updatestudent2.html", {"form": form, "adminuname": auname, "s": s})


############  Regarding FEEDBACK ##############
def aviewfeedback0(request):
    auname = request.session["auname"]
    x=FacultyCourseMapping.objects.all()

    return render(request, "aviewfeedback0.html", {"x":x, "adminuname": auname})

def aviewfeedback1(request, ay, yr, sem, dept, fid, cc, sec):
    auname = request.session["auname"]

    p=FacultyCourseMapping.objects.get(Q(faculty__facultyid=int(fid))&Q(course__coursecode=cc)&Q(section=int(sec)))
    print(p)
    y=RegHistoryM.objects.filter(Q(say=ay)&Q(syr=yr)&Q(ssem=sem)&Q(sdept=dept))
    a=[]
    for i in y:
        if(i.cc1==cc and i.f1==fid and i.sec1==sec):
            a.append(i)
        elif(i.cc2==cc and i.f2==fid and i.sec2==sec):
            a.append(i)
        elif (i.cc3 == cc and i.f3 == fid and i.sec3 == sec):
            a.append(i)
        elif (i.cc4 == cc and i.f4 == fid and i.sec4 == sec):
            a.append(i)
        elif (i.cc5 == cc and i.f5 == fid and i.sec5 == sec):
            a.append(i)
        elif (i.cc6 == cc and i.f6 == fid and i.sec6 == sec):
            a.append(i)
        elif (i.cc7 == cc and i.f7 == fid and i.sec7 == sec):
            a.append(i)


    return render(request, "aviewfeedback1.html", {"a": a,"p":p, "adminuname": auname})

def aviewfeedback2(request, sid, fid, ay, yr, sem, cc, sec):
    auname = request.session["auname"]
    z=FeedbackPosted.objects.get(Q(sid=sid)&Q(fid=fid)&Q(say=ay)&Q(syr=yr)&Q(ssem=sem)&Q(ccode=cc)&Q(section=sec))
    return render(request, "aviewfeedback2.html", {"z": z, "adminuname": auname})

## view in form of graoh
'''def aviewfeedback3(request, ay, yr, sem, dept, fid, cc,sec):
    auname = request.session["auname"]
    a=FeedbackPosted.objects.filter(Q(say=ay)&Q(syr=int(yr))&Q(ssem=sem)&Q(sdept=dept)&Q(fid=fid)&Q(section=int(sec)))
    for i in a:
        b, c, d = i.q1, i.q2, i.q3
    x=[b,c,d]
    y=[a.fdb1, a.fdb2, a.fdb3]
    plt.bar(x, y)
    plt.show() '''


def aviewfeedback3(request, ay, yr, sem, dept, fid, cc, sec):
    auname = request.session.get("auname")
    x = FeedbackPosted.objects.filter(Q(say=ay) & Q(syr=int(yr)) & Q(ssem=sem) & Q(sdept=dept) & Q(fid=fid) & Q(section=int(sec)))


    #return HttpResponse("hi")
    return render(request, "aviewfeedback3.html", {"ay": ay, "yr":yr, "sem":sem, "dept":dept, "fid":fid,"cc":cc, "sec":sec,"x":x, "adminuname": auname})
def aviewfeedback4(request, q, ay, yr, sem, dept, fid, cc, sec):
    auname = request.session.get("auname")
    q = int(q)
    mp={}
    x = FeedbackPosted.objects.filter(Q(say=ay) & Q(syr=int(yr)) & Q(ssem=sem) & Q(sdept=dept) & Q(fid=fid) & Q(section=int(sec)))
    for i in x:
        if q==1:
            for j in i.fdb1_options:
                if j[0] == i.fdb1:
                    mp[j[0]] = mp.get(j[0], 0)+1
                else:
                    mp[j[0]]=mp.get(j[0], 0)

        elif q==2 :
            for j in i.fdb2_options:
                if j[0] == i.fdb2:
                    mp[j[0]] = mp.get(j[0], 0) + 1
                else:
                    mp[j[0]] = mp.get(j[0], 0)

        elif q==3 :
            for j in i.fdb3_options:
                if j[0] == i.fdb3:
                    mp[j[0]] = mp.get(j[0], 0) + 1
                else:
                    mp[j[0]] = mp.get(j[0], 0)

        elif q==4 :
            for j in i.fdb4_options:
                if j[0] == i.fdb4:
                    mp[j[0]] = mp.get(j[0], 0) + 1
                else:
                    mp[j[0]] = mp.get(j[0], 0)

        elif q==5 :
            for j in i.fdb5_options:
                if j[0] == i.fdb5:
                    mp[j[0]] = mp.get(j[0], 0) + 1
                else:
                    mp[j[0]] = mp.get(j[0], 0)

    feedbacks = list(mp.keys())
    frequencies = list(mp.values())

    plt.bar(feedbacks, frequencies)
    plt.xlabel('Feedbacks')
    plt.ylabel('Frequencies')
    plt.title(q)
    plt.show()
    return render(request, "aviewfeedback3.html",{"ay": ay, "yr": yr, "sem": sem, "dept": dept, "fid": fid, "cc": cc, "sec": sec, "x": x, "adminuname": auname})
    #return HttpResponse("hi")

#### addin cc's to cc group #####

def addcc0(request):
    auname = request.session.get("auname")
    k=FacultyCourseMapping.objects.filter(type=True)
    return render(request, "addcc0.html", {"adminuname": auname, "k":k})

def addcc1(request, fid, cc, ay, yr, sem):
    auname = request.session.get("auname")
    x=CC.objects.filter(Q(fid=fid)&Q(cc=cc)&Q(ay=ay)&Q(yr=yr)&Q(sem=sem))
    if x:
        return HttpResponse("already exist")
    else:
        return render(request, "addcc1.html",
                      {"adminuname": auname, "fid": fid, "cc": cc, "ay": ay, "yr": yr, "sem": sem})



def addcc2(request):
    auname = request.session.get("auname")
    a=request.POST["fid"]
    k=Faculty.objects.get(facultyid=a)
    b=request.POST["cc"]
    l=Course.objects.get(id=b)
    c=request.POST["ay"]
    d=request.POST["yr"]
    e=request.POST["sem"]
    h=CC(fid=k, cc=l, ay=c, yr=int(d), sem=e)
    CC.save(h)
    return HttpResponse("added successfully")