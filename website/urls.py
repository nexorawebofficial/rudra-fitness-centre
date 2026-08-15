from django.urls import path

from core.ratelimit import rate_limit

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('trainers/', views.trainers, name='trainers'),
    path('equipment/', views.equipment, name='equipment'),
    path('diet-nutrition/', views.diet_nutrition, name='diet_nutrition'),
    path('diet-nutrition/plan/<int:pk>/', views.diet_plan_detail, name='diet_plan_detail'),
    path('diet-nutrition/<slug:slug>/', views.diet_category_detail, name='diet_category_detail'),
    path('pricing/', views.pricing, name='pricing'),
    path('gallery/', views.gallery, name='gallery'),
    path('testimonials/', views.testimonials, name='testimonials'),
    path('faq/', views.faq, name='faq'),
    path('contact/', rate_limit('contact', max_attempts=10, window_seconds=3600)(views.contact), name='contact'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    path('terms-and-conditions/', views.terms_and_conditions, name='terms_and_conditions'),
    path('offline/', views.offline, name='offline'),
]
