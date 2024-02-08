from django.db import models

# Create your models here.

from adminapp.models import FacultyCourseMapping, Course

class RegM(models.Model):
    dept_choices = (("CSE", "CSE"), ("ECE", "ECE"))
    dept = models.CharField(blank=False, choices=dept_choices)
    ay = models.CharField(blank=False, max_length=10)
    yr = models.IntegerField(blank=False)
    sem_choices = (("ODD", "ODD"), ("EVEN", "EVEN"))
    sem = models.CharField(blank=False, choices=sem_choices)
    c1=models.ForeignKey(Course, on_delete=models.CASCADE, blank=False, related_name="reg_c1")
    f11=models.ForeignKey(FacultyCourseMapping, on_delete=models.CASCADE, blank=False, related_name="reg_f11")
    f12 = models.ForeignKey(FacultyCourseMapping, on_delete=models.CASCADE,null=True, blank=True, related_name="reg_f12")
    f13 = models.ForeignKey(FacultyCourseMapping, on_delete=models.CASCADE,null=True, blank=True, related_name="reg_f13")

    c2=models.ForeignKey(Course, on_delete=models.CASCADE, blank=False, related_name="reg_c2")
    f21=models.ForeignKey(FacultyCourseMapping, on_delete=models.CASCADE, blank=False, related_name="reg_f21")
    f22 = models.ForeignKey(FacultyCourseMapping, on_delete=models.CASCADE,  null=True, blank=True,related_name="reg_f22")
    f23 = models.ForeignKey(FacultyCourseMapping, on_delete=models.CASCADE,null=True, blank=True, related_name="reg_f23")

    c3=models.ForeignKey(Course, on_delete=models.CASCADE, blank=False, related_name="reg_c3")
    f31=models.ForeignKey(FacultyCourseMapping, on_delete=models.CASCADE, blank=False, related_name="reg_f31")
    f32 = models.ForeignKey(FacultyCourseMapping, on_delete=models.CASCADE,null=True, blank=True, related_name="reg_f32")
    f33 = models.ForeignKey(FacultyCourseMapping, on_delete=models.CASCADE,null=True, blank=True, related_name="reg_f33")

    c4=models.ForeignKey(Course, on_delete=models.CASCADE,null=True, blank=True, related_name="reg_c4")
    f41 = models.ForeignKey(FacultyCourseMapping, on_delete=models.CASCADE,null=True, blank=True, related_name="reg_f41")
    f42 = models.ForeignKey(FacultyCourseMapping, on_delete=models.CASCADE,null=True, blank=True, related_name="reg_f42")
    f43 = models.ForeignKey(FacultyCourseMapping, on_delete=models.CASCADE,null=True, blank=True, related_name="reg_f43")

    c5 = models.ForeignKey(Course, on_delete=models.CASCADE,null=True, blank=True, related_name="reg_c5")
    f51 = models.ForeignKey(FacultyCourseMapping, on_delete=models.CASCADE,null=True, blank=True, related_name="reg_f51")
    f52 = models.ForeignKey(FacultyCourseMapping, on_delete=models.CASCADE,null=True, blank=True, related_name="reg_f52")
    f53 = models.ForeignKey(FacultyCourseMapping, on_delete=models.CASCADE,null=True, blank=True, related_name="reg_f53")

    c6 = models.ForeignKey(Course, on_delete=models.CASCADE,null=True, blank=True, related_name="reg_c6")
    f61 = models.ForeignKey(FacultyCourseMapping, on_delete=models.CASCADE,null=True, blank=True, related_name="reg_f61")
    f62 = models.ForeignKey(FacultyCourseMapping, on_delete=models.CASCADE,null=True, blank=True, related_name="reg_f62")
    f63 = models.ForeignKey(FacultyCourseMapping, on_delete=models.CASCADE,null=True, blank=True, related_name="reg_f63")

    c7 = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True,related_name="reg_c7")
    f71 = models.ForeignKey(FacultyCourseMapping, on_delete=models.CASCADE,null=True, blank=True, related_name="reg_f71")
    f72 = models.ForeignKey(FacultyCourseMapping, on_delete=models.CASCADE,null=True, blank=True, related_name="reg_f72")
    f73 = models.ForeignKey(FacultyCourseMapping, on_delete=models.CASCADE,null=True, blank=True, related_name="reg_f73")
    class Meta:
        db_table="academic_reg"

    def __str__(self):
        return self.sem

