
from django.db import models
from django.core.exceptions import ValidationError
from decimal import Decimal


class Room(models.Model):

    ROOM_TYPES = [
        ('Standard', 'Standard'),
        ('Deluxe', 'Deluxe'),
        ('Suite', 'Suite'),
    ]

    name = models.CharField(max_length=100)

    room_type = models.CharField(
        max_length=20,
        choices=ROOM_TYPES
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    capacity = models.PositiveIntegerField()

    description = models.TextField()

    image = models.ImageField(
        upload_to='rooms/',
        blank=True,
        null=True
    )

    # Kept for compatibility with existing project code.
    # Date-based availability should use is_available_for_dates().
    is_available = models.BooleanField(default=True)

    def is_available_for_dates(self, check_in, check_out):
        if check_in >= check_out:
            return False

        overlapping_bookings = self.bookings.filter(
            check_in__lt=check_out,
            check_out__gt=check_in
        ).exclude(status='Cancelled')

        return not overlapping_bookings.exists()

    def __str__(self):
        return self.name


class Booking(models.Model):

    STATUS_CHOICES = [
        ('Confirmed', 'Confirmed'),
        ('Checked In', 'Checked In'),
        ('Checked Out', 'Checked Out'),
        ('Cancelled', 'Cancelled'),
    ]

    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        related_name='bookings'
    )

    guest_name = models.CharField(max_length=100)

    guest_email = models.EmailField()

    guest_phone = models.CharField(
        max_length=15,
        blank=True
    )

    check_in = models.DateField()

    check_out = models.DateField()

    guests = models.PositiveIntegerField(default=1)

    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
        editable=False
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Confirmed'
    )

    booked_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        super().clean()

        if self.check_in and self.check_out:
            if self.check_in >= self.check_out:
                raise ValidationError({
                    'check_out': 'Check-out must be after check-in.'
                })

        if self.room_id and self.check_in and self.check_out:
            overlapping_bookings = Booking.objects.filter(
                room_id=self.room_id,
                check_in__lt=self.check_out,
                check_out__gt=self.check_in
            ).exclude(
                status='Cancelled'
            )

            if self.pk:
                overlapping_bookings = overlapping_bookings.exclude(
                    pk=self.pk
                )

            if overlapping_bookings.exists():
                raise ValidationError(
                    'This room is already booked for the selected dates.'
                )

    def save(self, *args, **kwargs):
        self.full_clean()

        if self.room_id and self.check_in and self.check_out:
            number_of_days = (self.check_out - self.check_in).days
            self.total_price = self.room.price * number_of_days

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.guest_name} - {self.room.name}"
