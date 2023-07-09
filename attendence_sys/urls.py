from django.urls import path
from django.urls import path
from .views import StudentListView
from .views import deleteStudent
from django.urls import path
from .views import StudentListView, updateStudent
from . import views

urlpatterns = [
    path('', views.home, name = 'home'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('searchattendence/', views.searchAttendence, name='searchattendence'),
    path('account/', views.facultyProfile, name='account'),
    # path('add_student',views.AddStudent,name='add_student'),
    path('add_student/', views.add_student, name='add_student'),
    # path('success/', views.success_view, name='success'),
    path('updateStudentRedirect/', views.updateStudentRedirect, name='updateStudentRedirect'),
    # path('updateStudent/<int:student_id>/', views.updateStudent, name='updateStudent'),
    path('attendence/', views.takeAttendence, name='attendence'),
    path('students/', StudentListView.as_view(), name='student_list'),
    path('delete-student/<int:student_id>/', deleteStudent, name='delete_student'),
    path('students/', StudentListView.as_view(), name='student_list'),
    path('update_student/<int:student_id>/', updateStudent, name='updateStudent'),
    # path('video_feed/', views.videoFeed, name='video_feed'),
    # path('videoFeed/', views.getVideo, name='videoFeed'),
    path('generate_pdf/', views.generate_pdf, name='generate_pdf'),
    # path('mark_attendance/', views.mark_attendance, name='mark_attendance'),
]


