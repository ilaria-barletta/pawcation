from django.shortcuts import render
from django.views import generic
from .models import Pet, Booking


# When users come to the site we want to show the home page 
# We are using TemplateView so we can just render 
# a template without any model
class Home(generic.TemplateView):
    template_name = "home.html"

class PetList(generic.ListView):
    model = Pet
    template_name = "pets.html"

    # Only show Pets for the current user 
    # and not every pet in the database
    def get_queryset(self):
        return Pet.objects.filter(owner=self.request.user)

class BookingList(generic.ListView):
    model = Booking
    template_name = "bookings.html"

    # Only show Bookings for the current user 
    # and not every booking in the database
    def get_queryset(self):
        return Booking.objects.filter(owner = self.request.user)
