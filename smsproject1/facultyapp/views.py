from django.core.files.storage import default_storage
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect

from adminapp.models import Faculty, FacultyCourseMapping, Course


from regapp.models import RegHistoryM

from .models import CourseContent

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
    print("course title: "+ ct)
    print(fid)
    for i in x:
        print(i.sid )
        print(i.f1)
        print(i.s1)
        if(i.s1==ct):
            print("matched")
        else:
            print(i.s1)
    for i in x:

        if(i.s1 == ct and i.f1 == fid):
            r.append(i)
        elif (i.s2 == ct and i.f2 == fid):
            r.append(i)

        elif (i.s3 == ct and i.f3 == fid):
            r.append(i)

        elif (i.s4 == ct and i.f4 == fid):
            r.append(i)

        elif (i.s5 == ct and i.f5 == fid):
            r.append(i)

        elif (i.s6 == ct and i.f6 == fid):
            r.append(i)

        elif (i.s7 == ct and i.f7 == fid):
            r.append(i)
    print(r)

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






