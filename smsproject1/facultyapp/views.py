from datetime import datetime
from socket import socket

from django.conf import settings
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.storage import default_storage
from django.core.mail import send_mail
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.mail import EmailMessage

from adminapp.models import Faculty, FacultyCourseMapping, Course, Student, Grievance
from adminapp.forms import AddFacultyForm,FacultyUpdateForm,StudentUpdateForm,AddStudentForm,GrievanceForm


import matplotlib.pyplot as plt
from django.utils.html import strip_tags
from regapp.models import RegHistoryM, FeedbackPosted

from .models import CourseContent, CC, Internals, Handout
from .forms import HandoutForm

from django.http import FileResponse, Http404
from pathlib import Path


# Create your views here.

def facultyhome(request):
    sfid= request.session["fid"]
    return render(request, "facultyhome.html", {"sfid":sfid})

def checkfacultylogin(request):
    if(request.method =="POST"):

        fid=request.POST["uid"]
        fpwd=request.POST["pwd"]
        try:
            x=Faculty.objects.get(Q(facultyid=fid)&Q(password=fpwd))
            if(x.flag == 0):
                request.session["fid"]=fid
                return render(request, "facultyhome.html", {"sfid":fid})
            else:
                msg="Access Denied"
                return render(request, "facultylogin.html", {"msg": msg})
        except ObjectDoesNotExist:
            msg="Login Failed"
            return render(request, "facultylogin.html", {"msg":msg})
    else:
        return render(request, "facultylogin.html")
def facultycourse(request):
    sfid=request.session["fid"]
    #print(FacultyCourseMapping.objects.get(Faculty.facultyid==sfid))
    faculty=Faculty.objects.all()
    course=Course.objects.all()
    fcm=FacultyCourseMapping.objects.all()
    fc=[]
    for x in fcm:
        if(x.faculty.facultyid == int(sfid)):
            fc.append(x)
            #fcourses.append(x.course.coursetitle) to append only course titles
            #print(x.course.coursetitle)
        else:
            print("not getting into loop")
    print(fc)

    count=len(fc)

    return render(request, "facultycourse.html", {"sfid":sfid, "fc":fc, "count":count})



def facultyupdtpwd(request):
    sfid = request.session["fid"]
    if(request.method == "POST"):
        oldpwd=request.POST["opwd"]
        newpwd=request.POST["npwd"]
        flag=Faculty.objects.filter(Q(facultyid=sfid)&Q(password=oldpwd))
        if(flag):
            try:
                Faculty.objects.get(Q(facultyid=sfid)&Q(password=newpwd))
                msg="New password is same as Old password"
            except ObjectDoesNotExist:
                p = Faculty.objects.get(facultyid=sfid)
                Faculty.objects.filter(facultyid=sfid).update(password=newpwd)
                msg="Updated Successfully"
                subject="Your ERP Password has been Updated"
                message=f'Dear {p.fullname} your ERP Password has been Updated'
                email=settings.EMAIL_HOST_USER
                recepient=[p.email]
                send_mail(subject, message, email, recepient)
        else:
            msg="Old password is incorrect"
        return render(request, "facultychangepwd.html", {"msg":msg, "sfid":sfid})
    else:
        return render(request, "facultychangepwd.html", {"sfid": sfid})


####### faculty uploading content

def fccontent1(request):
    sfid=request.session["fid"]
    if(request.method == "POST"):
        ay = request.POST["ay"]
        sem = request.POST["sem"]
        #c = Course.objects.filter(Q(academicyear=ay)&Q(year=yr)&Q(sem=sem))


        fcm = FacultyCourseMapping.objects.filter(faculty=int(sfid))
        fc = []
        for x in fcm:
            if (x.course.academicyear == ay  and x.course.semester == sem):
                fc.append(x)

            else:
                print("not getting into loop")
        print(fc)

        count = len(fc)

        return render(request, "fccontent1.html", {"sfid":sfid, "fc":fc, "count":count})
    else:
        return render(request, "fccontent0.html", {"sfid": sfid})

def fccontent2(request, ccode):

    sfid = request.session["fid"]
    return render(request, "fccontent2.html", {"ccode": ccode, "sfid": sfid})


