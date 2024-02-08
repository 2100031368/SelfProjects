from django.core.files.storage import default_storage
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect

from adminapp.models import Faculty, FacultyCourseMapping, Course


import matplotlib.pyplot as plt
from regapp.models import RegHistoryM, FeedbackPosted

from .models import CourseContent, CC, Internals

from django.http import FileResponse, Http404
from pathlib import Path



# Create your views here.

def facultyhome(request):
    sfid= request.session["fid"]
    return render(request, "facultyhome.html", {"sfid":sfid})

def checkfacultylogin(request):
    fid=request.POST["uid"]
    fpwd=request.POST["pwd"]
    flag=Faculty.objects.filter(Q(facultyid=fid)&Q(password=fpwd))

    if(flag):
        request.session["fid"]=fid
        return render(request, "facultyhome.html", {"sfid":fid})
    else:
        msg="Login Failed"
        return render(request, "facultylogin.html", {"msg":msg})

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

def facultychangepwd(request):
    sfid = request.session["fid"]
    return render(request, "facultychangepwd.html", {"sfid":sfid})

def facultyupdtpwd(request):
    sfid = request.session["fid"]
    oldpwd=request.POST["opwd"]
    newpwd=request.POST["npwd"]
    flag=Faculty.objects.filter(Q(facultyid=sfid)&Q(password=oldpwd))
    if(flag):
        if(Faculty.objects.filter(password=newpwd)):
            msg="New password is same as Old password"
        else:
            Faculty.objects.filter(facultyid=sfid).update(password=newpwd)
            msg="Updated Successfully"
    else:
        msg="Old password is incorrect"
    return render(request, "facultychangepwd.html", {"msg":msg, "sfid":sfid})

####### faculty uploading content
def fccontent0(request):
    sfid = request.session["fid"]
    return render(request, "fccontent0.html", {"sfid":sfid})

def fccontent1(request):
    sfid=request.session["fid"]

    ay = request.POST["ay"]
    yr = request.POST["yr"]
    sem = request.POST["sem"]
    #c = Course.objects.filter(Q(academicyear=ay)&Q(year=yr)&Q(sem=sem))


    fcm = FacultyCourseMapping.objects.filter(faculty=int(sfid))
    fc = []
    for x in fcm:
        if (x.course.academicyear == ay and x.course.year == int(yr) and x.course.semester == sem):
            fc.append(x)

        else:
            print("not getting into loop")
    print(fc)

    count = len(fc)

    return render(request, "fccontent1.html", {"sfid":sfid, "fc":fc, "count":count})

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
    msg="saved successfully"

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
    return render(request, "fccontent4.html", {"sfid":sfid,"f":f })


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
    return render(request, "viewfstudents1.html", {"sfid":sfid})

def viewfstudents2(request):
    sfid = request.session["fid"]
    ay=request.POST["ay"]
    dept=request.POST["dept"]
    yr=request.POST["yr"]
    sem=request.POST["sem"]
    sec=request.POST["sec"]

    c=Course.objects.all()
    f=Faculty.objects.all()
    x=FacultyCourseMapping.objects.all()
    r=[]
    for i in x:
        if(i.course.department == dept and i.course.academicyear ==ay and i.course.semester == sem and i.course.year == int(yr) and i.faculty.facultyid == int(sfid) and i.section == int(sec)):
            r.append(i)
    print(r)
    return render(request, "viewfstudents2.html", {"sfid":sfid, "r":r})

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

        if(i.cc1 == ct and i.f1 == fid):
            r.append(i)
        elif (i.cc2 == ct and i.f2 == fid):
            r.append(i)

        elif (i.cc3 == ct and i.f3 == fid):
            r.append(i)

        elif (i.cc4 == ct and i.f4 == fid):
            r.append(i)

        elif (i.cc5 == ct and i.f5 == fid):
            r.append(i)

        elif (i.cc6 == ct and i.f6 == fid):
            r.append(i)

        elif (i.cc7 == ct and i.f7 == fid):
            r.append(i)
    #print(r)

    else:
        return render(request, "viewfstudents3.html", {"sfid":sfid,"r":r })


###### posting att

def postatt0(request):
    sfid = request.session["fid"]
    return render(request, "postatt0.html", {"sfid":sfid})


def postatt1(request):
    sfid = request.session["fid"]

    ay = request.POST["ay"]
    yr = request.POST["yr"]
    sem = request.POST["sem"]
    sec = request.POST["sec"]


    fcm = FacultyCourseMapping.objects.filter(faculty=int(sfid))
    fc = []
    for x in fcm:
        if (x.course.academicyear == ay and x.course.year == int(yr) and x.course.semester == sem and x.section == int(sec)):
            fc.append(x)

    print(fc)

    count = len(fc)

    return render(request, "postatt1.html", {"sfid": sfid, "fc": fc, "count": count})

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
    y = FeedbackPosted.objects.filter(Q(ccode=cc) & Q(section=sec) & Q(fid=sfid) & Q(say=ay) & Q(syr=yr) & Q(ssem=sem))
    return render(request, "fviewfeedback1.html", {"y":y, "sfid":sfid, "ay":ay, "yr":yr, "sem":sem, "sec":sec, "cc":cc})

def fviewfeedback2(request, q, ay, yr, sem, fid, cc, sec):
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
    return render(request, "fviewfeedback1.html",{"y": y, "sfid": sfid, "ay": ay, "yr": yr, "sem": sem, "sec": sec, "cc": cc})


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
        return HttpResponse("Only Course Cordinator are given access or you might not be ranted permission")


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

    return HttpResponse("Updated")

