

from django.urls import path
from . import views # . represent current directory
urlpatterns = [
   path("studenthome", views.studenthome, name="studenthome"),
   path("checkstudentlogin", views.checkstudentlogin, name="checkstudentlogin"),
   path("studentchangepwd", views.studentchangepwd, name="studentchangepwd"),
   path("studentupdtpwd", views.studentupdtpwd, name="studentupdtpwd"),

   path("studentcoursematview0",views.studentcoursematview0, name="studentcoursematview0"),
   path("studentcoursematview1",views.studentcoursematview1, name="studentcoursematview1"),
   path("stmyccontent/<str:cc>/<int:fid>",views.stmyccontent, name="stmyccontent"),

   path("stmyprofile",views.stmyprofile, name="stmyprofile"),

   path("stureg1", views.stureg1, name="stureg1"),
   path("viewreghistory", views.viewreghistory, name="viewreghistory"),

   path("sfeedback0", views.sfeedback0, name="sfeedback0"),
   path("sfeedback1/<str:cc>/<int:fid>/<int:sec>", views.sfeedback1, name="sfeedback1"),
   path("sfeedback2", views.sfeedback2, name="sfeedback2"),

   path("sviewint0", views.sviewint0, name="sviewint0"),
   path("sviewint1/<str:ccode>", views.sviewint1, name="sviewint1"),

   path("sviewhd0",views.sviewhd0, name="sviewhd0"),
   path("sviewhd1",views.sviewhd1, name="sviewhd1"),
   path("sviewhd2/<str:cc>",views.sviewhd2, name="sviewhd2"),
]