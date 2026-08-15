from django.urls import path

from . import views

urlpatterns = [
    path('', views.dashboard, name='member_dashboard'),
    path('card/', views.membership_card, name='membership_card'),
    path('card/qr.png', views.membership_card_qr, name='membership_card_qr'),
]