def fccontent3(request):
    sfid = request.session["fid"]

   # form = CourseContentForm(initial={'faculty': faculty_instance, 'course': course_instance})
    faculty_id = request.POST["faculty"]
    course_id = request.POST["course"]

    description=request.POST["description"]
    link=request.POST["link"]
    file = request.FILES["file"]

    faculty =Faculty.objects.get(facultyid=faculty_id)
    course = Course.objects.get(coursecode=course_id)

    upload=CourseContent(faculty=faculty, course=course, description= description, link=link, contentimage=file)
    #CourseContent.save(upload)
    upload.save()
    msg="Course Content Uploaded Successfully"

    return render(request, "fccontent0.html", {"sfid": sfid,"msg":msg})

#### my uploads ########
def fccontent4(request,dept, ay, yr, sem, ccode):
    sfid = request.session["fid"]
    c=Course.objects.get(Q(department=dept)&Q(academicyear=ay)&Q(year=int(yr))&Q(semester=sem)&Q(coursecode=ccode))
    x=CourseContent.objects.filter(faculty=int(sfid))

    f=[]
    for i in x:

        if(i.course == c):
            f.append(i)
        else:
            print("not")
    return render(request, "fccontent4.html", {"sfid":sfid,"f":f , "ccode":c.coursecode})


##### delete my uploads
def deltemyuploads1(request, cid):

    print(cid)

    sfid = request.session["fid"]
    '''c=Course.objects.get(coursecode=cc)
    f=Faculty.objects.get(fullname=fid)'''
    x=CourseContent.objects.get(id=cid)

    print(x.contentimage.path)
    file_path = x.contentimage.path

    if default_storage.exists(file_path):
        default_storage.delete(file_path)
        x.delete()  # Delete from db
        msg = "Deleted File Successfully"
        return render(request, "fccontent0.html", {"sfid": sfid, "msg": msg})

    return render(request, "filenotfound.html")



######## view stu reg

def viewfstudents1(request):
    sfid = request.session["fid"]
    if request.method == "POST":

        ay=request.POST["ay"]
        dept=request.POST["dept"]
        pgm=request.POST["pgm"]
        sem=request.POST["sem"]
        sec=request.POST["sec"]

        c=Course.objects.all()
        f=Faculty.objects.all()
        x=FacultyCourseMapping.objects.all()
        r=[]
        for i in x:
            if(i.course.department == dept and i.course.academicyear ==ay and i.course.semester == sem and i.course.program == pgm and i.faculty.facultyid == int(sfid) and i.section == int(sec)):
                r.append(i)
        print(r)
        return render(request, "viewfstudents2.html", {"sfid":sfid, "r":r})
    else:
        return render(request, "viewfstudents1.html", {"sfid": sfid})
def viewfstudents3(request, dept,ay,yr,sem,ct,fid):
    sfid = request.session["fid"]
    x=RegHistoryM.objects.filter(Q(say=ay)&Q(sdept=dept)&Q(syr=yr)&Q(ssem=sem))
    r=[]
    '''
    print("course title: "+ ct)
    print(fid)
     for i in x:
        print(i.sid )
        print(i.f1)
        print(i.s1)
        if(i.s1==ct):
            print("matched")
        else:
            print(i.s1)'''
    for i in x:

        if(i.cc1.coursecode == ct and i.fcm1.faculty.facultyid == fid):
            r.append(i)
        elif (i.cc2.coursecode == ct and i.fcm2.faculty.facultyid == fid):
            r.append(i)

        elif (i.cc3.coursecode == ct and i.fcm3.faculty.facultyid == fid):
            r.append(i)

        elif (i.cc4.coursecode == ct and i.fcm4.faculty.facultyid == fid):
            r.append(i)

        elif (i.cc5.coursecode == ct and i.fcm5.faculty.facultyid == fid):
            r.append(i)

        elif (i.cc6.coursecode == ct and i.fcm6.faculty.facultyid == fid):
            r.append(i)

        elif (i.cc7.coursecode == ct and i.fcm7.faculty.facultyid == fid):
            r.append(i)
    #print(r)

    else:
        return render(request, "viewfstudents3.html", {"sfid":sfid,"r":r })


###### posting att

def postatt1(request):
    sfid = request.session["fid"]
    if(request.method == "POST"):

        ay = request.POST["ay"]
        yr = request.POST["yr"]
        sem = request.POST["sem"]
        sec = request.POST["sec"]
        x=Faculty.objects.get(facultyid=sfid).cur_ay
        y=Faculty.objects.get(facultyid=sfid).cur_sem
        z=Course.objects.filter(Q(academicyear=x)&Q(semester=y))

        fc = []
        for i in z:
            try:
              p=FacultyCourseMapping.objects.get(Q(faculty=int(sfid))&Q(course=i))
              fc.append(p)
            except ObjectDoesNotExist:
                print("hi")

        print(fc)

        count = len(fc)
        return render(request, "postatt1.html", {"sfid": sfid, "fc": fc, "count": count})
    else:
        return render(request, "postatt0.html", {"sfid": sfid})


