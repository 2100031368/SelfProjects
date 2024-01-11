from django.db import models

# Create your models here.
class Admin(models.Model):
    id=models.AutoField(primary_key=True)
    username=models.CharField(max_length=100, blank=False, unique=True)
    password=models.CharField(max_length=30, blank=False)

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
        return self.coursetitle

class Student(models.Model):
    #id = models.AutoField(primary_key=True)

    studentid=models.BigIntegerField(blank=False, unique=True, primary_key=True)
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
    email=models.CharField(unique=True, blank=False, max_length=100)
    contact = models.CharField(unique=True, blank=False, max_length=10)

    cur_ay=models.CharField(blank=False, max_length=10)

    cur_yr=models.IntegerField(blank=False)
    sem_choices = (("ODD", "ODD"), ("EVEN", "EVEN"))
    cur_sem = models.CharField(max_length=10, blank=False, choices=sem_choices)

    class Meta:
     db_table ="student_table"

    def __str__(self):
        return str(self.studentid)

class Faculty(models.Model):
   # id = models.AutoField(primary_key=True)
    facultyid=models.BigIntegerField(blank=False, unique=True, primary_key=True)
    fullname = models.CharField(max_length=100, blank=False)

    gender_choices = (("MALE", "MALE"), ("FEMALE", "FEMALE"), ("OTHERS", "OTHERS"))
    gender = models.CharField(max_length=20, blank=False, choices=gender_choices)

    department_choices = (("CSE", "CSE"), ("ECE", "ECE"))
    department = models.CharField(max_length=30, blank=False, choices=department_choices)


    qualification_choices = (("PHD", "PHD"), ("MTECH", "MTECH"))
    qualification=models.CharField(max_length=100, blank=False, choices=qualification_choices)

    designation_choices = (("Prof.", "Professor"), ("Assoc. Prof", "Associate Professor"), ("Asst. Prof", "Assistant Professor"))
    designation=models.CharField(max_length=100, blank=False,choices=designation_choices) #professor, aaatprofessor

    password=models.CharField(blank=False, default="klu123", max_length=30)
    email=models.CharField(unique=True, blank=False, max_length=100)
    contact = models.CharField(unique=True, blank=False, max_length=10)

    class Meta:
     db_table ="faculty_table"

    def __str__(self):
            return str(self.fullname + "-"+self.department)



class FacultyCourseMapping(models.Model):
    mappingid = models.AutoField(primary_key=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE) # object of type Course
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE) # object of type Faculty
    #no need to take care of yr because it is handled in course
    component_choices = (("L", "Lecture"), ("T", "Tutorial"), ("P", "Practical"), ("S", "Skill"))
    component = models.CharField(blank=False, choices=component_choices)
    type = models.BooleanField(blank = False, verbose_name="Faculty Type(CC/Instructor)") #true means main faculty, false means asistence faculty

    section = models.IntegerField(blank= False)
    class Meta:
        db_table="facultycousemapping_table"
    def __str__(self):
        return f'{self.faculty.facultyid}'

    '''
         for above type -- in db it will be as type, so in django admin if u want it to be as
          'Faculty Type(Main/ Assistance)' use verbose_name="Faculty type"
          but after adding verbose_name in db will be as 'type' only
        '''



