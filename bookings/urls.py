from . import views
from django.urls import path

urlpatterns = [
    path("", views.Home.as_view(), name="home"),
    path("pets", views.PetList.as_view(), name="pets"),
    path("bookings", views.BookingList.as_view(), name="bookings"),
]
