from django import forms
from django.utils import timezone


class BookingForm(forms.Form):

    guest_name = forms.CharField(
        max_length=100,
        label='Guest Name',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your name'
        })
    )

    guest_email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email'
        })
    )

    guest_phone = forms.CharField(
        max_length=15,
        required=False,
        label='Phone Number',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter phone number'
        })
    )

    check_in = forms.DateField(
        label='Check-in Date',
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control'
        })
    )

    check_out = forms.DateField(
        label='Check-out Date',
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control'
        })
    )

    guests = forms.IntegerField(
        min_value=1,
        label='Number of Guests',
        widget=forms.NumberInput(attrs={
            'class': 'form-control'
        })
    )

    def __init__(self, *args, room=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.room = room

    def clean(self):

        cleaned_data = super().clean()

        check_in = cleaned_data.get('check_in')
        check_out = cleaned_data.get('check_out')
        guests = cleaned_data.get('guests')

        if check_in and check_in < timezone.localdate():
            self.add_error(
                'check_in',
                'Check-in date cannot be in the past.'
            )

        if check_in and check_out:

            if check_out <= check_in:
                self.add_error(
                    'check_out',
                    'Check-out must be after check-in.'
                )

            elif self.room and not self.room.is_available_for_dates(
                check_in, check_out
            ):
                self.add_error(
                    None,
                    'This room is already booked for these dates.'
                )

        if guests and self.room and guests > self.room.capacity:
            self.add_error(
                'guests',
                'Guest count exceeds room capacity.'
            )

        return cleaned_data