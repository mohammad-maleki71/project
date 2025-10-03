from django.urls import path
from . import views

app_name = 'account'
urlpatterns = [
    path('register/', views.UserRegistrationView.as_view(), name='user_register'),
    path('verify/', views.VerifyCodeView.as_view(), name='verify_code'),
]