def postatt2(request, dept, ay, yr, sem, cc, fid, sec):
    sfid = request.session["fid"]
    y=RegHistoryM.objects.filter(Q(sdept=dept)&Q(say=ay)&Q(syr=yr)&Q(ssem=sem))
    r=[]
    for i in y:
        if(i.cc1==cc and i.sec1==int(sec) and i.f1==fid):
            r.append(i)

        elif (i.cc2 == cc and i.sec1==int(sec) and i.f2 == fid):
            r.append(i)

        elif (i.cc3 == cc and i.sec3 == int(sec) and i.f3 == fid):
            r.append(i)

        elif (i.cc4 == cc and i.sec4 == int(sec) and i.f4 == fid):
            r.append(i)

        elif (i.cc5 == cc and i.sec5 == int(sec) and i.f5 == fid):
            r.append(i)

        elif (i.cc6 == cc and i.sec6 == int(sec) and i.f6 == fid):
                r.append(i)


        elif (i.cc7 == cc and i.sec7 == int(sec) and i.f7 == fid):
            r.append(i)
        print(r)
    return render(request, "postatt2.html", {"sfid": sfid, "r":r})


#### VIEW FEEDBACKS #####

def fviewfeedback0(request):
    sfid = request.session["fid"]
    f=Faculty.objects.get(facultyid=sfid)
    x=FacultyCourseMapping.objects.filter(faculty=sfid)
    return render(request, "fviewfeedback0.html", {"sfid":sfid, "x":x})


def fviewfeedback1(request, cc, ay, yr, sem, sec):
    sfid = request.session["fid"]
    x=RegHistoryM.objects.filter(Q(say=ay)&Q(syr=yr)&Q(ssem=sem))
    stu=[]
    for i in x:
        if(i.cc1.coursecode == cc and i.fcm1.faculty.facultyid == int(sfid) and i.fcm1.section == sec):
            stu.append(i)
        elif(i.cc2.coursecode == cc and i.fcm2.faculty.facultyid == int(sfid) and i.fcm2.section == sec):
            stu.append(i)
        elif(i.cc3.coursecode == cc and i.fcm3.faculty.facultyid == int(sfid) and i.fcm3.section== sec):
            stu.append(i)
        elif(i.cc4.coursecode == cc and i.fcm4.faculty.facultyid == int(sfid) and i.fcm4.section == sec):
            stu.append(i)
        elif(i.cc5.coursecode == cc and i.fcm5.faculty.facultyid == int(sfid) and i.fcm5.section == sec):
            stu.append(i)
        elif(i.cc6.coursecode == cc and i.fcm6.faculty.facultyid == int(sfid) and i.fcm6.section == sec):
            stu.append(i)
        elif(i.cc7.coursecode == cc and i.fcm7.faculty.facultyid == int(sfid) and i.fcm7.section == sec):
            stu.append(i)
    c1=len(stu)
    y = FeedbackPosted.objects.filter(Q(ccode=cc) & Q(section=sec) & Q(fid=sfid) & Q(say=ay) & Q(syr=yr) & Q(ssem=sem))
    c2=len(y)
    return render(request, "fviewfeedback1.html", {"y":y, "sfid":sfid, "ay":ay, "yr":yr, "sem":sem, "sec":sec, "cc":cc, "c1":c1, "c2":c2})