def fpostint0(request,sec,dept,ctitle, c,  ayr, y, sm):
    sfid = request.session["fid"]
    k=CC.objects.get(Q(ay=ayr)&Q(yr=y)&Q(sem=sm)&Q(cc=c))
    if k:
        if(k.post == 1):
            return redirect("fpostint1",sec=sec,  dept=dept, ct=ctitle, c=c, ay=ayr, yr=y, sem=sm)
            #return HttpResponse("granted")
        else:
            return HttpResponse("Not Granted")
    else:
        return HttpResponse("admin not undertaken issue")

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
    for j in x:
        print(j.sid)
    r = []
    for i in x:

        if (i.cc1 == ct and i.f1 == fid):
            r.append(i)
        elif (i.cc2 == ct and i.f2 == fid):
            r.append(i)

        elif (i.cc3 == ct and i.f3 == fid):
            r.append(i)

        elif (i.cc4 == ct and i.f4 == fid):
            r.append(i)

        elif (i.cc5 == ct and i.f5 == fid):
            r.append(i)

        elif (i.cc6 == ct and i.f6 == fid):
            r.append(i)

        elif (i.cc7 == ct and i.f7 == fid):
            r.append(i)
    print("r")
    for i in r:
        print(i.sid)

    return render(request, "fpostint2.html", {"r":r, "sfid":sfid,"dept":dept, "ct":ct, "c":c, "ay":ay, "yr":yr, "sem":sem, "sec":sec})


    #return redirect("viewfstudents3",  dept, ay, yr, sem, ct, fid)

def fpostint2(request,sid, dept, ay, yr, sem, c, ct, sec):
    sfid = request.session["fid"]

    '''    print(type(sid))
    print(type(dept))
    print(type(ay))
    print(type(yr))
    print(type(sem))
    print(type(c))
    print(type(ct))
    print(type(sec))
    '''

    return render(request, "fpostint3.html",{"sfid": sfid,"sid":sid, "sec" :sec, "dept": dept, "ct": ct, "c": c, "ay": ay, "yr": yr, "sem": sem})


def fpostint3(request):

    sfid = request.session["fid"]
    fid = int(sfid)
    dept = request.POST["dept"]
    ay = request.POST["ay"]
    yr = request.POST["yr"]
    sem = request.POST["sem"]
    sid = request.POST["sid"]
    c = request.POST["c"]
    ct = request.POST["ct"]
    sec = request.POST["sec"]
    it = Internals.objects.filter(Q(sid=sid) & Q(fid=fid) & Q(dept=dept) & Q(ay=ay) & Q(yr=yr) & Q(sem=sem) & Q(cid=c) & Q(cc=ct) & Q(sec=sec))
    x = Internals.objects.get(Q(sid=sid) & Q(fid=fid) & Q(dept=dept) & Q(ay=ay) & Q(yr=yr) & Q(sem=sem) & Q(cid=c) & Q(cc=ct) & Q(sec=sec))

    sem1 = request.POST["sem1"]
    if sem1:
        sem1 = float(sem1)
    else:
        if it:
            sem1=x.sem1
        else:
            sem1=0.0

    sem2 = request.POST["sem2"]
    if sem2:
        sem2 = float(sem2)
    else:
        if it:
            sem2 = x.sem2
        else:
            sem2 = 0.0

    lab1 = request.POST["lab1"]
    if lab1:
        lab1 = float(lab1)
    else:
        if it:
            lab1 = x.lab1
        else:
            lab1 = 0.0


    quiz1 = request.POST["quiz1"]
    if quiz1:
        quiz1 = float(quiz1)
    else:
        if it:
            quiz1 = x.quiz1
        else:
            quiz1 = 0.0

    quiz2 = request.POST["quiz2"]
    if quiz2:
        quiz2 = float(quiz2)
    else:
        if it:
            quiz2 = x.quiz2
        else:
            quiz2 = 0.0

    quiz3 = request.POST["quiz3"]
    if quiz3:
        quiz3 = float(quiz3)
    else:
        if it:
            quiz3 = x.quiz3
        else:
            quiz3 = 0.0

    quiz4 = request.POST["quiz4"]
    if quiz4:
        quiz4 = float(quiz4)
    else:
        if it:
            quiz4 = x.quiz4
        else:
            quiz4 = 0.0

    semend = request.POST["semend"]
    if semend:
        semend = float(semend)
    else:
        if it:
            semend = x.semend
        else:
            semend = 0.0

    labend = request.POST["labend"]
    if labend:
        labend = float(labend)
    else:
        if it:
            labend = x.labend
        else:
            labend = 0.0

    gp = request.POST["gp"]
    if gp:
        gp = float(semend)
    else:
        if it:
            gp = x.grade_points
        else:
            gp = 0.0

    g = request.POST["g"]

    it = Internals.objects.filter(Q(sid=sid) & Q(fid=fid) & Q(dept=dept) & Q(ay=ay) & Q(yr=yr) & Q(sem=sem) & Q(cid=c) & Q(cc=ct) & Q(sec=sec))
    if it:
        it.update(sem1=sem1, sem2=sem2, lab1=lab1, quiz1=quiz1, quiz2=quiz2, quiz3=quiz3, quiz4=quiz4, semend=semend, labend=labend, grade_points=gp, grade=g)
    else:
        x = Internals(sid=sid, fid=fid, dept=dept, ay=ay, yr=yr, sem=sem, cid=c, cc=ct, sec=sec, sem1=sem1, sem2=sem2, lab1=lab1, quiz1=quiz1, quiz2=quiz2, quiz3=quiz3, quiz4=quiz4, semend=semend, labend=labend, grade_points=gp, grade=g)
        x.save()

    return HttpResponse("helo")
