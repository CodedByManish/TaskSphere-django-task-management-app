from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('verify/<str:token>/', views.verify_email, name='verify_email'),
    path('verify/', views.email_verification, name='email_verification'),
]