def fviewfeedback2(request, q, ay, yr, sem, fid, cc, sec, c1, c2):
    sfid = request.session["fid"]
    q = int(q)
    mp = {}
    y = FeedbackPosted.objects.filter(Q(ccode=cc)& Q(say=ay) & Q(syr=int(yr)) & Q(ssem=sem)& Q(fid=int(fid)) & Q(section=int(sec)))
    for i in y:
        if q == 1:
            for j in i.fdb1_options:
                if j[0] == i.fdb1:
                    mp[j[0]] = mp.get(j[0], 0) + 1
                else:
                    mp[j[0]] = mp.get(j[0], 0)

        elif q == 2:
            for j in i.fdb2_options:
                if j[0] == i.fdb2:
                    mp[j[0]] = mp.get(j[0], 0) + 1
                else:
                    mp[j[0]] = mp.get(j[0], 0)

        elif q == 3:
            for j in i.fdb3_options:
                if j[0] == i.fdb3:
                    mp[j[0]] = mp.get(j[0], 0) + 1
                else:
                    mp[j[0]] = mp.get(j[0], 0)

        elif q == 4:
            for j in i.fdb4_options:
                if j[0] == i.fdb4:
                    mp[j[0]] = mp.get(j[0], 0) + 1
                else:
                    mp[j[0]] = mp.get(j[0], 0)

        elif q == 5:
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
    return render(request, "fviewfeedback1.html",{"y": y, "sfid": sfid, "ay": ay, "yr": yr, "sem": sem, "sec": sec, "cc": cc, "c1":c1, "c2":c2})



##### FACULTY POSTING INTERNALS #######
def fpostintcc0(request):
    sfid=request.session["fid"]
    x=FacultyCourseMapping.objects.filter(faculty=sfid)
    return render(request, "fpostintcc0.html", {"sfid":sfid, "x":x})

def fpostintcc1(request, c,ccode, ayr,y, sm, ft):
    sfid = request.session["fid"]

    h=CC.objects.filter(Q(cc = int(c))&Q(ay=ayr)&Q(yr=int(y))&Q(sem=sm)&Q(fid=int(ft)))
    if h:
        #return HttpResponse("hi")
        return render(request, "fpostintcc1.html", {"sfid":sfid, "c":c,"ccode":ccode, "ay":ayr, "yr": y, "sem":sm})
    else:
        msg="Only Course Cordinator are given access or you might not be granted permission"
        return render(request, "facultyhome.html", {"msg": msg})



def fpostintcc2(request):
    sfid = request.session["fid"]
    p=request.POST["sd"]
    print(p)
    a=request.POST["sno"]
    b=request.POST["fid"]
    c=request.POST["ayr"]
    d=request.POST["y"]
    e=request.POST["sm"]
    CC.objects.filter(Q(cc=a)&Q(fid=sfid)&Q(ay=c)&Q(yr=int(d))&Q(sem=e)).update(post=p)
    msg="Posting Internals has been Updated"
    return render(request, "facultyhome.html", {"msg":msg})

def fpostint0(request,sec,dept,ctitle, c,  ayr, y, sm):
    sfid = request.session["fid"]

    try:
        k = CC.objects.get(Q(ay=ayr) & Q(yr=y) & Q(sem=sm) & Q(cc=c))
        if(k.post == 1):
            return redirect("fpostint1",sec=sec,  dept=dept, ct=ctitle, c=c, ay=ayr, yr=y, sem=sm)
            #return HttpResponse("granted")
        else:
            msg="CC need to Grant Access To Post Internals"
            return render(request, "facultyhome.html", {"sfid":sfid, "msg":msg})
    except ObjectDoesNotExist:
        msg = f'CC need to Grant Access To Post Internals'
        return render(request, "facultyhome.html", {"sfid": sfid, "msg": msg})

def fpostint1(request,sec,dept,ct, c,  ay, yr, sem):
    sfid = request.session["fid"]
    fid=int(sfid)


    '''print(type(fid))
    print(sec)
    print(dept)
    print(ct)
    print(c)
    print(type(ay))
    print(type(yr))
    print(type(sem))'''

    x = RegHistoryM.objects.filter(Q(say=ay) & Q(sdept=dept) & Q(syr=yr) & Q(ssem=sem) )

    r = []
    for i in x:

        if (i.cc1.coursecode == ct and i.fcm1.faculty.facultyid == fid):
            r.append(i)
        elif (i.cc2 and i.cc2.coursecode == ct and i.fcm2.faculty.facultyid == fid):
            r.append(i)

        elif (i.cc3 and i.cc3.coursecode == ct and i.fcm3.faculty.facultyid == fid):
            r.append(i)

        elif (i.cc4 and i.cc4.coursecode == ct and i.fcm4.faculty.facultyid == fid):
            r.append(i)

        elif (i.cc5 and i.cc5.coursecode == ct and i.fcm5.faculty.facultyid == fid):
            r.append(i)

        elif (i.cc6 and i.cc6.coursecode == ct and i.fcm6.faculty.facultyid == fid):
            r.append(i)

        elif (i.cc7 and i.cc7.coursecode == ct and i.fcm7.faculty.facultyid == fid):
            r.append(i)
    return render(request, "fpostint2.html", {"r":r, "sfid":sfid,"dept":dept, "ct":ct, "c":c, "ay":ay, "yr":yr, "sem":sem, "sec":sec})


    #return redirect("viewfstudents3",  dept, ay, yr, sem, ct, fid)

