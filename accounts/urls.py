from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),#the first urgument we need to apss to path is the route, then the views and then we can also name a path 
    path('verify-account/', views.verify_account, name='verify_account'),
    path('login/', views.login, name='login'),
    path('forgot-password/', views.send_password_reset_link, name='reset_password_via_email'),
    path('verify-password-reset-link/', views.verify_password_reset_link, name= 'verify_password_reset_link'),
    path('set-new-password/', views.set_new_password_using_reset_link, name='set_new_password'),
    path('logout/', views.logout, name='logout'),
    
]

