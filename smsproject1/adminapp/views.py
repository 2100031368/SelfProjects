from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.forms import modelform_factory
from django.http import HttpResponse

from urllib.parse import unquote
from django.db.models import Q
from django.contrib.auth import logout


import matplotlib.pyplot as plt
from django.shortcuts import redirect

import json
from django.core.mail import send_mail

from django.db.models import Count

from django.shortcuts import render, redirect

from .forms import AddFacultyForm, AddStudentForm, StudentUpdateForm, FacultyUpdateForm, FacultyCourseMappingForm
from .models import Admin, Student, Course, Faculty, FacultyCourseMapping, Grievance

from django.shortcuts import render, redirect

from regapp.models import RegM,RegHistoryM, FeedbackPosted
from regapp.forms import AddRegForm

from facultyapp.models import InternalsAccess, Internals

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

###############################################
def adminhome(request):
    auname = request.session["auname"]
    return render(request, "adminhome.html", {"adminuname": auname})

def adminchangepwd(request):
    return render(request, "adminchangepwd.html")


def adminpwdupdt(request):
    an = request.session["auname"]
    if(request.method == "POST"):
        oldpwd = request.POST["opwd"]
        newpwd = request.POST["npwd"]
        records = Admin.objects.all()
        flag = Admin.objects.filter(Q(username=an) & Q(password=oldpwd))
        if (flag):
            if (Admin.objects.filter(password=newpwd)):
                msg = "Old and New passwords are same"
            else:
                Admin.objects.filter(username=an).update(password=newpwd)
                subject = "ERP PASSWORD UPDATION"
                message = f'Dear Admin,\n Your Password has been Updated.If not Youas you are having super-user credentials update your password immediately.\nThankYou.'
                email=settings.EMAIL_HOST_USER
                recipient=[]
                send_mail(subject, message, email, recipient)
                msg = "Password Updated Successfully"
        else:
            msg = "Old Password is not matching"
        return render(request, "adminchangepwd.html", {"msg": msg})
    else:
        return render(request, "adminchangepwd.html")



def adminLogOut(request):
    logout(request)
    return render(request, "login.html")


def checkadminlogin(request):
    if request.method == "POST":

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
    else:
        return render(request, "login.html")


########################################################################################################

from django.db.models import Q



def viewcourses(request):
    auname = request.session["auname"]
    if (request.method == "POST"):
        dept = request.POST["dept"]
        ay = request.POST["ay"]
        sem = request.POST["sem"]
        x=Course.objects.filter(Q(department=dept)&Q(academicyear=ay)&Q(semester=sem))
        return render(request, "viewcourses.html", {"coursesdata" : x, "adminuname": auname})
    else:
        return render(request, "filter.html", {"adminuname": auname})


    '''if request.method == "POST":

        b = request.POST["dept"]
        c = request.POST["ay"]
        e = request.POST["sid"]

        # to lower case
        b = b.upper()
        c = c.upper()
        e = e.upper()

        x = Course.objects.filter(department__iexact=b)

        if (c is not None and e is not None):
            x = Course.objects.filter(Q(department__iexact=b) & Q(academicyear__iexact=c) & Q(coursecode__iexact=e))

        elif (c is not None):
            x = Course.objects.filter(Q(department__iexact=b) & Q(academicyear__iexact=c))

        elif (e is not None):
            x = Course.objects.filter(Q(department__inexact=b) & Q(coursecode__iexact=e))
        print(x)
        for i in x:
            print(x.coursecode)
        return render(request, "viewcourses.html", {"coursesdata" : x, "adminuname": auname})
    else:
        return render(request, "aviewcourse0.html", {"adminuname": auname})
    '''



##################################################################################################

def admincourse(request):
    auname = request.session["auname"]
    return render(request, "admincourse.html", {"adminuname": auname})


def adminfaculty(request):
    auname = request.session["auname"]
    return render(request, "adminfaculty.html", {"adminuname": auname})


def adminstudent(request):
    auname = request.session["auname"]
    return render(request, "adminstudent.html", {"adminuname": auname})
