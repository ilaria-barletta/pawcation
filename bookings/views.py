from django.shortcuts import render
from django.views import generic
from .models import Pet, Booking, Review
from .forms import ReviewForm


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
        return Booking.objects.filter(owner = self.request.user).order_by("-start_date")

class ReviewList(generic.ListView):
    model = Review
    template_name = "reviews.html"

    # Only show Reviews for the current user
    # and not every review in the database
    def get_queryset(self):
        return Review.objects.filter(owner=self.request.user)
    
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['max_review_score'] = 5

        return data 

class NewReview(generic.edit.CreateView):
    model = Review
    template_name = "create_edit_review.html"
    form_class = ReviewForm
    success_url = '/reviews'

    # Taken from here: https://stackoverflow.com/questions/45847561/how-do-i-filter-values-in-django-createview-updateview 
    def get_form_kwargs(self):
        kwargs = super(NewReview, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    # Taken from here: https://stackoverflow.com/questions/21652073/django-how-to-set-a-hidden-field-on-a-generic-create-view
    def form_valid(self, form):
         user = self.request.user
         form.instance.owner = user
         return super(NewReview, self).form_valid(form)

class UpdateReview(generic.edit.UpdateView):
    model = Review
    template_name = "create_edit_review.html"
    form_class = ReviewForm
    success_url = '/reviews'

    # Taken from here: https://stackoverflow.com/questions/45847561/how-do-i-filter-values-in-django-createview-updateview 
    def get_form_kwargs(self):
        kwargs = super(UpdateReview, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
