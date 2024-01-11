
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
]