def viewstudents(request):
    auname = request.session["auname"]
    if(request.method == "POST"):
        pgm=request.POST["pgm"]
        dept=request.POST["dept"]
        ay=request.POST["ay"]
        x= Student.objects.filter(Q(program=pgm)&Q(department=dept)&Q(ay=ay))
        return render(request, "aviewstu1.html", {"x": x, "adminuname": auname})
    else:
        return render(request, "filter.html", {"adminuname": auname})


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
        x = Student.objects.filter(Q(program=s.program) & Q(department=s.department) & Q(ay=s.ay) & Q(semester=s.semester))
        return render(request, "aviewstu1.html", {"msg": msg, "adminuname": auname, "x":x})

    else:
        form = StudentUpdateForm(instance=s)
        return render(request, "updatestudent2.html", {"form": form, "adminuname": auname, "s": s})


###############################################################

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
    #count = Course.objects.count()
    return render(request, "deletecourse.html", {"coursesdata": courses, "adminuname": auname})


def coursedeletion(request, ccode):
    try:

        course=Course.objects.get(coursecode = ccode)
        x=RegHistoryM.objects.filter(Q(sprogram=course.program)&Q(sdept=course.department)&Q(say=course.academicyear)&Q(syr=course.year)&Q(ssem=course.semester))
        if x is not None:
            for r in x:
                for i in range(1, 8):
                    cc_field = f'cc{i}'
                    if getattr(r, cc_field) == ccode:
                        setattr(r, cc_field, "")
                        setattr(r, f's{i}', "")
                        setattr(r, f'f{i}', 0)
                        setattr(r, f'sec{i}', 0)
                r.save()
                email = Student.objects.get(studentid=r.sid.studentid).email

                subject = "Course Deletion from your Registered Courses."
                message = f'Dear {r.sname} from your Registered Courses from academic year {course.academicyear} the Course - {course.coursetitle}, bearing CourseCode - {course.coursecode} has been deleted by the administration.\n Thank You.\n Team SCMS.'
                sender = settings.EMAIL_HOST_USER
                rec = [email]
                send_mail(subject, message, sender, rec)
        fcm = FacultyCourseMapping.objects.filter(course=course)
        if fcm is not None:
            for i in fcm:
                fid = i.faculty.facultyid
                email = i.faculty.email

                subject = "Course Deletion from your Allotted Courses."
                message = f'Dear {i.faculty.fullname} from your Allotted Courses from academic year {course.academicyear} the Course - {course.coursetitle}, bearing CourseCode - {course.coursecode} has been deleted by the administration.For more details verify ERP.\n Thank You.\nTeam SCMS.'
                sender = settings.EMAIL_HOST_USER
                rec = [email]
                send_mail(subject, message, sender, rec)

        Course.objects.filter(coursecode=ccode).delete()
        FacultyCourseMapping.objects.filter(course=course).delete()
        msg="Deleted Course Successfully"
        # return HttpResponse("deleted successfully")
        return render(request, "admincourse.html", {"msg":msg})
    except:
        return redirect("deletecourse")


def updatecourse1(request, ccode):
    auname = request.session["auname"]
    c = Course.objects.get(coursecode=ccode)
    return render(request, "updatecourse2.html", {"c": c, "adminuname": auname})


def updatecourse2(request):
    auname = request.session["auname"]
    if(request.method =="POST"):
        ccode = request.POST["ccode"]
        dep = request.POST["dept"]
        prgm = request.POST["program"]
        ay = request.POST["ay"]
        sem = request.POST["sem"]
        yr = request.POST["year"]
        ltps = request.POST["ltps"]
        credits = request.POST["credits"]
        # course = Course(department=dep, program=prgm, academicyear=ay, semester=sem, year=yr,coursetitle=ctitle, ltps=ltps, credits=credits)
        course=Course.objects.get(coursecode=ccode)
        x=RegHistoryM.objects.filter(Q(sprogram=course.program)&Q(sdept=course.department)&Q(say=course.academicyear)&Q(syr=course.year)&Q(ssem=course.semester))
        if x is not None:
            for r in x:
                if(course.program != prgm or course.department != dep or course.academicyear != ay or course.year != yr or course.semester != sem):
                       for i in range(1, 8):
                           cc_field = f'cc{i}'
                           if getattr(r, cc_field) == ccode:
                               setattr(r, cc_field, "")
                               setattr(r, f's{i}', "")
                               setattr(r, f'f{i}', 0)
                               setattr(r, f'sec{i}', 0)
                       r.save()
                       email=Student.objects.get(studentid=r.sid.studentid).email

                       subject="Course Deletion from your Registered Courses."
                       message=f'Dear {r.sname} from your Registered Courses from academic year {course.academicyear} the Course - {course.coursetitle}, bearing CourseCode - {course.coursecode} has been deleted by the administration.\n Thank You.\n Team SCMS.'
                       sender=settings.EMAIL_HOST_USER
                       rec=[email]
                       send_mail(subject, message, sender, rec)

        course=Course.objects.get(coursecode=ccode)
        fcm= FacultyCourseMapping.objects.filter(course=course)
        if fcm is not None:
            for i in fcm:
                fid=i.faculty.facultyid
                email=i.faculty.email

                subject = "Course Details Updation from your Allotted Courses."
                message = f'Dear {i.faculty.fullname} from your Allotted Courses from academic year {course.academicyear} the Course - {course.coursetitle}, bearing CourseCode - {course.coursecode} has been updated by the administration.For more details verify ERP.\n Thank You.\nTeam SCMS.'
                sender = settings.EMAIL_HOST_USER
                rec = [email]
                send_mail(subject, message, sender, rec)


        Course.objects.filter(coursecode=ccode).update(department=dep, program=prgm, academicyear=ay, semester=sem, year=yr,
                                                       ltps=ltps, credits=credits)
        msg = "Updated successfully"
        return render(request, "filter.html", {"msg": msg, "adminuname": auname})



