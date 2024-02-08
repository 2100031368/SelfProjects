
from django.urls import path, include
from . import views # . represent current directory
urlpatterns = [
   path("adminhome", views.adminhome, name="adminhome"),

   path("adminLogout", views.adminLogOut,name="AdminLogout"),
   path("checkadminlogin", views.checkadminlogin, name="checkadminlogin"),
   path("adminchangepwd", views.adminchangepwd, name="adminchangepwd"),
   path("adminpwdupdt", views.adminpwdupdt,name="adminpwdupdt"),

   path("adminstudent", views.adminstudent, name="adminstudent"),
   path("viewstudents", views.viewstudents, name="viewstudents"),
   path("addstudent", views.addstudent, name="addstudent"),
   path("deletestudent", views.deletestudent, name="deletestudent"),
   path("studentdeletion/<int:sid>", views.studentdeletion, name="studentdeletion"),
   path("updatestudent1", views.updatestudent1, name="updatestudent1"),
   path("updatestudent2/<slug:sid>", views.updatestudent2, name="updatestudent2"),

   path("admincourse", views.admincourse, name="admincourse"),
   path("viewcourses", views.viewcourses, name="viewcourses"),
   path("addcourse", views.addcourse, name="addcourse"),
   path("insertcourse", views.insertcourse, name="insertcourse"),
   path("deletecourse", views.deletecourse, name="deletecourse"),
   path("coursedeletion/<int:cid>", views.coursedeletion, name="coursedeletion"),
   path("updatecourse1", views.updatecourse1, name="updatecourse1"),
   path("updatecourse2",views.updatecourse2, name="updatecourse2"),
   path("updatecourse3", views.updatecourse3, name="updatecourse3"),

   path("facultycoursemapping", views.facultycoursemapping, name="facultycoursemapping"),
   path("addfacultycourse", views.addfacultycourse, name="addfacultycourse"),


   path("adminfaculty", views.adminfaculty, name="adminfaculty"),
   path("viewfaculty", views.viewfaculty, name="viewfaculty"),
   path("addfaculty", views.addfaculty, name="addfaculty"),
   path("deletefaculty", views.deletefaculty, name="deletefaculty"),
   path("facultydeletion/<int:fid>", views.facultydeletion, name="facultydeletion"),
   path("updatefaculty1", views.updatefaculty1, name="updatefaculty1"),
   path("updatefaculty2/<slug:fid>", views.updatefaculty2, name="updatefaculty2"),

   path("regadmin1", views.regadmin1, name="regadmin1"),
   path("regadmin2", views.regadmin2, name="regadmin2"),
   path("history/<str:id>/<str:ay>/<str:yr>/<str:sem>", views.history, name="history"),

   path("regadmin4/<str:dept>/<str:ay>/<str:yr>/<str:sem>", views.regadmin4, name="regadmin4"),
   path("regadmin5", views.regadmin5, name="regadmin5"),

   path("aviewfeedback0", views.aviewfeedback0, name="aviewfeedback0"),
   path("aviewfeedback1/<str:ay>/<int:yr>/<str:sem>/<str:dept>/<int:fid>/<str:cc>/<int:sec>", views.aviewfeedback1, name="aviewfeedback1"),
   path("aviewfeedback2/<int:sid>/<int:fid>/<str:ay>/<int:yr>/<str:sem>/<str:cc>/<int:sec>", views.aviewfeedback2, name="aviewfeedback2"),
   path("aviewfeedback3/<str:ay>/<int:yr>/<str:sem>/<str:dept>/<int:fid>/<str:cc>/<int:sec>", views.aviewfeedback3, name="aviewfeedback3"),
   path("aviewfeedback4/<int:q>/<str:ay>/<int:yr>/<str:sem>/<str:dept>/<int:fid>/<str:cc>/<int:sec>", views.aviewfeedback4, name="aviewfeedback4"),

   path("addcc0", views.addcc0, name="addcc0"),
   path("addcc1/<int:fid>/<int:cc>/<str:ay>/<int:yr>/<str:sem>",views.addcc1, name="addcc1"),
   path("addcc2", views.addcc2, name="addcc2"),
]