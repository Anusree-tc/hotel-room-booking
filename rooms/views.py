from django.shortcuts import render
from datetime import date
from decimal import Decimal
from django.db.models import Q
# Create your views here.
from django.shortcuts import render,get_object_or_404, redirect
from .models import Room,Booking


def room_list(request):
    rooms = Room.objects.filter(is_available=True)
    checkin = request.GET.get('checkin', '')
    checkout = request.GET.get('checkout', '')
    guests = request.GET.get('guests', '1')

    try:
        guests = int(guests)
        if guests < 1:
            guests = 1
    except (ValueError, TypeError):
        guests = 1

    rooms = rooms.filter(capacity__gte=guests)

    context = {
        'rooms': rooms,
        'checkin': checkin,
        'checkout': checkout,
        'guests': guests,
    }
    return render(request, 'rooms/room_list.html', {'rooms': rooms})


def book_room(request, room_id):
    room = get_object_or_404(Room, id=room_id, is_available=True)

    error = ''

    if request.method == 'POST':
        guest_name = request.POST.get('guest_name', '').strip()
        guest_email = request.POST.get('guest_email', '').strip()
        guest_phone = request.POST.get('guest_phone', '').strip()
        check_in_text = request.POST.get('check_in', '')
        check_out_text = request.POST.get('check_out', '')
        guests_text = request.POST.get('guests', '1')

        try:
            check_in = date.fromisoformat(check_in_text)
            check_out = date.fromisoformat(check_out_text)
            guests = int(guests_text)

            if not guest_name or not guest_email:
                error = 'Please enter your name and email.'

            elif check_in < date.today():
                error = 'Check-in date cannot be in the past.'

            elif check_out <= check_in:
                error = 'Check-out must be after check-in.'

            elif guests < 1 or guests > room.capacity:
                error = 'Invalid number of guests.'

            else:
                nights = (check_out - check_in).days
                total_price = room.price * Decimal(nights)
                
                booking = Booking.objects.create(
                    room=room,
                    guest_name=guest_name,
                    guest_email=guest_email,
                    guest_phone=guest_phone,
                    check_in=check_in,
                    check_out=check_out,
                    guests=guests,
                    total_price=total_price,
                    status='Confirmed',
                    )

                return render(
                    request,
                    'rooms/booking_details.html',
                    {
                        'booking':booking,
                        'room': room,
                        'guest_name': guest_name,
                        'guest_email': guest_email,
                        'check_in': check_in,
                        'check_out': check_out,
                        'guests': guests,
                        'nights': nights,
                        'total_price': total_price,
                    }
                )

        except (ValueError, TypeError):
            error = 'Please enter valid booking details.'

    return render(
        request,
        'rooms/book_room.html',
        {
            'room': room,
            'error': error,
        }
    )
    

def my_bookings(request):
    bookings = Booking.objects.none()
    email = ''

    if request.method == 'POST':
        email = request.POST.get('email', '').strip()

    if email:
        bookings = Booking.objects.filter(
            guest_email__iexact=email
        ).order_by('-booked_at')

    return render(
        request,
        'rooms/my_bookings.html',
        {
            'bookings': bookings,
            'email': email,
        }
    )

def cancel_booking(request, booking_id):
    if request.method == 'POST':
        booking = get_object_or_404(Booking, id=booking_id)

        email = request.POST.get('email', '').strip()

        if email and booking.guest_email.lower() == email.lower():
            if booking.status == 'Confirmed':
                booking.status = 'Cancelled'
                booking.save()

        return redirect('/rooms/my-bookings/')

    return redirect('my_bookings')


def guest_profile(request):
    bookings = Booking.objects.none()
    email = ''

    if request.method == 'POST':
        email = request.POST.get('email', '').strip()

    if email:
        bookings = Booking.objects.filter(
            guest_email__iexact=email
        ).select_related('room').order_by('-booked_at')

    latest_booking = bookings.first()

    context = {
        'bookings': bookings,
        'email': email,
        'guest_name': latest_booking.guest_name if latest_booking else '',
        'guest_phone': latest_booking.guest_phone if latest_booking else '',
    }

    return render(request, 'rooms/guest_profile.html', context)

