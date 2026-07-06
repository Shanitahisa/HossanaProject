from django.urls import path
from . import views

urlpatterns = [
    path('', views.resortIndex, name='resortIndex'),
    path('resortIndex/', views.resortIndex, name='resortIndex'),
    path('booking/', views.booking, name='booking'),
    path('banquet-booking/', views.banquet_booking, name='banquet_booking'),
    path('banquet-booking/success/<int:booking_id>/', views.banquet_booking_success, name='banquet_booking_success'),
    path('payment/<int:booking_id>/', views.payment, name='payment'),
    path('booking/success/<int:booking_id>/', views.booking_success, name='booking_success'),
    path('staff/', views.staff_login, name='staff_login'),
    path('staff/logout/', views.staff_logout, name='staff_logout'),
    path('staff/dashboard/', views.staff_dashboard, name='staff_dashboard'),
    path('staff/bookings/<int:booking_id>/confirm/', views.confirm_booking, name='confirm_booking'),
    path('staff/banquet-bookings/<int:booking_id>/confirm/', views.confirm_banquet_booking, name='confirm_banquet_booking'),
    
    
]
