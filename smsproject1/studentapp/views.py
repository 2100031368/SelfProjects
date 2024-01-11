from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect

from adminapp.models import Student,Course

from regapp.models import RegM, RegHistoryM, FeedbackPosted

from regapp.forms import AddRegForm, FeedbackForm

from facultyapp.models import CourseContent



# Create your views here.

def studenthome(request):
    ssid = request.session["sid"]
    return render(request, "studenthome.html", {"ssid":ssid})

def stmyprofile(request):
    ssid=request.session["sid"]
    y=Student.objects.get(studentid=ssid)
    print(y)
    return render(request, "stmyprofile.html", {"ssid":ssid,"x":y})

def checkstudentlogin(request):

    sid= request.POST["uid"]
    spwd= request.POST["pwd"]
    flag= Student.objects.filter(Q(studentid=sid)&Q(password=spwd))

    if(flag):
        request.session["sid"] = sid
        return render(request, "studenthome.html", {"ssid": sid})
    else:
        msg = "Login Failed"
        return render(request, "studentlogin.html", {"msg": msg})

def studentchangepwd(request):
    ssid=request.session["sid"]
    return render(request, "studentchangepwd.html", {"ssid":ssid})

def studentupdtpwd(request):
    ssid = request.session["sid"]
    oldpwd=request.POST["opwd"]
    newpwd=request.POST["npwd"]
    flag=Student.objects.filter(Q(studentid=ssid)&Q(password=oldpwd))
    if(flag):
        if(Student.objects.filter(Q(studentid=ssid)&Q(password=newpwd))):
            msg="Old password and New password are same"
        else:
            msg="updated successfully"
            Student.objects.filter(studentid=ssid).update(password=newpwd)
    else:
        msg="Old password entered is not Correct"

    return render(request, "studentchangepwd.html", {"ssid":ssid, "msg":msg})

def studentcourse(request):
    ssid=request.session["sid"]
    return render(request, "studentcourse.html", {"ssid":ssid})

def studentmycourse(request):
    ssid = request.session["sid"]
    ay = request.POST["ay"]
    sem= request.POST["sem"]
    s = Student.objects.get(studentid=ssid)
    c=RegHistoryM.objects.get(Q(sid=ssid)&Q(say=ay)&Q(ssem=sem))


    return render(request, "displaystudentcourse.html", {"ssid": ssid, "c": c})

def stmyccontent(request, cc,fid):
    ssid = request.session["sid"]
    y=Course.objects.get(coursecode=cc)
    x=CourseContent.objects.filter(Q(course=y)&Q(faculty=fid))
    return render(request, "stmyccontent.html", {"ssid":ssid, "x":x})



    '''
    #p=s.department
    p = Student.objects.get(studentid=ssid).department
    print(p)
    h=[]
    for y in c:
        #flag = Course.objects.filter(Q(department=p)&Q(y.semester=sem)&Q(y.academicyear=ay))
        h = Course.objects.filter(Q(semester=sem)&Q(academicyear=ay)&Q(department=p))
        #flag = Course.objects.filter(Q(y.department==p)&Q(y.semester==sem)&Q(y.academicyear==ay))


    return render(request, "displaystudentcourse.html", {"ssid":ssid, "h":h})  '''





'''def studentcourse(request):
    ssid = request.session["sid"]
    st=Student.objects.all()
    ct=Course.objects.all()
    flag1=Student.objects.filter(studentid=ssid)

    z=[]
    for x in st:
        if(x.studentid==int(ssid)):
            z.append(x)

    listofc=[]
    for y in ct:
        c= Course.objects.filter(Q(year=z.year)&Q(semester=z.semester)&Q(program=z.program))
        if(c):
            listofc.append(c)

    return render(request, "studentcourse.html", {"listofc":listofc, "ssid":ssid})


'''



'''def stureg1(request):
    ssid = request.session["sid"]
    form=Reg1()
    if (request.method == "POST"):
        form = Reg1(request.POST)
        s=Student.objects.get(studentid=ssid)

        id = Odd2023CHm.objects.all()
        for x in id:
                print("true")
    return render(request, "stureg1.html", {"ssid": ssid, "form": form})'''

