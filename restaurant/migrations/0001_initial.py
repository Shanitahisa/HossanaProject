# Generated manually to initialize booking and payment models.

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("full_name", models.CharField(max_length=120)),
                ("email", models.EmailField(max_length=254, unique=True)),
                ("phone", models.CharField(max_length=30)),
                ("mobile", models.CharField(blank=True, max_length=30)),
                ("city", models.CharField(max_length=100)),
                ("country", models.CharField(max_length=100)),
                ("passport_or_id", models.CharField(blank=True, max_length=80)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={"ordering": ["full_name"]},
        ),
        migrations.CreateModel(
            name="Booking",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("full_name", models.CharField(max_length=120)),
                ("email", models.EmailField(max_length=254)),
                ("phone", models.CharField(max_length=30)),
                ("mobile", models.CharField(blank=True, max_length=30)),
                ("city", models.CharField(max_length=100)),
                ("country", models.CharField(max_length=100)),
                ("room_type", models.CharField(max_length=80)),
                ("adults", models.PositiveSmallIntegerField(default=1)),
                ("children", models.PositiveSmallIntegerField(default=0)),
                ("check_in", models.DateField()),
                ("check_out", models.DateField()),
                ("passport_or_id", models.CharField(max_length=80)),
                ("special_requests", models.TextField()),
                ("total_amount", models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                (
                    "booking_status",
                    models.CharField(
                        choices=[("pending", "Pending"), ("confirmed", "Confirmed"), ("cancelled", "Cancelled")],
                        default="pending",
                        max_length=20,
                    ),
                ),
                (
                    "payment_status",
                    models.CharField(
                        choices=[("unpaid", "Unpaid"), ("pending", "Pending Confirmation"), ("paid", "Paid")],
                        default="unpaid",
                        max_length=20,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "user",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="bookings",
                        to="restaurant.user",
                    ),
                ),
            ],
            options={"ordering": ["-created_at"]},
        ),
        migrations.CreateModel(
            name="Payment",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "payment_method",
                    models.CharField(
                        choices=[
                            ("bank_transfer", "Bank Transfer"),
                            ("mobile_money", "Mobile Money"),
                            ("cash", "Cash at Reception"),
                        ],
                        max_length=30,
                    ),
                ),
                ("payer_name", models.CharField(max_length=120)),
                ("amount", models.DecimalField(decimal_places=2, max_digits=10)),
                ("reference_code", models.CharField(max_length=100)),
                (
                    "payment_status",
                    models.CharField(
                        choices=[("pending", "Pending"), ("verified", "Verified")],
                        default="pending",
                        max_length=20,
                    ),
                ),
                ("notes", models.TextField(blank=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "booking",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="payments", to="restaurant.booking"),
                ),
            ],
            options={"ordering": ["-created_at"]},
        ),
    ]
