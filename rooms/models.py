from django.db import models

# Create your models here.
from django.db import models


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

    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    
    
class Booking(models.Model):
    
    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        related_name='bookings'
    )

    guest_name = models.CharField(max_length=100)

    guest_email = models.EmailField()
    guest_phone = models.CharField(max_length=15, blank=True)

    check_in = models.DateField()

    check_out = models.DateField()

    guests = models.PositiveIntegerField(default=1)

    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    STATUS_CHOICES = [
        ('Confirmed', 'Confirmed'),
        ('checked in', 'checked in'),
        ('checked out', 'checked out'),
        ('Cancelled', 'Cancelled'),
       
    ]

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Confirmed'
    )

    booked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.guest_name} - {self.room.name}"