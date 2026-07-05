from django.urls import path
from . import views

urlpatterns = [
    path('', views.resortIndex, name='resortIndex'),
    path('resortIndex/', views.resortIndex, name='resortIndex'),
    path('booking/', views.booking, name='booking'),
    path('payment/<int:booking_id>/', views.payment, name='payment'),
    path('booking/success/<int:booking_id>/', views.booking_success, name='booking_success'),
    path('staff/login/', views.staff_login, name='staff_login'),
    path('staff/logout/', views.staff_logout, name='staff_logout'),
    path('staff/dashboard/', views.staff_dashboard, name='staff_dashboard'),
    path('staff/bookings/<int:booking_id>/confirm/', views.confirm_booking, name='confirm_booking'),
    
    
]
