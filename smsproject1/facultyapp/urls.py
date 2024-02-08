
from django.urls import path
from . import views # . represent current directory
urlpatterns = [
   path("facultyhome", views.facultyhome, name="facultyhome"),
   path("checkfacultylogin", views.checkfacultylogin, name="checkfacultylogin"),
   path("myfcourses", views.facultycourse, name="facultycourse"),
   path("facultychangepwd", views.facultychangepwd, name="facultychangepwd"),
   path("facultyupdtpwd", views.facultyupdtpwd, name="facultyupdtpwd"),

   path("fccontent0", views.fccontent0, name="fccontent0"),
   path("fccontent1",views.fccontent1, name="fccontent1"),
   path("fccontent2/<str:ccode>",views.fccontent2, name="fccontent2"),
   path("fccontent3", views.fccontent3, name="fccontent3"),
   path("fccontent4/<str:dept>/<str:ay>/<int:yr>/<str:sem>/<str:ccode>", views.fccontent4, name="fccontent4"),
   path("deltemyuploads1/<int:cid>", views.deltemyuploads1, name="deltemyuploads1"),

   path("postatt0",views.postatt0, name="postatt0"),
   path("postatt1", views.postatt1, name="postatt1"),
   path("postatt2/<str:dept>/<str:ay>/<int:yr>/<str:sem>/<str:cc>/<int:fid>/<int:sec>", views.postatt2, name="postatt2"),

   path("viewfstudents1", views.viewfstudents1, name="viewfstudents1"),
   path("viewfstudents2", views.viewfstudents2, name="viewfstudents2"),
   path("viewfstudents3/<str:dept>/<str:ay>/<int:yr>/<str:sem>/<str:ct>/<int:fid>", views.viewfstudents3,name="viewfstudents3"),

   path("fviewfeedback0", views.fviewfeedback0, name="fviewfeedback0"),
   path("fviewfeedback1/<str:cc>/<str:ay>/<int:yr>/<str:sem>/<int:sec>", views.fviewfeedback1, name="fviewfeedback1"),
   path("fviewfeedback2/<str:q>/<str:ay>/<int:yr>/<str:sem>/<str:fid>/<str:cc>/<int:sec>", views.fviewfeedback2, name="fviewfeedback2"),

   path("fpostintcc0", views.fpostintcc0, name="fpostintcc0"),
   path("fpostintcc1/<int:c>/<str:ccode>/<str:ayr>/<int:y>/<str:sm>/<int:ft>", views.fpostintcc1, name="fpostintcc1"),
   path("fpostintcc2", views.fpostintcc2, name="fpostintcc2"),

   path("fpostint0/<int:sec>/<str:dept>/<str:ctitle>/<int:c>/<str:ayr>/<int:y>/<str:sm>", views.fpostint0,name="fpostint0"),
   path("fpostint1/<int:sec>/<str:dept>/<str:ct>/<int:c>/<str:ay>/<int:yr>/<str:sem>", views.fpostint1,name="fpostint1"),
   path("fpostint2/<int:sid>/<str:dept>/<str:ay>/<int:yr>/<str:sem>/<int:c>/<str:ct>/<int:sec>", views.fpostint2, name="fpostint2"),
   path("fpostint3", views.fpostint3,name="fpostint3"),


]
