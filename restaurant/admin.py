from django.contrib import admin
from .models import Booking, Payment, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
	list_display = ("id", "full_name", "email", "phone", "city", "country", "created_at")
	search_fields = ("full_name", "email", "phone", "passport_or_id")
	list_filter = ("country", "city", "created_at")


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
	list_display = (
		"id",
		"user",
		"full_name",
		"room_type",
		"check_in",
		"check_out",
		"booking_status",
		"payment_status",
		"created_at",
	)
	list_filter = ("booking_status", "payment_status", "room_type", "created_at")
	search_fields = ("full_name", "email", "phone", "passport_or_id")


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
	list_display = (
		"id",
		"booking",
		"payment_method",
		"amount",
		"reference_code",
		"payment_status",
		"created_at",
	)
	list_filter = ("payment_method", "payment_status", "created_at")
	search_fields = ("reference_code", "payer_name", "booking__full_name", "booking__email")
