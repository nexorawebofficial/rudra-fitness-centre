from django.urls import path

from . import views

app_name = 'management'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('members/', views.member_list, name='members'),
    path('members/<str:member_id>/', views.member_detail, name='member_detail'),
    path('members/<str:member_id>/toggle-active/', views.toggle_member_active, name='toggle_member_active'),
    path('memberships/<int:membership_id>/extend/', views.extend_membership, name='extend_membership'),
    path('memberships/<int:membership_id>/cancel/', views.cancel_membership, name='cancel_membership'),
    path('attendance/', views.attendance_list, name='attendance'),
    path('attendance/record/', views.record_manual_attendance, name='record_manual_attendance'),
    path('enquiries/', views.enquiry_list, name='enquiries'),
    path('enquiries/<int:enquiry_id>/resolve/', views.resolve_enquiry, name='resolve_enquiry'),
]
