from django.urls import path
from . import views

urlpatterns = [
<<<<<<< HEAD
    path('about', views.about),
    path('', views.homepage),
=======
    path('about', views.about, name="about"),
    path('', views.homepage),
    path('student/', views.student_index, name='student_index'),
    path('student/create/', views.student_create, name='student_create'),# Create
>>>>>>> 2c709c3 (Review 4)
]