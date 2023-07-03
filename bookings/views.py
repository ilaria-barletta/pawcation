from django.http import Http404
from django.views import generic
from django.db.models import Q
from .models import Pet, Booking, Review
from .forms import ReviewForm, PetForm, BookingForm


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
        data['empty_message'] = "You don't have any reviews yet"
        data['can_modify_reviews'] = True

        return data 

class OtherUsersReviewList(generic.ListView):
    model = Review
    template_name = "reviews.html"

    # Only show Reviews for the other users
    # and not the current user
    def get_queryset(self):
        return Review.objects.filter(~Q(owner=self.request.user))
    
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['max_review_score'] = 5
        data['empty_message'] = "There are no reviews yet."
        data['can_modify_reviews'] = False

        return data 

class NewReview(generic.edit.CreateView):
    model = Review
    template_name = "create_edit_review.html"
    form_class = ReviewForm
    success_url = '/reviews'

    # Taken from here: https://stackoverflow.com/questions/45847561/how-do-i-filter-values-in-django-createview-updateview 
    # This allows us to filter the list of bookings for the review to show 
    # the current users bookings 
    def get_form_kwargs(self):
        kwargs = super(NewReview, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    # Taken from here: https://stackoverflow.com/questions/21652073/django-how-to-set-a-hidden-field-on-a-generic-create-view
    # This sets the owner on the review model to the current user
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
    
    # Taken from here: https://stackoverflow.com/questions/25324948/django-generic-updateview-how-to-check-credential 
    def get_object(self, *args, **kwargs):
        obj = super(UpdateReview, self).get_object(*args, **kwargs)
        if not obj.owner == self.request.user:
            raise Http404
        return obj

class DeleteReview(generic.edit.DeleteView):
    model = Review
    template_name = "delete_review.html"
    success_url = '/reviews'
    context_object_name = 'review'

    def get_object(self, *args, **kwargs):
        obj = super(DeleteReview, self).get_object(*args, **kwargs)
        if not obj.owner == self.request.user:
            raise Http404
        return obj


class NewPet(generic.edit.CreateView):
    model = Pet
    template_name = "create_edit_pet.html"
    form_class = PetForm
    success_url = '/pets'

    def form_valid(self, form):
        user = self.request.user
        form.instance.owner = user
        return super(NewPet, self).form_valid(form)


class UpdatePet(generic.edit.UpdateView):
    model = Pet
    template_name = "create_edit_pet.html"
    form_class = PetForm
    success_url = '/pets'

    def get_object(self, *args, **kwargs):
        obj = super(UpdatePet, self).get_object(*args, **kwargs)
        if not obj.owner == self.request.user:
            raise Http404
        return obj


class DeletePet(generic.edit.DeleteView):
    model = Pet
    template_name = "delete_pet.html"
    success_url = '/pets'
    context_object_name = 'pet'

    def get_object(self, *args, **kwargs):
        obj = super(DeletePet, self).get_object(*args, **kwargs)
        if not obj.owner == self.request.user:
            raise Http404
        return obj


class NewBooking(generic.edit.CreateView):
    model = Booking
    template_name = "create_edit_booking.html"
    form_class = BookingForm
    success_url = '/bookings'

    # This allows us to filter the list of pet for the booking to show
    # the current users pets
    def get_form_kwargs(self):
        kwargs = super(NewBooking, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        user = self.request.user
        form.instance.owner = user

        # Check if this pet has stayed before and make a pre-visit 
        # if they haven't and a full booking if they have 
        pet = form.instance.pet
        bookings_for_pet = Booking.objects.filter(pet=pet)
        booking_type = 0
        if len(bookings_for_pet) > 0:
            booking_type = 1

        form.instance.booking_type = booking_type

        return super(NewBooking, self).form_valid(form)


class UpdateBooking(generic.edit.UpdateView):
    model = Booking
    template_name = "create_edit_booking.html"
    form_class = BookingForm
    success_url = '/bookings'

    def get_form_kwargs(self):
        kwargs = super(UpdateBooking, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def get_object(self, *args, **kwargs):
        obj = super(UpdateBooking, self).get_object(*args, **kwargs)
        if not obj.owner == self.request.user:
            raise Http404
        return obj


class DeleteBooking(generic.edit.DeleteView):
    model = Booking
    template_name = "delete_booking.html"
    success_url = '/bookings'
    context_object_name = 'booking'

    def get_object(self, *args, **kwargs):
        obj = super(DeleteBooking, self).get_object(*args, **kwargs)
        if not obj.owner == self.request.user:
            raise Http404
        return obj