def fpostint2(request,sid, dept, ay, yr, sem, c, ct, sec):
    sfid = request.session["fid"]
    try:
      x=Internals.objects.get(Q(fid=sfid)&Q(sid=sid)&Q(ay=ay)&Q(yr=yr)&Q(sem=sem)&Q(cc=ct)&Q(sec=sec))
      flag=1
    except ObjectDoesNotExist:
       flag=0
       x=0

    return render(request, "fpostint3.html",{"sfid": sfid,"sid":sid, "sec" :sec, "dept": dept, "ct": ct, "c": c, "ay": ay, "yr": yr, "sem": sem, "x":x, "flag":flag})


def fpostint3(request):
    sfid = request.session["fid"]
    if request.method =="POST":
        fid = int(sfid)
        dept = request.POST["dept"]
        ay = request.POST["ay"]
        yr = request.POST["yr"]
        sem = request.POST["sem"]
        sid = request.POST["sid"]
        c = request.POST["c"]
        ct = request.POST["ct"]
        sec = request.POST["sec"]
        it = Internals.objects.filter(
            Q(sid=sid) & Q(fid=fid) & Q(dept=dept) & Q(ay=ay) & Q(yr=yr) & Q(sem=sem) & Q(cid=c) & Q(cc=ct) & Q(sec=sec))
        try:
            x = Internals.objects.get(
                Q(sid=sid) & Q(fid=fid) & Q(dept=dept) & Q(ay=ay) & Q(yr=yr) & Q(sem=sem) & Q(cid=c) & Q(cc=ct) & Q(sec=sec))
            flag=1
        except ObjectDoesNotExist:
            flag=0


        sem1 = float(request.POST["sem1"]) if request.POST["sem1"] else (x.sem1 if it else 0.0)
        sem2 = float(request.POST["sem2"]) if request.POST["sem2"] else (x.sem2 if it else 0.0)
        lab1 = float(request.POST["lab1"]) if request.POST["lab1"] else (x.lab1 if it else 0.0)
        quiz1 = float(request.POST["quiz1"]) if request.POST["quiz1"] else (x.quiz1 if it else 0.0)
        quiz2 = float(request.POST["quiz2"]) if request.POST["quiz2"] else (x.quiz2 if it else 0.0)
        quiz3 = float(request.POST["quiz3"]) if request.POST["quiz3"] else (x.quiz3 if it else 0.0)
        quiz4 = float(request.POST["quiz4"]) if request.POST["quiz4"] else (x.quiz4 if it else 0.0)
        semend = float(request.POST["semend"]) if request.POST["semend"] else (x.semend if it else 0.0)
        labend = float(request.POST["labend"]) if request.POST["labend"] else (x.labend if it else 0.0)
        gp = float(request.POST["gp"]) if request.POST["gp"] else (x.grade_points if it else 0.0)
        g = request.POST["g"]

        if flag == 1:
                x.sem1 = sem1
                x.sem2 = sem2
                x.lab1 = lab1
                x.quiz1 = quiz1
                x.quiz2 = quiz2
                x.quiz3 = quiz3
                x.quiz4 = quiz4
                x.semend = semend
                x.labend = labend
                x.grade_points = gp
                x.grade = g
                x.save()
        else:
                Internals.objects.create(
                    sid=sid, fid=fid, dept=dept, ay=ay, yr=yr, sem=sem, cid=c, cc=ct, sec=sec,
                    sem1=sem1, sem2=sem2, lab1=lab1, quiz1=quiz1, quiz2=quiz2, quiz3=quiz3, quiz4=quiz4,
                    semend=semend, labend=labend, grade_points=gp, grade=g
                )

        x = Faculty.objects.get(facultyid=fid)
        y = Student.objects.get(studentid=sid)
        email = settings.EMAIL_HOST_USER
        faculty_email = x.email
        student_email = y.email
        subject = "Internal Marks Posted"
        message = f"Dear {y.fullname},\n\nYour internal marks for the course {ct} have been posted by the faculty bearing ID no: {x.facultyid} and Name: {x.fullname}.\n\nBest regards,\n Team SCMS."

        m2 = f"Dear {x.fullname},\n\nYou have posted internal marks for the course {ct} to the student bearing ID no: {y.studentid}.\n\nBest regards,\n Team SCMS."

        '''send_mail(subject, message, email, [student_email], reply_to=[faculty_email])
        send_mail(subject, m2, email, [faculty_email], reply_to=[student_email])'''

        email1 = EmailMessage(
            subject,
            message,
            email,
            [student_email],
            reply_to=[faculty_email]
        )
        email1.send(fail_silently=False)

        email2 = EmailMessage(
            subject,
            m2,
            email,
            [faculty_email],
            reply_to=[student_email]
        )
        email2.send(fail_silently=False)

        '''msg = "Uploaded Internals and Email Sent Successfully!"
            except socket.gaierror as e:
                msg = f"Uploaded Internals but failed to send email due to DNS resolution error: {e}"
                print(msg)
            except Exception as e:
                msg = f"Uploaded Internals but failed to send email due to an unexpected error: {e}"
                print(msg)
        '''

        #return redirect("fpostintcc0")

        #send_mail(subject, m2, email, [faculty_email], fail_silently = False)
            #email2.send(fail_silently = False)
        msg = "Uploaded Internals and Email Sent Successfully!"
        '''except Exception as e:
            msg = f"Uploaded Internals but failed to send email: {e}" '''
        return redirect("fpostint1", int(sec), dept, ct, c, ay, yr, sem)
    else:
        return redirect("fpostintcc0")



