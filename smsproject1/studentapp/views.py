from datetime import datetime

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect

from adminapp.models import Student,Course, Grievance
from django.urls import reverse

from adminapp.forms import GrievanceForm

from regapp.models import RegM, RegHistoryM, FeedbackPosted, FacultyCourseMapping

from regapp.forms import AddRegForm, FeedbackForm

from facultyapp.models import CourseContent, Internals, Handout

from tenacity import retry, stop_after_attempt, wait_exponential



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
    if(request.method == "POST"):
        sid= request.POST["uid"]
        spwd= request.POST["pwd"]
        try:
            x= Student.objects.get(Q(studentid=sid)&Q(password=spwd))
            if(x.flag ==0):
                request.session["sid"] = sid
                return render(request, "studenthome.html", {"ssid": sid})
            else:
                msg="Access Denied"
                return render(request, "studentlogin.html", {"msg":msg})

        except ObjectDoesNotExist:
            msg = "Login Failed"
            return render(request, "studentlogin.html", {"msg": msg})
    else:
      return render(request, "studentlogin.html")


def studentchangepwd(request):
    ssid=request.session["sid"]
    return render(request, "studentchangepwd.html", {"ssid":ssid})


def studentupdtpwd(request):
    ssid = request.session["sid"]
    if(request.method == "POST"):
        oldpwd=request.POST["opwd"]
        newpwd=request.POST["npwd"]
        flag=Student.objects.filter(Q(studentid=ssid)&Q(password=oldpwd))
        if(flag):
            if(Student.objects.filter(Q(studentid=ssid)&Q(password=newpwd))):
                msg="Old password and New password are same"
            else:
                p=Student.objects.get(studentid=ssid)
                msg="Updated Successfully"
                subject = "Your ERP Password has been Updated"
                message = f'Dear {p.fullname} your ERP Password has been Updated.\n In case if it is not you contact adminstration office cabin C305. \n Meanwhile to block access to your account send email to "bhavanahemasree@gmail.com", so they will stop access to your ERP.After you contacting administration they will update with new password therby you can continue with your account securely.\n ThankYou.\nTeam SCMS. '
                email = settings.EMAIL_HOST_USER
                recepient = [p.email]
                send_mail(subject, message, email, recepient)

                Student.objects.filter(studentid=ssid).update(password=newpwd)
        else:
            msg="Old password entered is not Correct"

        return render(request, "studentchangepwd.html", {"ssid":ssid, "msg":msg})
    else:
        return render(request, "studentchangepwd.html", {"ssid": ssid})

def studentcoursematview1(request):
    ssid = request.session["sid"]
    if request.method == "POST":
        ay = request.POST["ay"]
        sem= request.POST["sem"]
        s = Student.objects.get(studentid=ssid)
        try:
            c=RegHistoryM.objects.get(Q(sid=ssid)&Q(say=ay)&Q(ssem=sem))
            return render(request, "displaystudentcourse.html", {"ssid": ssid, "c": c})
        except ObjectDoesNotExist:
            return render(request, "stufilenotfound.html", {"ssid": ssid})
    else:
        return render(request, "studentcourse.html", {"ssid": ssid})
def stmyccontent(request, cc,fid):
    ssid = request.session["sid"]
    y=Course.objects.get(coursecode=cc)
    x=CourseContent.objects.filter(Q(course=y)&Q(faculty=fid))
    return render(request, "stmyccontent.html", {"ssid":ssid, "x":x})




def stureg1(request):
    ssid = request.session["sid"]
    st=Student.objects.get(studentid=ssid)

    e = RegHistoryM.objects.filter(
        Q(sid=st) & Q(sdept=st.department) & Q(say=st.cur_ay) & Q(syr=st.cur_yr) & Q(ssem=st.cur_sem)).first()
    if e is None:
        if request.method=="POST":

                exist=RegHistoryM(sid=st, sname=st.fullname, sprogram=st.program, sdept=st.department, say=st.cur_ay, syr=st.cur_yr, ssem=st.cur_sem)

                for i in range(1, 8):

                    course = f'c{i}'
                    fcm = f'faculty_c{i}'


                    if course in request.POST and fcm in request.POST:

                        cval = request.POST[course]
                        fcmval=request.POST[fcm]
                        print(cval)
                        print(fcmval)

                        if cval is not 0 and fcmval is not 0 :
                            print("getting into if")
                            course=Course.objects.get(coursecode=cval)
                            fcm=FacultyCourseMapping.objects.get(mappingid=fcmval)

                            setattr(exist, f'cc{i}', course)
                            setattr(exist, f'fcm{i}', fcm)
                exist.save()
                return render(request, "stureg2.html", {"ssid": ssid})


        m=RegM.objects.get(Q(dept=st.department)&Q(pgm=st.program)&Q(ay=st. cur_ay)&Q(sem=st.cur_sem))
        return render(request, "stureg1.html", {"m":m, "ssid":ssid})

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
    try:
        k=FeedbackPosted.objects.get(Q(sid=st.studentid)&Q(fid=fid)&Q(syr=st.cur_yr)&Q(ssem=st.cur_sem))
        msg = "Feedback Already Posted"
        return render(request, "sfeedback0.html", {"ssid": ssid, "msg": msg})

    except ObjectDoesNotExist:
        form = FeedbackForm()
        return render(request, "sfeedback1.html",
                      {"ssid": ssid, "cc": cc, "fid": fid, "sec": sec, "form": form})


