from django.urls import path
from .views import PaymentSuccess

urlpatterns=[
    path('success/',PaymentSuccess.as_view(), name='payment'),

]