def stureg1(request):
    ssid = request.session["sid"]
    st=Student.objects.get(studentid=ssid)
    ft=RegM.objects.all()
    m=RegM.objects.get(Q(dept=st.department)&Q(ay=st.cur_ay)&Q(sem=st.cur_sem)&Q(yr=st.cur_yr))

    '''e = RegHistoryM.objects.get(
        Q(sid=st.studentid) & Q(sdept=st.department) & Q(say=st.cur_ay) & Q(syr=st.cur_yr) & Q(ssem=st.cur_sem))
        if we take get it wont take None
        '''
    e = RegHistoryM.objects.filter(
        Q(sid=st.studentid) & Q(sdept=st.department) & Q(say=st.cur_ay) & Q(syr=st.cur_yr) & Q(ssem=st.cur_sem)).first()
    if e is None:

        if request.method=="POST":

                exist=RegHistoryM(sid=st.studentid, sname=st.fullname, sprogram=st.program, sdept=st.department, say=st.cur_ay, syr=st.cur_yr, ssem=st.cur_sem)

                for i in range(1, 8):

                    s_key = f'cc{i}'
                    c_key = f'c{i}'
                    f_key = f'faculty_c{i}'
                    sec_key =  f'sec{i}'

                    if s_key in request.POST and c_key in request.POST and f_key in request.POST:

                        s_val = request.POST[s_key]
                        c_val=request.POST[c_key]
                        f_val=request.POST[f_key]
                        sec_val=request.POST[sec_key]


                        if s_val is not None and c_val is not None and f_val is not None and sec_val is not None:
                            print("getting into if")

                            setattr(exist, f'cc{i}', s_val)
                            setattr(exist, f's{i}', c_val)
                            setattr(exist, f'f{i}', f_val)
                            setattr(exist, f'sec{i}', sec_val)
                        else:
                            print("not getting into if")


                exist.save()
                return render(request, "stureg2.html", {"ssid":ssid})
        else:
            return render(request, "stureg1.html", {"m": m, "ssid": ssid})

    else:
        return render(request, "stureg4.html", {"ssid":ssid})


###### view reg history
def viewreghistory(request):
    ssid = request.session["sid"]
    found=RegHistoryM.objects.filter(sid=ssid)

    return render(request, "stureg3.html", {"ssid":ssid, "found":found})

####### give feedback

def sfeedback0(request):
    ssid = request.session["sid"]
    st=Student.objects.get(studentid=ssid)
    fb=RegHistoryM.objects.filter(Q(sid=ssid)&Q(syr=st.cur_yr)&Q(ssem=st.cur_sem))

    return render(request, "sfeedback0.html", {"ssid": ssid, "fb": fb})

def sfeedback1(request, cc, fid, sec):
    ssid = request.session["sid"]
    st=Student.objects.get(studentid=ssid)
    k=FeedbackPosted.objects.get(Q(sid=st.studentid)&Q(fid=fid)&Q(syr=st.cur_yr)&Q(ssem=st.cur_sem))
    if(k is None):
        form=FeedbackForm()

        return render(request, "sfeedback1.html", {"ssid": ssid, "cc":cc, "fid":fid, "sec":sec, "st":st, "form":form})

    else:
        msg="Feedback Already Posted"
        return render(request, "sfeedback0.html", {"ssid":ssid, "msg":msg})

def sfeedback2(request):
    ssid = request.session["sid"]

    form = FeedbackForm(request.POST)
    sid=request.POST["sid"]
    fid=request.POST["fid"]
    prgm=request.POST["sprogram"]
    dept=request.POST["sdept"]
    say=request.POST["say"]
    syr=request.POST["syr"]
    sem=request.POST["ssem"]
    ccode=request.POST["ccode"]
    sec=request.POST["section"]

    print(f' {sid} {fid} {prgm} {dept} {say} {syr} {sem} {ccode} {sec}')

    h=FeedbackPosted(sid=int(sid), fid=int(fid), sprogram=prgm, sdept=dept, say=say, syr=int(syr), ssem=sem, ccode=ccode, section=int(sec))
    if(form.is_valid):
        form.save()
        return HttpResponse("saved")
    else:
        return HttpResponse("wrong")