#############################################################################################

## faculty handout

def fhandout0(request):
    sfid = request.session["fid"]
    x=Faculty.objects.get(facultyid=sfid)
    y=FacultyCourseMapping.objects.filter(faculty=x)
    return render(request, "fhandout1.html", {"sfid":sfid, "y":y})

def fhandoutadd(request, fid, cid, type):
    sfid = request.session["fid"]
    if(type == "True"):
        cid=int(cid)
        x=Faculty.objects.get(facultyid=fid)
        y=Course.objects.get(id=cid)

        try:
            z=Handout.objects.get(Q(fid=x)&Q(cid=y))
            msg="Already handout added"
            return render(request, "facultyhome.html",{"msg":msg})
        except Handout.DoesNotExist:
            p=HandoutForm()
            return render(request, "faddhandout.html",{"p":p, "sfid":sfid, "y":y})
    else:
        msg = "Only CC can add handout"
        return render(request, "facultyhome.html", {"msg": msg, "sfid":sfid})

def fhandoutadd1(request):
    sfid = request.session["fid"]
    if(request.method == "POST"):
        x=request.POST["fid"]
        y=request.POST["cid"]
        a=Faculty.objects.get(facultyid=x)
        b=Course.objects.get(id=y)
        file = request.FILES["file"]
        upload = Handout(fid=a, cid=b, hd=file)
        upload.save()
        msg="Uploaded File Successfully ! "
        return render(request, "facultyhome.html", {"sfid":sfid, "msg":msg})


###### to view handouts ######
def fhandoutview(request, cid, fid):
    sfid = request.session["fid"]
    x = Faculty.objects.get(facultyid=fid)
    y = Course.objects.get(id=cid)
    try:
        z=Handout.objects.get(fid=x, cid=y)
        return render(request, "fhandoutview.html", {"z":z})
    except ObjectDoesNotExist:
        msg=f'No Handout Added for {y.coursecode} - {y.coursetitle} '
        return render(request, "facultyhome.html", {"msg":msg, "sfid":sfid})

def fhandoutdel(request, cid, fid):
    sfid = request.session["fid"]
    x=Faculty.objects.get(facultyid=fid)
    y=Course.objects.get(id=cid)
    p=FacultyCourseMapping.objects.get(Q(course=y)&Q(faculty=x))
    if(p.type == True):
        try:
            z=Handout.objects.get(Q(fid=x)&Q(cid=y))
            filepath=z.hd.path
            print(filepath)
            if(default_storage.exists(filepath)):
                default_storage.delete(filepath)
            z.delete()
            msg="Handout deleted Successfully"
            return render(request, "facultyhome.html", {"sfid":sfid, "msg":msg})
        except ObjectDoesNotExist:
            msg="No Handout Uploaded ! "
            return render(request, "facultyhome.html", {"sfid":sfid, "msg":msg})
    else:
        msg="Only CC can modify the handout ! "
        return render(request, "facultyhome.html", {"sfid": sfid, "msg": msg})

