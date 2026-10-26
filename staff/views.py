

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.utils import timezone
from django.views.decorators.http import require_POST
from rooms.models import Booking
from django.db.models import Sum
from rooms.models import Room


@user_passes_test(
    lambda user: user.is_authenticated and user.is_staff,
    login_url='/staff/login/'
)
def dashboard(request):
    today = timezone.localdate()

    # Today's Check-ins
    checkin_bookings = Booking.objects.filter(
        check_in=today,
        status='Confirmed'
    ).select_related('room').order_by('check_in')

    today_checkins = checkin_bookings.count()

    # Currently Staying Guests
    staying_bookings = Booking.objects.filter(
        status='Checked In'
    ).select_related('room').order_by('check_out')

    currently_staying = staying_bookings.count()

    # Today's Check-outs
    checkout_bookings = Booking.objects.filter(
        check_out=today,
        status='Checked In'
    ).select_related('room').order_by('check_out')

    today_checkouts = checkout_bookings.count()

    # All Bookings
    bookings = Booking.objects.select_related(
        'room'
    ).order_by('-booked_at')

    total_bookings = Booking.objects.exclude(
        status='Cancelled'
    ).count()

    context = {
        'today': today,
        'today_checkins': today_checkins,
        'checkin_bookings': checkin_bookings,
        'currently_staying': currently_staying,
        'staying_bookings': staying_bookings,
        'today_checkouts': today_checkouts,
        'checkout_bookings': checkout_bookings,
        'total_bookings': total_bookings,
        'bookings': bookings,
    }

    return render(request, 'staff/dashboard.html', context)



@user_passes_test(lambda user: user.is_authenticated and user.is_staff, login_url='/staff/login/')
@require_POST
def check_in_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    today = timezone.localdate()

    if booking.status != 'Confirmed':
        messages.error(request, 'This booking cannot be checked in.')
    elif booking.check_in > today:
        messages.error(request, 'Check-in date has not arrived yet.')
    elif booking.check_out <= today:
        messages.error(request, 'This booking has already reached its checkout date.')
    else:
        booking.status = 'Checked In'
        booking.save(update_fields=['status'])
        messages.success(request, 'Guest checked in successfully.')

    return redirect('staff_dashboard')



@user_passes_test(lambda user: user.is_authenticated and user.is_staff, login_url='/staff/login/')
@require_POST
def check_out_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    today = timezone.localdate()

    if booking.status != 'Checked In':
        messages.error(
            request,
            'Only checked-in guests can check out.'
        )

    elif booking.check_out > today:
        messages.error(
            request,
            'Checkout is allowed only on or after the checkout date.'
        )

    else:
        booking.status = 'Checked Out'
        booking.save(update_fields=['status'])
        messages.success(
            request,
            'Guest checked out successfully.'
        )

    return redirect('staff_dashboard')

@user_passes_test(
    lambda user: user.is_authenticated and user.is_staff,
    login_url='/staff/login/'
)
def admin_reports(request):
    total_bookings = Booking.objects.count()

    confirmed_bookings = Booking.objects.filter(
        status='Confirmed'
    ).count()

    cancelled_bookings = Booking.objects.filter(
        status='Cancelled'
    ).count()

    revenue = Booking.objects.exclude(
        status='Cancelled'
    ).aggregate(
        total=Sum('total_price')
    )['total'] or 0

    total_rooms = Room.objects.count()

    available_rooms = Room.objects.filter(
        is_available=True
    ).count()

    bookings = Booking.objects.select_related(
        'room'
    ).order_by('-booked_at')

    context = {
        'total_bookings': total_bookings,
        'confirmed_bookings': confirmed_bookings,
        'cancelled_bookings': cancelled_bookings,
        'revenue': revenue,
        'total_rooms': total_rooms,
        'available_rooms': available_rooms,
        'bookings': bookings,
    }

    return render(
        request,
        'staff/admin_reports.html',
        context
    )