###################################

def viewfaculty(request):
    auname = request.session["auname"]
    x=Faculty.objects.all()
    return render(request, "viewfaculty.html", {"facultydata": x, "adminuname": auname})

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



def updatefaculty2(request, fid):
    auname = request.session["auname"]
    f = Faculty.objects.get(facultyid=fid)
    if request.method == "POST":
        form = FacultyUpdateForm(request.POST, instance=f)
        if form.is_valid():
            form.save()
            msg="Updated Successfully"
        else:
            msg = "Failed Updating"
        x = Faculty.objects.all()
        return render(request, "viewfaculty.html", {"msg":msg, "facultydata":x})
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
    c1=c2=0
    for i in y:
        if(i.cc1 is not None and i.cc1.coursecode==cc and i.fcm1.faculty.facultyid==fid and i.fcm1.section==sec):
            c1=c1+1
            a.append(i)
        elif(i.cc2 is not None and i.cc2.coursecode==cc and i.fcm2.faculty.facultyid==fid and i.fcm2.section==sec):
            c1 = c1 + 1
            a.append(i)
        elif (i.cc3 is not None and i.cc3.coursecode == cc and i.fcm3.faculty.facultyid == fid and i.fcm3.section == sec):
            c1 = c1 + 1
            a.append(i)
        elif (i.cc4 is not None and i.cc4.coursecode == cc and i.fcm4.faculty.facultyid == fid and i.fcm4.section == sec):
            c1 = c1 + 1
            a.append(i)
        elif (i.cc5 is not None and i.cc5.coursecode == cc and i.fcm5.faculty.facultyid == fid and i.fcm5.section == sec):
            c1 = c1 + 1
            a.append(i)
        elif (i.cc6 is not None and i.cc6.coursecode == cc and i.fcm6.faculty.facultyid == fid and i.fcm6.section == sec):
            c1 = c1 + 1
            a.append(i)
        elif (i.cc7 is not None and i.cc7.coursecode == cc and i.fcm7.faculty.facultyid == fid and i.fcm7.section == sec):
            c1 = c1 + 1
            a.append(i)
    z=FeedbackPosted.objects.filter(Q(fid=fid)&Q(say=ay)&Q(syr=yr)&Q(ssem=sem)&Q(ccode=cc)&Q(section=sec))
    c2=len(z)

    return render(request, "aviewfeedback1.html", {"a": a,"p":p, "adminuname": auname, "c1":c1, "c2":c2})

def aviewfeedback2(request, sid, fid, ay, yr, sem, cc, sec):
    auname = request.session["auname"]
    z=FeedbackPosted.objects.get(Q(sid=sid)&Q(fid=fid)&Q(say=ay)&Q(syr=yr)&Q(ssem=sem)&Q(ccode=cc)&Q(section=sec))
    return render(request, "aviewfeedback2.html", {"z": z, "adminuname": auname})


