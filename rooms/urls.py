from django.urls import path
from . import views

urlpatterns = [
    path('', views.room_list, name='room_list'),
    path('book/<int:room_id>/', views.book_room, name='book_room'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path(
    'cancel-booking/<int:booking_id>/',
    views.cancel_booking,
    name='cancel_booking'
),
    path('profile/', views.guest_profile, name='guest_profile'),
]