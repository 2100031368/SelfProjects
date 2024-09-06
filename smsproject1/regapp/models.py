from django.db import models

# Create your models here.

from adminapp.models import FacultyCourseMapping, Course, Student, Faculty

class RegM(models.Model):
    pgm_choices=(("BTECH", "BTECH"), ("MTECH", "MTECH"))
    pgm=models.CharField(blank=False, choices=pgm_choices)
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

    access = models.BooleanField(blank=False)
    class Meta:
        db_table="academic_reg"

    def __str__(self):
        return str(self.sem)

class RegHistoryM(models.Model):
    id=models.AutoField(primary_key=True)
    sid=models.ForeignKey(Student, on_delete=models.CASCADE, null=True, blank=True,)
    sname=models.CharField(blank=False)
    sprogram=models.CharField(blank=False)
    sdept=models.CharField(blank=False)
    say=models.CharField(blank=False)
    syr=models.IntegerField(blank=False)
    ssem=models.CharField(blank=False)

    cc1=models.ForeignKey(Course, on_delete=models.CASCADE, related_name="course1",  null=True, blank=True)
    fcm1=models.ForeignKey(FacultyCourseMapping, on_delete=models.CASCADE, related_name="map1", null=True, blank=True)

    cc2 = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="course2", null=True, blank=True)
    fcm2 = models.ForeignKey(FacultyCourseMapping, on_delete=models.CASCADE, related_name="map2", null=True, blank=True)

    cc3 = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="course3", null=True, blank=True)
    fcm3 = models.ForeignKey(FacultyCourseMapping, on_delete=models.CASCADE, related_name="map3", null=True, blank=True)

    cc4 = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="course4", null=True, blank=True)
    fcm4 = models.ForeignKey(FacultyCourseMapping, on_delete=models.CASCADE, related_name="map4", null=True, blank=True)

    cc5 = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="course5", null=True, blank=True)
    fcm5 = models.ForeignKey(FacultyCourseMapping, on_delete=models.CASCADE, related_name="map5",  null=True, blank=True)

    cc6 = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="course6",  null=True, blank=True)
    fcm6 = models.ForeignKey(FacultyCourseMapping, on_delete=models.CASCADE, related_name="map6",  null=True, blank=True)

    cc7 = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="course7",  null=True, blank=True)
    fcm7 = models.ForeignKey(FacultyCourseMapping, on_delete=models.CASCADE, related_name="map7",  null=True, blank=True)

    class Meta:
        db_table="reg_history"

    def __str__(self):
        return str(self.sid)

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


