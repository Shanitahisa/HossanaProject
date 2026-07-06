# Generated manually to add banquet booking requests.

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("restaurant", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="BanquetBooking",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("full_name", models.CharField(max_length=120)),
                ("email", models.EmailField(max_length=254)),
                ("phone", models.CharField(max_length=30)),
                ("mobile", models.CharField(blank=True, max_length=30)),
                ("city", models.CharField(max_length=100)),
                ("country", models.CharField(max_length=100)),
                (
                    "banquet_space",
                    models.CharField(
                        choices=[
                            ("Grand Ball Rooms", "Grand Ball Rooms"),
                            ("Business Meetings", "Business Meetings"),
                            ("Outdoor Event", "Outdoor Event"),
                            ("Social Event", "Social Event"),
                        ],
                        max_length=80,
                    ),
                ),
                ("event_date", models.DateField()),
                ("event_time", models.TimeField()),
                ("guest_count", models.PositiveIntegerField(default=1)),
                ("event_type", models.CharField(max_length=100)),
                ("special_requests", models.TextField(blank=True)),
                (
                    "booking_status",
                    models.CharField(
                        choices=[("pending", "Pending"), ("confirmed", "Confirmed"), ("cancelled", "Cancelled")],
                        default="pending",
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
                        related_name="banquet_bookings",
                        to="restaurant.user",
                    ),
                ),
            ],
            options={"ordering": ["-created_at"]},
        ),
    ]
