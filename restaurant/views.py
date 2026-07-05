from decimal import Decimal

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import BookingForm, PaymentForm
from .models import Booking, Payment, User

# Create your views here.

staff_required = user_passes_test(
    lambda user: user.is_active and user.is_staff,
    login_url="staff_login",
)


def resortIndex(request):
    return render(request, 'index-1.html')


def _calculate_total_amount(room_type, check_in, check_out):
    nightly_rates = {
        "Simple Room": Decimal("200.00"),
        "Simple Duplex": Decimal("300.00"),
        "Deluxe Room": Decimal("380.00"),
        "Exclusive Luxury Room": Decimal("420.00"),
    }
    nights = (check_out - check_in).days
    rate = nightly_rates.get(room_type, Decimal("0.00"))
    return rate * Decimal(nights)


def booking(request):
    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            booking_instance = form.save(commit=False)
            user, _ = User.objects.get_or_create(
                email=booking_instance.email,
                defaults={
                    "full_name": booking_instance.full_name,
                    "phone": booking_instance.phone,
                    "mobile": booking_instance.mobile,
                    "city": booking_instance.city,
                    "country": booking_instance.country,
                    "passport_or_id": booking_instance.passport_or_id,
                },
            )
            user.full_name = booking_instance.full_name
            user.phone = booking_instance.phone
            user.mobile = booking_instance.mobile
            user.city = booking_instance.city
            user.country = booking_instance.country
            user.passport_or_id = booking_instance.passport_or_id
            user.save()

            booking_instance.user = user
            booking_instance.total_amount = _calculate_total_amount(
                booking_instance.room_type,
                booking_instance.check_in,
                booking_instance.check_out,
            )
            booking_instance.save()
            messages.success(request, "Booking details submitted. Continue with payment.")
            return redirect("payment", booking_id=booking_instance.id)
    else:
        form = BookingForm()

    return render(request, "booking.html", {"form": form})


def payment(request, booking_id):
    booking_instance = get_object_or_404(Booking, id=booking_id)

    if request.method == "POST":
        form = PaymentForm(request.POST, booking=booking_instance)
        if form.is_valid():
            payment_instance = form.save(commit=False)
            payment_instance.booking = booking_instance
            payment_instance.payment_status = Payment.PAYMENT_STATUS_PENDING
            payment_instance.save()

            booking_instance.payment_status = Booking.PAYMENT_STATUS_PENDING
            booking_instance.booking_status = Booking.BOOKING_STATUS_PENDING
            booking_instance.save(update_fields=["payment_status", "booking_status", "updated_at"])

            messages.success(request, "Payment details received. We will verify and confirm shortly.")
            return redirect("booking_success", booking_id=booking_instance.id)
    else:
        form = PaymentForm(booking=booking_instance)

    return render(
        request,
        "payment.html",
        {
            "form": form,
            "booking": booking_instance,
        },
    )


def booking_success(request, booking_id):
    booking_instance = get_object_or_404(Booking, id=booking_id)
    latest_payment = booking_instance.payments.first()
    return render(
        request,
        "booking-success.html",
        {
            "booking": booking_instance,
            "payment": latest_payment,
        },
    )


def staff_login(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect("staff_dashboard")

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.is_staff:
                login(request, user)
                return redirect("staff_dashboard")
            form.add_error(None, "This account does not have staff access.")
    else:
        form = AuthenticationForm(request)

    return render(request, "staff-login.html", {"form": form})


@require_POST
def staff_logout(request):
    logout(request)
    messages.success(request, "You have been signed out.")
    return redirect("staff_login")


@staff_required
def staff_dashboard(request):
    bookings = Booking.objects.select_related("user").prefetch_related("payments")
    total_bookings = bookings.count()
    pending_bookings = bookings.filter(booking_status=Booking.BOOKING_STATUS_PENDING).count()
    confirmed_bookings = bookings.filter(booking_status=Booking.BOOKING_STATUS_CONFIRMED).count()
    pending_payments = bookings.filter(payment_status=Booking.PAYMENT_STATUS_PENDING).count()

    return render(
        request,
        "staff-dashboard.html",
        {
            "bookings": bookings,
            "total_bookings": total_bookings,
            "pending_bookings": pending_bookings,
            "confirmed_bookings": confirmed_bookings,
            "pending_payments": pending_payments,
        },
    )


@staff_required
@require_POST
def confirm_booking(request, booking_id):
    booking_instance = get_object_or_404(Booking, id=booking_id)
    latest_payment = booking_instance.payments.first()

    booking_instance.booking_status = Booking.BOOKING_STATUS_CONFIRMED
    if latest_payment:
        latest_payment.payment_status = Payment.PAYMENT_STATUS_VERIFIED
        latest_payment.save(update_fields=["payment_status"])
        booking_instance.payment_status = Booking.PAYMENT_STATUS_PAID
    booking_instance.save(update_fields=["booking_status", "payment_status", "updated_at"])

    messages.success(request, f"Booking #{booking_instance.id} has been confirmed.")
    return redirect("staff_dashboard")