def aviewfeedback3(request, ay, yr, sem, dept, fid, cc, sec):
    auname = request.session.get("auname")
    x = FeedbackPosted.objects.filter(Q(say=ay) & Q(syr=int(yr)) & Q(ssem=sem) & Q(sdept=dept) & Q(fid=fid) & Q(section=int(sec)))
    y = RegHistoryM.objects.filter(Q(say=ay) & Q(syr=yr) & Q(ssem=sem) & Q(sdept=dept))

    c1 = c2 = 0
    for i in y:
        if (i.cc1 is not None and i.cc1.coursecode == cc and i.fcm1.faculty.facultyid == fid and i.fcm1.section == sec):
            c1 = c1 + 1
        elif (i.cc2 is not None and i.cc2.coursecode == cc and i.fcm2.faculty.facultyid == fid and i.fcm2.section == sec):
            c1 = c1 + 1

        elif (i.cc3 is not None and i.cc3.coursecode == cc and i.fcm3.faculty.facultyid == fid and i.fcm3.section == sec):
            c1 = c1 + 1
        elif (i.cc4 is not None and i.cc4.coursecode == cc and i.fcm4.faculty.facultyid == fid and i.fcm4.section == sec):
            c1 = c1 + 1
        elif (i.cc5 is not None and i.cc5.coursecode == cc and i.fcm5.faculty.facultyid == fid and i.fcm5.section == sec):
            c1 = c1 + 1
        elif (i.cc6 is not None and i.cc6.coursecode == cc and i.fcm6.faculty.facultyid == fid and i.fcm6.section == sec):
            c1 = c1 + 1
        elif (i.cc7 is not None and i.cc7.coursecode == cc and i.fcm7.faculty.facultyid == fid and i.fcm7.section == sec):
            c1 = c1 + 1
    c2=len(x)
    return render(request, "aviewfeedback3.html", {"ay": ay, "yr":yr, "sem":sem, "dept":dept, "fid":fid,"cc":cc, "sec":sec,"x":x, "adminuname": auname, "c1":c1, "c2":c2})
def aviewfeedback4(request, q, ay, yr, sem, dept, fid, cc, sec,c1,c2):
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
    return render(request, "aviewfeedback3.html",{"ay": ay, "yr": yr, "sem": sem, "dept": dept, "fid": fid, "cc": cc, "sec": sec, "x": x, "adminuname": auname,"c1":c1, "c2":c2})
    #return HttpResponse("hi")

##EFC050;

################################################################3


########## giving access to other faculty
def agiveaccess0(request):
    auname = request.session.get("auname")
    x=Faculty.objects.all()
    auname = request.session.get("auname")
    return render(request, "agiveaccess0.html", {"facultydata":x, "adminuname":auname})

from django.http import JsonResponse

def agiveaccess1(request):
    auname = request.session.get("auname")
    x = Faculty.objects.all()

    if request.method == 'POST':
        hidden_data = request.POST.get('hiddenData', '[]')

        try:
            faculty_data = json.loads(hidden_data)

            for faculty in faculty_data:
                fid = faculty.get('facultyid')
                access = int(faculty.get('access', 0))
                graccess = int(faculty.get('graccess', 0))  # Get grievance access

                # Update access and grievance access in the database
                a = Faculty.objects.get(facultyid=fid)
                a.access = access
                a.graccess = graccess
                a.save()

            msg = "Accesses have been Modified"
            return render(request, "agiveaccess0.html", {"facultydata": x, "msg": msg, "adminuname": auname})

        except json.JSONDecodeError as e:
            print(f"JSONDecodeError: {str(e)}")
            return HttpResponse("Error: Invalid JSON data received.", status=400)

    return render(request, "agiveaccess0.html", {"facultydata": x, "adminuname": auname})

######### view student internals
def astuinternals(request,sid):
    auname = request.session.get("auname")
    return render(request, "aysemfilter.html", {"adminuname":auname,"sid":sid})
def astuinternals2(request,sid):
    auname = request.session.get("auname")
    if(request.method=="POST"):
        ay=request.POST["ay"]
        sem=request.POST["sem"]
        x=Internals.objects.filter(Q(sid=sid)&Q(ay=ay)&Q(sem=sem))

        if x.exists():
            #print("x" + x)
            return render(request, "astuinternals.html", {"adminuname":auname, "x":x, "sid":sid, "ay":ay, "sem":sem})
        else:
            #print("empty")
            msg=f'NO INTERNALS POSTED YET FOR ID-{sid} during Academic Year-{ay} and Sem-{sem}'
            return render(request, "aysemfilter.html", {"x": x, "adminuname": auname, "msg":msg})
    else:
        return render(request, "aysemfilter.html", {"adminuname":auname,"sid":sid})

def aviewgrievance0(request):
    auname = request.session.get("auname")
    return render(request, "aviewgr0.html", {"adminuname":auname})
