

from django.urls import path
from . import views # . represent current directory
urlpatterns = [
   path("studenthome", views.studenthome, name="studenthome"),
   path("checkstudentlogin", views.checkstudentlogin, name="checkstudentlogin"),
   path("studentchangepwd", views.studentchangepwd, name="studentchangepwd"),
   path("studentupdtpwd", views.studentupdtpwd, name="studentupdtpwd"),
   path("studentcourse",views.studentcourse, name="studentcourse"),
   path("studentmycourse",views.studentmycourse, name="studentmycourse"),
   path("stmyccontent/<str:cc>/<int:fid>",views.stmyccontent, name="stmyccontent"),

   path("stmyprofile",views.stmyprofile, name="stmyprofile"),

   path("stureg1", views.stureg1, name="stureg1"),
   path("viewreghistory", views.viewreghistory, name="viewreghistory"),

   path("sfeedback0", views.sfeedback0, name="sfeedback0"),
   path("sfeedback1/<str:cc>/<int:fid>/<int:sec>", views.sfeedback1, name="sfeedback1"),
   path("sfeedback2", views.sfeedback2, name="sfeedback2"),

   path("sviewint0", views.sviewint0, name="sviewint0"),
   path("sviewint1/<str:ccode>", views.sviewint1, name="sviewint1"),
]