#### faculty home - data addon/update
def ffhome(request):
    sfid = request.session["fid"]
    f=Faculty.objects.get(facultyid=sfid)
    if f.access == 1:
        return render(request, "ffhome.html", {"sfid": sfid})
    else:
        msg = "Access Denied"
        return render(request, "facultyhome.html", {"sfid": sfid, "msg": msg})


####### faculty access to add faculty - flag=1
def faddfaculty(request):
    sfid = request.session["fid"]
    x = Faculty.objects.get(facultyid=sfid)
    form = AddFacultyForm()
    if request.method == "POST":
            form1 = AddFacultyForm(request.POST)
            if form1.is_valid():
                form1.save()
                msg = "Faculty added successfully"
                subject = "Welcome to SCMS UNIVERSITY - FACULTY TEAM"
                message = f'Dear {form1.fullname}, \n Congratulations and Welcome to SCMS UNIVERSITY. \n We are delighted to have you join our esteemed faculty team. Your registration has been successfully completed, and we look forward to your contributions to our academic community.\n NOTE: Your UNIVERSITY ID NUMBER: {form1.studentid}, DEFAULT PASSWORD: {form1.password}.\n Modify Your Password for better security. \n Thaank You\n Team SCMS.'
                email = settings.EMAIL_HOST_USER
                recipients = [form1.email]
                send_mail(subject, message, email, recipients)
                return render(request, "facultyhome.html", {"msg": msg, "sfid": sfid})
                return render(request, 'facultyhome.html', {"msg": msg, "sfid":sfid})
            else:
                msg = "Failed to add Data"
                return render(request, "faddfaculty.html", {"msg": msg})

    return render(request, "faddfaculty.html", {"form": form})


####### faculty update access -1

def fviewfaculty(request):
    sfid = request.session["fid"]
    x=Faculty.objects.all()
    return render(request, "fviewfaculty.html", {"facultydata": x, "sfid": sfid})

def fupdatefaculty(request, fid):
    sfid = request.session["fid"]
    f = Faculty.objects.get(facultyid=fid)
    if request.method == "POST":
        form = FacultyUpdateForm(request.POST, instance=f)
        if form.is_valid():
            form.save()
            msg="Updated Successfully"
        else:
            msg = "Failed Updating"
        x = Faculty.objects.all()
        return render(request, "fviewfaculty.html", {"msg":msg, "facultydata":x})
    else:
        form = FacultyUpdateForm(instance=f)
        return render(request, "fupdatefaculty.html", {"form": form, "sfid": sfid, "f": f})

##### faculty home -1
def fshome(request):
    sfid = request.session["fid"]
    x=Faculty.objects.get(facultyid=sfid)
    if x.access == 1:
        return render(request, "fshome.html", {"sfid":sfid})
    else:
        msg="Access Denied"
        return render(request,"facultyhome.html", {"sfid":sfid, "msg":msg})

####### adding student  -1
def faddstudent(request):
    sfid = request.session["fid"]
    form = AddStudentForm()

    if request.method == "POST":
        form1 = AddStudentForm(request.POST)
        if form1.is_valid():
            form1.save()
            msg = "insertion done"
            subject="Welcome to SCMS UNIVERSITY - Your Journey Begins Here"
            message =f'Dear {form1.fullname}, \n Congratulations and Welcome to SCMS UNIVERSITY. \nWe are thrilled to have you join our academic community. Your registration for the program {form1.program}, department - {form1.department} has been successfully completed. This is the beginning of an exciting journey, and we are here to support you every step of the way.\n NOTE: Your UNIVERSITY ID NUMBER: {form1.studentid}, DEFAULT PASSWORD: {form1.password}.\n Modify Your Password for better security. \n Thaank You\n Team SCMS.'
            email=settings.EMAIL_HOST_USER
            recipients = [form1.email]
            send_mail(subject, message, email, recipients)
            return render(request, "facultyhome.html", {"msg": msg, "sfid":sfid})
        else:
            msg = "Failed to add Data"
            return render(request, "faddstudent.html", {"msg": msg})

    return render(request, "faddstudent.html", {"form": form})


####### student details updating - 1
def fviewstudents(request):
    sfid = request.session["fid"]
    f=Faculty.objects.get(facultyid=sfid)
    if(request.method == "POST"):
            pgm=request.POST["pgm"]
            dept=request.POST["dept"]
            ay=request.POST["ay"]
            sem=request.POST["sem"]
            x= Student.objects.filter(Q(program=pgm)&Q(department=dept)&Q(ay=ay)&Q(semester=sem))
            return render(request, "fviewstu.html", {"x": x, "sfid": sfid})
    else:
            return render(request, "ffilter.html", {"sfid": sfid})