def aviewgrievance1(request):
    auname = request.session.get("auname")
    gr = Grievance.objects.all()
    lt=[]
    if gr:
        for i in gr:
            id=i.pid
            try:
                x=Faculty.objects.get(facultyid=id)
                lt.append(i)
            except ObjectDoesNotExist:
                pass
        return render(request, "aviewgr1.html",{"adminuname":auname, "lt":lt})
    else:
        msg="No Grievances Posted"
        return render(request, "aviewgr0.html", {"adminuname":auname, "msg":msg})


def aviewgrievance2(request):
    auname = request.session.get("auname")
    gr = Grievance.objects.all().order_by('-date')
    lt=[]
    if gr:
      for i in gr:
            id=i.pid
            try:
                x=Student.objects.get(studentid=id)
                lt.append(i)
            except ObjectDoesNotExist:
                pass
      return render(request, "aviewgr1.html",{"adminuname":auname, "lt":lt})
    else:
        msg="No Grievances Posted"
        return render(request, "aviewgr0.html", {"adminuname":auname, "msg":msg})

def aviewgrissuestu(request, id):
    auname = request.session.get("auname")
    x=Grievance.objects.get(id=id)
    x.status=1
    x.save()
    return render(request, "aviewgrissuestu.html", {"adminuname":auname, "x":x})

def update_issue_status(request, id):
    auname = request.session.get("auname")
    x=Grievance.objects.get(id=id)
    if x.status ==1:
      x.solved=1
      x.solvedby=1
      x.save()
      subject="Grievance Posted Has Been Solved"
      message=f'Dear {x.name},\nThe issue which has been posted by you regarding "{x.category}", - "{x.issue}" at {x.date} has been solved by the university team. If it has not been solved and marked as solved you can contact adminstration team at room no:C325.\nThankYou\nTeam SCMS.'
      email=settings.EMAIL_HOST_USER
      rec={x.email}
      send_mail(subject, message, email, rec)

    referer = request.META.get('HTTP_REFERER')
    return redirect(referer)



### admin viewing - student sgpa
def asgpa0(request,sid):
    auname = request.session.get("auname")
    if request.method == "POST":
        ay=request.POST["ay"]
        sem=request.POST["sem"]
        s = Student.objects.get(studentid=sid)
        try:

            x=RegHistoryM.objects.get(Q(say=ay)&Q(ssem = sem)&Q(sid=s))

            y=Course.objects.filter(Q(department=s.department)&Q(program=s.program)&Q(academicyear=ay)&Q(semester=sem))
            q=0
            for i in y:
                q = q + i.credits
            p=Internals.objects.filter(Q(sid=sid)&Q(dept=s.department)&Q(ay=ay)&Q(sem=sem))
            for i in p:
               if(x.cc1.coursecode == i.cc):
                   cred = x.cc1.credits * i.grade_points
               elif(x.cc2 and x.cc2.coursecode == i.cc):
                   cred = x.cc2.credits * i.grade_points
               elif(x.cc3 and x.cc3.coursecode == i.cc):
                   cred = x.cc3.credits * i.grade_points
               elif(x.cc4 and x.cc4.coursecode == i.cc):
                   cred = x.cc4.credits * i.grade_points
               elif(x.cc5 and x.cc5.coursecode == i.cc):
                   cred = x.cc5.credits * i.grade_points
               elif(x.cc6 and x.cc6.coursecode == i.cc):
                   cred = x.cc6.credits * i.grade_points
               elif(x.cc7 and x.cc7.coursecode == i.cc):
                   cred = x.cc7.credits * i.grade_points
            cred=cred/q

            b=0

            if(x.cc1):
                b=b+1
            if(x.cc2):
                b=b+1
            if (x.cc3):
                b = b + 1
            if (x.cc4):
                b = b + 1
            if (x.cc5):
                b = b + 1
            if (x.cc6):
                b = b + 1
            if (x.cc7):
                b = b + 1
            c=len(p)
            if(c < b):
                msg=f'Registered Number of Courses {b} , Total Credits {q}, Missing in {b-c} courses'
                return render(request, "asgpa1.html", {"msg":msg, "p":p, "cred":cred})
            else:
                return HttpResponse("hi")


        except ObjectDoesNotExist:
            msg="Doesn't Exist"
            return render(request, "asgpa.html", {"adminuname":auname, "msg":msg})
    else:
        return render(request, "asgpa.html", {"adminuname":auname,})