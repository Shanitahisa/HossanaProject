from decimal import Decimal

from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone

from .models import Booking, Payment


class BookingForm(forms.ModelForm):
    ROOM_CHOICES = [
        ("Simple Room", "Simple Room ($200/night)"),
        ("Simple Duplex", "Simple Duplex ($300/night)"),
        ("Deluxe Room", "Deluxe Room ($380/night)"),
        ("Exclusive Luxury Room", "Exclusive Luxury Room ($420/night)"),
    ]

    room_type = forms.ChoiceField(choices=ROOM_CHOICES)

    class Meta:
        model = Booking
        fields = [
            "full_name",
            "email",
            "phone",
            "mobile",
            "city",
            "country",
            "room_type",
            "adults",
            "children",
            "check_in",
            "check_out",
            "passport_or_id",
            "special_requests",
        ]
        widgets = {
            "full_name": forms.TextInput(attrs={"class": "validate"}),
            "email": forms.EmailInput(attrs={"class": "validate"}),
            "phone": forms.TextInput(attrs={"class": "validate"}),
            "mobile": forms.TextInput(attrs={"class": "validate"}),
            "city": forms.TextInput(attrs={"class": "validate"}),
            "country": forms.TextInput(attrs={"class": "validate"}),
            "adults": forms.NumberInput(attrs={"min": 1, "max": 10, "class": "validate"}),
            "children": forms.NumberInput(attrs={"min": 0, "max": 10, "class": "validate"}),
            "check_in": forms.DateInput(attrs={"type": "date"}),
            "check_out": forms.DateInput(attrs={"type": "date"}),
            "passport_or_id": forms.TextInput(attrs={"class": "validate"}),
            "special_requests": forms.Textarea(attrs={"class": "materialize-textarea", "rows": 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["room_type"].widget.attrs.update({"class": "browser-default"})

    def clean(self):
        cleaned_data = super().clean()
        check_in = cleaned_data.get("check_in")
        check_out = cleaned_data.get("check_out")
        adults = cleaned_data.get("adults")
        children = cleaned_data.get("children")

        if check_in and check_in < timezone.localdate():
            self.add_error("check_in", "Check-in date cannot be in the past.")

        if check_in and check_out and check_out <= check_in:
            self.add_error("check_out", "Check-out date must be after check-in date.")

        if adults is not None and adults < 1:
            self.add_error("adults", "At least one adult is required.")

        if children is not None and children < 0:
            self.add_error("children", "Children cannot be negative.")

        return cleaned_data


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ["payment_method", "payer_name", "amount", "reference_code", "notes"]
        widgets = {
            "payment_method": forms.Select(attrs={"class": "browser-default"}),
            "payer_name": forms.TextInput(attrs={"class": "validate"}),
            "amount": forms.NumberInput(attrs={"step": "0.01", "min": "0", "class": "validate"}),
            "reference_code": forms.TextInput(attrs={"class": "validate"}),
            "notes": forms.Textarea(attrs={"class": "materialize-textarea", "rows": 4}),
        }

    def __init__(self, *args, booking=None, **kwargs):
        self.booking = booking
        super().__init__(*args, **kwargs)
        if booking:
            self.fields["amount"].initial = booking.total_amount

    def clean_amount(self):
        amount = self.cleaned_data["amount"]
        if amount <= Decimal("0"):
            raise ValidationError("Amount must be greater than zero.")
        return amount
