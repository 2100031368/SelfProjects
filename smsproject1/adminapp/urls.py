
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
   path("updatestudent2/<slug:sid>", views.updatestudent2, name="updatestudent2"),

   path("admincourse", views.admincourse, name="admincourse"),
   path("viewcourses", views.viewcourses, name="viewcourses"),
   path("addcourse", views.addcourse, name="addcourse"),
   path("insertcourse", views.insertcourse, name="insertcourse"),
   path("deletecourse", views.deletecourse, name="deletecourse"),
   path("coursedeletion/<str:ccode>", views.coursedeletion, name="coursedeletion"),
   path("updatecourse1/<str:ccode>",views.updatecourse1, name="updatecourse1"),
   path("updatecourse2", views.updatecourse2, name="updatecourse2"),

   path("facultycoursemapping", views.facultycoursemapping, name="facultycoursemapping"),
   path("addfacultycourse", views.addfacultycourse, name="addfacultycourse"),


   path("adminfaculty", views.adminfaculty, name="adminfaculty"),
   path("viewfaculty", views.viewfaculty, name="viewfaculty"),
   path("addfaculty", views.addfaculty, name="addfaculty"),
   path("deletefaculty", views.deletefaculty, name="deletefaculty"),
   path("facultydeletion/<int:fid>", views.facultydeletion, name="facultydeletion"),
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
   path("aviewfeedback4/<int:q>/<str:ay>/<int:yr>/<str:sem>/<str:dept>/<int:fid>/<str:cc>/<int:sec>/<int:c1>/<int:c2>", views.aviewfeedback4, name="aviewfeedback4"),


   path("agiveaccess0", views.agiveaccess0, name='agiveaccess0'),
   path("agiveaccess1", views.agiveaccess1, name='agiveaccess1'),

   path("astuinternals/<int:sid>", views.astuinternals, name='astuinternals'),
   path("astuinternals2/<int:sid>", views.astuinternals2, name='astuinternals2'),

   path("aviewgrievance0", views.aviewgrievance0, name='aviewgrievance0'),
   path("aviewgrievance1", views.aviewgrievance1, name='aviewgrievance1'),
   path("aviewgrievance2", views.aviewgrievance2, name='aviewgrievance2'),
   path("aviewgrissuestu/<int:id>", views.aviewgrissuestu, name="aviewgrissuestu"),
   path("update_issue_status/<int:id>", views.update_issue_status, name="update_issue_status"),

   path("asgpa0/<int:sid>", views.asgpa0, name="asgpa0"),
]