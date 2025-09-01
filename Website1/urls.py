from django.urls import path
from . import views
app_name = 'Website1'
urlpatterns = [
    path('', views.Course, name='home-page'),
    path('<int:couse_id>/', views.CourseDetails, name='CourseDetails'),
    path('<int:couse_id>/yourchoice/', views.YourChoice, name='YourChoice'),

]

