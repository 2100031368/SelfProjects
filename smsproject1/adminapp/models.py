from datetime import datetime

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

# Create your models here.
class Admin(models.Model):
    id=models.AutoField(primary_key=True)
    username=models.CharField(max_length=100, blank=False, unique=True)
    password=models.CharField(max_length=30, blank=False)
    email=models.EmailField(max_length=40,blank=True)

    class  Meta:
        db_table="admin_table"

    def __str__(self):
      return self.username  # in django admin to display username, return self.id

class Course(models.Model):
    id=models.AutoField(primary_key=True)

    department_choices = (("CSE", "CSE"), ("ECE", "ECE"))
    department = models.CharField(max_length=30, blank=False, choices=department_choices)

    program_choices = (("BTECH", "BTECH"), ("MTECH", "MTECH"))
    program = models.CharField(max_length=100, blank=False, choices=program_choices)

    academic_choices=(("2023-2024", "2023-2024"), ("2022-2023", "2022-2023"))
    academicyear = models.CharField(max_length=30, blank=False, choices=academic_choices)

    sem_choices=(("ODD", "ODD"), ("EVEN", "EVEN"))
    semester = models.CharField(max_length=10, blank=False, choices=sem_choices)

    year = models.IntegerField(blank=False)
    coursecode=models.CharField(max_length=100, blank=False)
    coursetitle=models.CharField(max_length=100, blank=False)

    ltps = models.CharField(max_length=10, blank=False)
    credits = models.FloatField(blank=False)

    class Meta:
        db_table = "course_table"
    def __str__(self):
        return f"{self.coursecode} - {self.coursetitle}"

class Student(models.Model):
    #id = models.AutoField(primary_key=True)

    studentid=models.BigAutoField(primary_key=True)
    fullname = models.CharField(max_length=100, blank=False)

    gender_choices=(("MALE","MALE"), ("FEMALE", "FEMALE"),("OTHERS", "OTHERS"))
    gender=models.CharField(max_length=20, blank=False,choices=gender_choices)

    ay=models.CharField(blank=False, max_length=10)

    department_choices = (("CSE", "CSE"), ("ECE", "ECE"))
    department = models.CharField(max_length=30, blank=False, choices=department_choices)

    program_choices = (("BTECH", "BTECH"), ("MTECH", "MTECH"))
    program=models.CharField(max_length=100, blank=False,choices=program_choices)

    year = models.IntegerField(blank=False)

    sem_choices = (("ODD", "ODD"), ("EVEN", "EVEN"))
    semester = models.CharField(max_length=10, blank=False, choices=sem_choices)

    password=models.CharField(blank=False, default="klu123", max_length=30)
    email=models.EmailField(unique=True, blank=False, max_length=100)
    contact = models.CharField(unique=True, blank=False, max_length=10)

    cur_ay=models.CharField(blank=False, max_length=10)

    cur_yr=models.IntegerField(default=1, blank=False)
    sem_choices = (("ODD", "ODD"), ("EVEN", "EVEN"))
    cur_sem = models.CharField(max_length=10, blank=False, choices=sem_choices)

    flag = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(1)])

    class Meta:
     db_table ="student_table"

    def save(self, *args, **kwargs):
        if not self.studentid:
            last_student = Student.objects.order_by('-studentid').first()
            if last_student:
                self.studentid = last_student.studentid + 1
            else:
                self.studentid = 210001  # Starting point if no students exist yet
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.studentid)

class Faculty(models.Model):
   # id = models.AutoField(primary_key=True)
    facultyid=models.BigAutoField(primary_key=True)
    fullname = models.CharField(max_length=100, blank=False)

    gender_choices = (("MALE", "MALE"), ("FEMALE", "FEMALE"), ("OTHERS", "OTHERS"))
    gender = models.CharField(max_length=20, blank=False, choices=gender_choices)

    department_choices = (("CSE", "CSE"), ("ECE", "ECE"))
    department = models.CharField(max_length=30, blank=False, choices=department_choices)

    ay = models.CharField(blank=False)

    qualification_choices = (("PHD", "PHD"), ("MTECH", "MTECH"))
    qualification=models.CharField(max_length=100, blank=False, choices=qualification_choices)

    designation_choices = (("Prof.", "Professor"), ("Assoc. Prof", "Associate Professor"), ("Asst. Prof", "Assistant Professor"))
    designation=models.CharField(max_length=100, blank=False,choices=designation_choices) #professor, aaatprofessor

    password=models.CharField(blank=False, default="klu123", max_length=30)
    email=models.EmailField(unique=True, blank=False, max_length=100)
    contact = models.CharField(unique=True, blank=False, max_length=10)

    cur_ay=models.CharField(blank=False,default="2023-2024")
    sem_choices = (("ODD", "ODD"), ("EVEN", "EVEN"))
    cur_sem = models.CharField(max_length=10, blank=False, choices=sem_choices, default="ODD")
    resume = models.FileField(blank=True, upload_to='resume/')

    # access to modify students, faculty details
    access =models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(1)])

   # to view grievances
    graccess = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(1)])

   # to enter into their account
    flag = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(1)])
    class Meta:
        db_table ="faculty_table"


    def save(self, *args, **kwargs):
        if not self.facultyid:
            last_faculty = Faculty.objects.order_by('-facultyid').first()
            if last_faculty:
                self.facultyid = last_faculty.facultyid + 1
            else:
                self.facultyid = 1001  # Starting point if no students exist yet
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.facultyid}  - {self.fullname}  - {self.department}"

class FacultyCourseMapping(models.Model):
    mappingid = models.AutoField(primary_key=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE) # object of type Course
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE) # object of type Faculty
    #no need to take care of yr because it is handled in course

    type = models.BooleanField(blank = False, verbose_name="Faculty Type(CC/Instructor)") #true means main faculty, false means asistence faculty

    section = models.IntegerField(blank= False)
    class Meta:
        db_table="facultycousemapping_table"
    def __str__(self):
        return f'{self.faculty.facultyid} - {self.course.coursecode}'

    '''
         for above type -- in db it will be as type, so in django admin if u want it to be as
          'Faculty Type(Main/ Assistance)' use verbose_name="Faculty type"
          but after adding verbose_name in db will be as 'type' only
        '''

class Grievance(models.Model):
    id=models.AutoField(primary_key=True)
    pid=models.IntegerField(blank=False)
    name=models.CharField(blank=False, default='')
    email = models.EmailField(blank=False, default='')
    prgm=models.CharField(blank=True)
    dept=models.CharField(blank=False)
    ay=models.CharField(blank=False)
    sem=models.CharField(blank=False)
    date=models.DateTimeField(blank=False, default=datetime.now)
    cat_choices=(("Hostel", "Hostel"), ("Transport", "Transport"), ("Internet", "Internet"),("Counselling", "Counselling"), ("ClassroomMaintanance", "ClassroomMaintanance"), ("OtherIssues", "OtherIssues"))
    category=models.CharField(blank=False,choices=cat_choices )
    issue=models.CharField(blank=False)
    status = models.BooleanField(default=False)
    solved = models.BooleanField(default=False)
    solvedby=models.IntegerField(blank=False, default=0)

    class Meta:
        db_table = "grievance_table"

    def __str__(self):
        return f'{self.pid}'

