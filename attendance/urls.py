from django.urls import path

from . import views

urlpatterns = [
    path('checkin/<str:token>/', views.checkin_scan, name='checkin_scan'),
]
