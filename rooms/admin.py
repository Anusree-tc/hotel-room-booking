from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Room,Booking




@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'room_type',
        'price',
        'capacity',
    )

    list_filter = ('room_type',)

    search_fields = ('name',)


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        'guest_name',
        'guest_email',
        'room',
        'check_in',
        'check_out',
        'guests',
        'status',
        'total_price',
    )

    list_filter = (
        'status',
        'check_in',
        'check_out',
    )

    search_fields = (
        'guest_name',
        'guest_email',
        'reference_code',
    )

    ordering = ('-booked_at',)