def fupdatestudent(request, sid):
    sfid = request.session["fid"]
    s = Student.objects.get(studentid=sid)
    if (request.method == "POST"):
        form1 = StudentUpdateForm(request.POST, instance=s)
        if form1.is_valid():
            form1.save()
            msg = "Updated successfully"
        else:
            msg = "Invalid"
        x = Student.objects.filter(Q(program=s.program) & Q(department=s.department) & Q(ay=s.ay) & Q(semester=s.semester))
        return render(request, "fviewstu.html", {"msg": msg, "sfid": sfid, "x":x})

    else:
        form = StudentUpdateForm(instance=s)
        return render(request, "fupdatestudent.html", {"form": form, "sfid": sfid, "s": s})


### faculty grievances adding and viewing his grievances

def fgrievance0(request):
    sfid = request.session["fid"]
    return render(request, "fgr0.html", {"sfid":sfid})

    ### for adding grievance
def fgrievance1(request):
    sfid = request.session["fid"]
    s=Faculty.objects.get(facultyid=sfid)
    x=GrievanceForm()
    if(request.method == "POST"):
        y=GrievanceForm(request.POST)

        grievance = y.save(commit=False)

            # Set additional fields
        grievance.name=s.fullname
        grievance.pid = sfid
        grievance.dept = s.department
        grievance.ay = s.cur_ay
        grievance.sem = s.cur_sem
        grievance.email = s.email
        grievance.date = datetime.now()

            # Save the form to the database
        grievance.save()
        msg="Grievance Submitted Successfully."

        return render(request, "fgr0.html", {"sfid":sfid, "msg":msg})

    else:
        return render(request, "fgr1.html", {"sfid":sfid,"x":x})

     ### for viewing my grievances
def fgrievance2(request):
    sfid = request.session["fid"]
    x=Grievance.objects.filter(pid=sfid)
    if x:
        return render(request, "fgr2.html", {"sfid":sfid, "x":x})
    else:
       msg="You Haven't Submitted Any Grievances"
       return render(request, "fgr0.html", {"sfid":sfid, "msg":msg})


#### faculty given acccess to view student grievances


def fgroth(request):
    sfid=request.session["fid"]
    x=Faculty.objects.get(facultyid=sfid)
    if(x.graccess == 1):
        return redirect('fviewgrievance0')
    else:
        msg="Access Denied"
        return render(request, "fgr0.html", {"sfid":sfid, "msg":msg})
def fviewgrievance0(request):
    sfid = request.session["fid"]
    return render(request, "fviewgr0.html", {"sfid":sfid})
def fviewgrievance1(request):
    sfid = request.session["fid"]
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
        return render(request, "fviewgr1.html",{"sfid":sfid, "lt":lt})
    else:
        msg="No Grievances Posted"
        return render(request, "fviewgr0.html", {"sfid":sfid, "msg":msg})


def fviewgrievance2(request):
    sfid = request.session["fid"]
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
      return render(request, "fviewgr1.html",{"sfid":sfid, "lt":lt})
    else:
        msg="No Grievances Posted"
        return render(request, "fviewgr0.html", {"sfid":sfid, "msg":msg})

def fviewgrissuestu(request, id):
    sfid = request.session["fid"]
    x=Grievance.objects.get(id=id)
    x.status=1
    x.save()
    return render(request, "fviewgrissue.html", {"sfid":sfid, "x":x})

def fupdate_issue_status(request, id):
    sfid = request.session["fid"]
    x=Grievance.objects.get(id=id)
    if x.status ==1:
      x.solved=1
      x.solvedby=sfid
      x.save()
      subject="Grievance Posted Has Been Solved"
      message = f'Dear {x.name}\n,The issue which has been posted by you regarding "{x.category}", - "{x.issue}" at {x.date} has been solved by the university team.If it has not been solved and marked as solved you can contact the administration team at room no: C325.\nThank you\nTeam SCMS.'

      # Convert the HTML message to a plain text alternative (optional but recommended)
      plain_message = strip_tags(message)
      email=settings.EMAIL_HOST_USER
      rec={x.email}
      send_mail(subject, message, email, rec)


    referer = request.META.get('HTTP_REFERER')
    print(referer)

    return redirect(referer)