def sfeedback2(request, fid,ccode, sec):
    ssid = request.session["sid"]

    #print(f' {ssid} {fid} {prgm} {dept} {say} {syr} {ssem} {ccode} {sec}')\
    st=Student.objects.get(studentid=ssid)

    #h=FeedbackPosted(sid=int(ssid), fid=int(fid), sprogram=st.program, sdept=st.department, say=st.cur_ay, syr=st.cur_yr, ssem=st.cur_sem, ccode=ccode, section=int(sec))
    post_data = request.POST.copy()
    print("hi")
    post_data['sid'] = ssid
    post_data['fid'] = int(fid)
    post_data['sprogram'] = st.program
    post_data['sdept'] = st.department
    post_data['say'] = st.cur_ay
    post_data['syr'] = st.cur_yr
    post_data['ssem'] = st.cur_sem
    post_data['ccode'] = ccode
    post_data['section'] = int(sec)

    print("Post data:", post_data)

    form = FeedbackForm(post_data)

    # Debugging: print form data
    print("Form data:", form.data)

    if(form.is_valid):
        feedback = form.save(commit=False)
        feedback.sid = ssid
        feedback.fid = fid
        feedback.sprogram = st.program
        feedback.sdept = st.department
        feedback.say = st.cur_ay
        feedback.syr = st.cur_yr
        feedback.ssem = st.cur_sem
        feedback.ccode = ccode
        feedback.section = sec
        feedback.save()

        return redirect(reverse('studenthome') + '?msg=Feedback Posted Successfully ')
    else:
        return redirect(reverse('studenthome') + '?msg=Failed in Posting Feedback')


def sviewint0(request):
    ssid = request.session["sid"]
    if(request.method == "POST"):
        ay=request.POST["ay"]
        sem=request.POST["sem"]
        x=RegHistoryM.objects.filter(Q(sid=ssid)&Q(say=ay)&Q(ssem=sem))
        return render(request, "sviewint1.html", {"ssid":ssid, "x":x})
    else:
        return render(request, "sviewint0.html", {"ssid":ssid})

def sviewint1(request, ccode):
    ssid = request.session["sid"]
    y=Internals.objects.filter(Q(sid=ssid)&Q(cc=ccode))
    if y:
        return render(request, "sviewint2.html", {"ssid":ssid, "y":y})
    else:
        msg="No internals are posted yet. "
        return render(request, "sviewint0.html", {"msg":msg})



def sviewhd1(request):
    ssid = request.session["sid"]
    if request.method == "POST":
        ay = request.POST["ay"]
        sem = request.POST["sem"]
        s = Student.objects.get(studentid=ssid)
        try:
            c = RegHistoryM.objects.get(Q(sid=ssid) & Q(say=ay) & Q(ssem=sem))
            return render(request, "sviewhandout1.html", {"ssid": ssid, "c": c})
        except ObjectDoesNotExist:
            return render(request, "stufilenotfound.html", {"ssid": ssid})
    else:
        return render(request, "sviewhandout0.html", {"ssid": ssid})

def sviewhd2(request, cc):
    ssid = request.session["sid"]
    y = Course.objects.get(coursecode=cc)
    try:
        x = Handout.objects.get(cid=y)
        print(x.hd)
        return render(request, "sviewhandout3.html", {"ssid": ssid, "x": x})

    except ObjectDoesNotExist:
        msg="No handout uploaded"
        return render(request, "sviewhandout0.html", {"msg":msg,"ssid":ssid})


######## student submitting issues

def sgrievance0(request):
    ssid = request.session["sid"]
    return render(request, "sgr0.html", {"ssid":ssid})

### for adding grievance
def sgrievance1(request):
    ssid = request.session["sid"]
    s=Student.objects.get(studentid=ssid)
    x=GrievanceForm()
    if(request.method == "POST"):
        y=GrievanceForm(request.POST)
        '''y.pid=s.studentid
        y.prgm=s.program
        y.dept=s.department
        y.ay=s.cur_ay
        y.sem=s.cur_sem'''
        #print(f'details {y.pid} , {y.prgm} , {y.sem}')

        grievance = y.save(commit=False)

            # Set additional fields
        grievance.name=s.fullname
        grievance.pid = ssid
        grievance.prgm = s.program
        grievance.dept = s.department
        grievance.ay = s.cur_ay
        grievance.sem = s.cur_sem
        grievance.email = s.email
        grievance.date = datetime.now()

            # Save the form to the database
        grievance.save()
        msg="Grievance Submitted Successfully."

        return render(request, "sgr0.html", {"sid":ssid, "msg":msg})

    else:
        return render(request, "sgr1.html", {"ssid":ssid,"x":x})

### for viewing my grievances
def sgrievance2(request):
    ssid=request.session["sid"]
    x=Grievance.objects.filter(pid=ssid)
    if x:
        return render(request, "sgr2.html", {"ssid":ssid, "x":x})
    else:
       msg="You Haven't Submitted Any Grievances"
       return render(request, "sgr0.html", {"ssid":ssid, "msg":msg})


### student sgpa
def ssgpa0(request):
    ssid = request.session["sid"]
    if request.method == "POST":
        ay=request.POST["ay"]
        sem=request.POST["sem"]
        s = Student.objects.get(studentid=ssid)
        try:

            x=RegHistoryM.objects.get(Q(say=ay)&Q(ssem = sem)&Q(sid=s))

            y=Course.objects.filter(Q(department=s.department)&Q(program=s.program)&Q(academicyear=ay)&Q(semester=sem))
            q=0
            for i in y:
                q = q + i.credits
            p=Internals.objects.filter(Q(sid=ssid)&Q(dept=s.department)&Q(ay=ay)&Q(sem=sem))
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
                return render(request, "ssgpa1.html", {"msg":msg, "p":p, "cred":cred})
            else:
                return HttpResponse("hi")


        except ObjectDoesNotExist:
            msg="Doesn't Exist"
            return render(request, "studenthome.html", {"ssid":ssid, "msg":msg})
    else:
        return render(request, "ssgpa0.html", {"ssid":ssid})