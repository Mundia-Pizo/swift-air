from django.urls import path
from .views import RegistrationView, DashBoardView

urlpatterns =[
    path('register/', RegistrationView.as_view(), name='register'),
    path('your-dashboard/', DashBoardView.as_view(), name='dashboard')
]