class RegHistoryM(models.Model):
    id=models.AutoField(primary_key=True)
    sid=models.CharField(blank=False)
    sname=models.CharField(blank=False)
    sprogram=models.CharField(blank=False)
    sdept=models.CharField(blank=False)
    say=models.CharField(blank=False)
    syr=models.IntegerField(blank=False)
    ssem=models.CharField(blank=False)

    cc1=models.CharField(blank=False)
    s1 = models.CharField(blank=False)
    f1 = models.BigIntegerField(blank=False)
    sec1=models.IntegerField(blank=False)

    cc2 = models.CharField(null=True,blank=False)
    s2 = models.CharField(null=True,blank=False)
    f2 = models.BigIntegerField(null=True,blank=False)
    sec2= models.IntegerField(null=True,blank=False)

    cc3 = models.CharField(null=True,blank=False)
    s3 = models.CharField(null=True,blank=False)
    f3 = models.BigIntegerField(null=True,blank=False)
    sec3 = models.IntegerField(null=True,blank=False)

    cc4 = models.CharField(null=True,blank=False)
    s4 = models.CharField(null=True, blank=True)
    f4 = models.BigIntegerField(null=True, blank=True)
    sec4 = models.IntegerField(null=True,blank=False)

    cc5 = models.CharField(null=True,blank=False)
    s5 = models.CharField(null=True, blank=True)
    f5 = models.BigIntegerField(null=True, blank=True)
    sec5 = models.IntegerField(null=True,blank=False)

    cc6 = models.CharField(null=True,blank=False)
    s6 = models.CharField(null=True, blank=True)
    f6 = models.BigIntegerField(null=True, blank=True)
    sec6 = models.IntegerField(null=True,blank=False)

    cc7 = models.CharField(null=True,blank=False)
    s7 = models.CharField(null=True, blank=True)
    f7 = models.BigIntegerField(null=True, blank=True)
    sec7 = models.IntegerField(null=True,blank=False)

    class Meta:
        db_table="reg_history"

    def __str__(self):
        return self.sid

class FeedbackPosted(models.Model):
    id = models.AutoField(primary_key=True)
    sid = models.BigIntegerField(blank=False)
    fid = models.BigIntegerField(blank=False)
    sprogram = models.CharField(blank=False)
    sdept = models.CharField(blank=False)
    say = models.CharField(blank=False)
    syr = models.IntegerField(blank=False)
    ssem = models.CharField(blank=False)

    ccode = models.CharField(blank=False)

    section = models.IntegerField(blank=False)
    q1 = models.CharField(max_length=1000, default="Is the syllabus coverage matching with the lesson plan as on date?")
    fdb1_options=(("100% Matching", "100% Matching"), ("Almost Matching", "Almost Matching"), ("Moderate", "Moderate"), ("Not at all", "Not at all"))
    fdb1=models.CharField(blank=False, choices=fdb1_options)

    q2=models.CharField(max_length=100, default="How well is the teacher able to explain the concept?")
    fdb2_options=(("Excellent ", "Excellent "), ("Very Good", "Very Good"),("Good", "Good"), ("Satisfactory ", "Satisfactory "),("Not-Satisfactory","Not-Satisfactory"))
    fdb2=models.CharField(blank=False, choices=fdb2_options)

    q3 = models.CharField(max_length=100, default="Is the teacher encouraging interaction to get the doubts clarified?")
    fdb3_options = (
    ("Excellent ", "Excellent "), ("Very Good", "Very Good"), ("Good", "Good"), ("Satisfactory ", "Satisfactory "),
    ("Not-Satisfactory", "Not-Satisfactory"))
    fdb3 = models.CharField(blank=False, choices=fdb3_options)

    q4 = models.CharField(max_length=100, default="Whether your teacher is teaching in any other language than English?")
    fdb4_options = (
        ("Never", "Never"), ("Very Rare", "Very Rare"), ("Less frequently", " Less frequently"), ("More frequently", "More frequently"),
        ("All the time", "All the time"))
    fdb4 = models.CharField(blank=False, choices=fdb4_options)

    q5 = models.CharField(max_length=100,
                          default="Overall rating of your teacher.")
    fdb5_options = (
        ("Excellent ", "Excellent "), ("Very Good", "Very Good"), ("Good", "Good"), ("Satisfactory ", "Satisfactory "),
        ("Not-Satisfactory", "Not-Satisfactory"))
    fdb5 = models.CharField(blank=False, choices=fdb5_options)

    class Meta:
        db_table="feedback_posted"
    def __str__(self):
        return str(self.sid)


