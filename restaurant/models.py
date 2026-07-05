from django.db import models


class User(models.Model):
	full_name = models.CharField(max_length=120)
	email = models.EmailField(unique=True)
	phone = models.CharField(max_length=30)
	mobile = models.CharField(max_length=30, blank=True)
	city = models.CharField(max_length=100)
	country = models.CharField(max_length=100)
	passport_or_id = models.CharField(max_length=80, blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ["full_name"]

	def __str__(self):
		return f"{self.full_name} ({self.email})"


class Booking(models.Model):
	BOOKING_STATUS_PENDING = "pending"
	BOOKING_STATUS_CONFIRMED = "confirmed"
	BOOKING_STATUS_CANCELLED = "cancelled"

	PAYMENT_STATUS_UNPAID = "unpaid"
	PAYMENT_STATUS_PENDING = "pending"
	PAYMENT_STATUS_PAID = "paid"

	BOOKING_STATUS_CHOICES = [
		(BOOKING_STATUS_PENDING, "Pending"),
		(BOOKING_STATUS_CONFIRMED, "Confirmed"),
		(BOOKING_STATUS_CANCELLED, "Cancelled"),
	]

	PAYMENT_STATUS_CHOICES = [
		(PAYMENT_STATUS_UNPAID, "Unpaid"),
		(PAYMENT_STATUS_PENDING, "Pending Confirmation"),
		(PAYMENT_STATUS_PAID, "Paid"),
	]

	user = models.ForeignKey(
		User,
		on_delete=models.SET_NULL,
		related_name="bookings",
		blank=True,
		null=True,
	)
	full_name = models.CharField(max_length=120)
	email = models.EmailField()
	phone = models.CharField(max_length=30)
	mobile = models.CharField(max_length=30, blank=True)
	city = models.CharField(max_length=100)
	country = models.CharField(max_length=100)

	room_type = models.CharField(max_length=80)
	adults = models.PositiveSmallIntegerField(default=1)
	children = models.PositiveSmallIntegerField(default=0)
	check_in = models.DateField()
	check_out = models.DateField()

	passport_or_id = models.CharField(max_length=80)
	special_requests = models.TextField()

	total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
	booking_status = models.CharField(
		max_length=20,
		choices=BOOKING_STATUS_CHOICES,
		default=BOOKING_STATUS_PENDING,
	)
	payment_status = models.CharField(
		max_length=20,
		choices=PAYMENT_STATUS_CHOICES,
		default=PAYMENT_STATUS_UNPAID,
	)

	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ["-created_at"]

	def __str__(self):
		return f"{self.full_name} - {self.room_type} ({self.check_in})"


class Payment(models.Model):
	METHOD_BANK_TRANSFER = "bank_transfer"
	METHOD_MOBILE_MONEY = "mobile_money"
	METHOD_CASH = "cash"

	PAYMENT_STATUS_PENDING = "pending"
	PAYMENT_STATUS_VERIFIED = "verified"

	PAYMENT_METHOD_CHOICES = [
		(METHOD_BANK_TRANSFER, "Bank Transfer"),
		(METHOD_MOBILE_MONEY, "Mobile Money"),
		(METHOD_CASH, "Cash at Reception"),
	]

	PAYMENT_STATUS_CHOICES = [
		(PAYMENT_STATUS_PENDING, "Pending"),
		(PAYMENT_STATUS_VERIFIED, "Verified"),
	]

	booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name="payments")
	payment_method = models.CharField(max_length=30, choices=PAYMENT_METHOD_CHOICES)
	payer_name = models.CharField(max_length=120)
	amount = models.DecimalField(max_digits=10, decimal_places=2)
	reference_code = models.CharField(max_length=100)
	payment_status = models.CharField(
		max_length=20,
		choices=PAYMENT_STATUS_CHOICES,
		default=PAYMENT_STATUS_PENDING,
	)
	notes = models.TextField(blank=True)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ["-created_at"]

	def __str__(self):
		return f"Payment #{self.id} - {self.booking.full_name}"
