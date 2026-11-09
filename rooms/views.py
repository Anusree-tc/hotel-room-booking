from .forms import BookingForm
from django.core.exceptions import ValidationError



from datetime import date
from urllib.parse import urlencode

from django.shortcuts import render, get_object_or_404, redirect
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.urls import reverse

from .models import Room, Booking


def room_list(request):
    checkin_text = request.GET.get('checkin', '')
    checkout_text = request.GET.get('checkout', '')
    guests_text = request.GET.get('guests', '1')

    error = ''

    try:
        guests = max(1, int(guests_text))
    except (ValueError, TypeError):
        guests = 1

    rooms = Room.objects.filter(capacity__gte=guests)

    if checkin_text and checkout_text:
        try:
            checkin = date.fromisoformat(checkin_text)
            checkout = date.fromisoformat(checkout_text)

            if checkin < timezone.localdate():
                error = 'Check-in date cannot be in the past.'

            elif checkout <= checkin:
                error = 'Check-out must be after check-in.'

            else:
                rooms = [
                    room for room in rooms
                    if room.is_available_for_dates(
                        checkin,
                        checkout
                    )
                ]

        except ValueError:
            error = 'Please select valid dates.'

    elif checkin_text or checkout_text:
        error = 'Please select both check-in and check-out dates.'

    context = {
        'rooms': rooms,
        'checkin': checkin_text,
        'checkout': checkout_text,
        'guests': guests,
        'error': error,
    }

    return render(request, 'rooms/room_list.html', context)


def book_room(request, room_id):
    
    room = get_object_or_404(Room, id=room_id)

    form = BookingForm(
        request.POST or None,
        room=room
    )

    if request.method == 'POST' and form.is_valid():

        data = form.cleaned_data

        booking = Booking(
            room=room,
            guest_name=data['guest_name'],
            guest_email=data['guest_email'],
            guest_phone=data['guest_phone'],
            check_in=data['check_in'],
            check_out=data['check_out'],
            guests=data['guests'],
            status='Confirmed'
        )

        try:
            booking.save()

            nights = (
                booking.check_out - booking.check_in
            ).days

            return render(
                request,
                'rooms/booking_details.html',
                {
                    'booking': booking,
                    'room': room,
                    'nights': nights,
                    'total_price': booking.total_price,
                }
            )

        except ValidationError as e:
            form.add_error(None, ' '.join(e.messages))

    return render(
        request,
        'rooms/book_room.html',
        {
            'room': room,
            'form': form,
        }
    )


def my_bookings(request):
    bookings = Booking.objects.none()

    email = request.POST.get(
        'email',
        request.GET.get('email', '')
    ).strip()

    if email:
        bookings = Booking.objects.filter(
            guest_email__iexact=email
        ).select_related(
            'room'
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

        booking = get_object_or_404(
            Booking,
            id=booking_id
        )

        email = request.POST.get('email', '').strip()
        today = timezone.localdate()

        if email.lower() != booking.guest_email.lower():
            return redirect('my_bookings')

        if booking.status != 'Confirmed':
            return redirect('my_bookings')

        if booking.check_in <= today:
            return redirect('my_bookings')

        booking.status = 'Cancelled'
        booking.save(update_fields=['status'])

        return redirect(f"{reverse('my_bookings')}?{urlencode({'email': email})}")

    return redirect('my_bookings')


def guest_profile(request):
    bookings = Booking.objects.none()

    email = request.POST.get(
        'email',
        request.GET.get('email', '')
    ).strip()

    if email:
        bookings = Booking.objects.filter(
            guest_email__iexact=email
        ).select_related(
            'room'
        ).order_by('-booked_at')

    latest_booking = bookings.first()

    context = {
        'bookings': bookings,
        'email': email,
        'guest_name': (
            latest_booking.guest_name
            if latest_booking else ''
        ),
        'guest_phone': (
            latest_booking.guest_phone
            if latest_booking else ''
        ),
    }

    return render(
        request,
        'rooms/guest_profile.html',
        context
    )


