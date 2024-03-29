from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.http import Http404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.db.models import Q
from .models import Pet, Booking, Review
from .forms import (
    ReviewForm,
    PetForm,
    PreVisitBookingForm,
    FullVisitBookingForm,
)
from datetime import timedelta


# When users come to the site we want to show the home page
# We are using TemplateView so we can just render
# a template without any model
class Home(TemplateView):
    template_name = "home.html"


class PetList(LoginRequiredMixin, ListView):
    model = Pet
    template_name = "pets.html"
    # Send users to home page if they try and access a logged in page
    login_url = "/"

    # Only show Pets for the current user
    # and not every pet in the database
    def get_queryset(self):
        return Pet.objects.filter(owner=self.request.user)


class BookingList(LoginRequiredMixin, ListView):
    model = Booking
    template_name = "bookings.html"
    # Send users to home page if they try and access a logged in page
    login_url = "/"

    def get_queryset(self):
        return Booking.objects.filter(owner=self.request.user).order_by(
            "-start_date"
        )  # Only show Bookings for the current user


class ReviewList(LoginRequiredMixin, ListView):
    model = Review
    template_name = "reviews.html"
    # Send users to home page if they try and access a logged in page
    login_url = "/"

    # Only show Reviews for the current user
    # and not every review in the database
    def get_queryset(self):
        return Review.objects.filter(owner=self.request.user)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data["max_review_score"] = 5
        data["empty_message"] = "You don't have any reviews yet"
        data["can_modify_reviews"] = True
        data["can_create_reviews"] = True
        data["page_title"] = "My Reviews"

        return data


class OtherUsersReviewList(ListView):
    model = Review
    template_name = "reviews.html"

    # If the user is logged in we can see other user reviews
    # If the user is not logged in they can see all reviews
    def get_queryset(self):
        if not self.request.user.is_anonymous:
            return Review.objects.filter(~Q(owner=self.request.user))
        return Review.objects.all()

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data["max_review_score"] = 5
        data["empty_message"] = "There are no reviews yet."
        data["can_modify_reviews"] = False
        # Only let logged in users leave reviews
        data["can_create_reviews"] = False
        data["page_title"] = (
            "All Reviews"
            if self.request.user.is_anonymous
            else "Other Users Reviews"  # Change title depending on auth
        )

        return data


class NewReview(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Review
    template_name = "create_edit_review.html"
    form_class = ReviewForm
    success_url = "/reviews"
    success_message = "Your review has been added successfully."
    # Send users to home page if they try and access a logged in page
    login_url = "/"

    # Taken from here: https://tinyurl.com/3bbxhb9n
    # This allows us to filter the list of bookings for the review to show
    # the current users bookings
    def get_form_kwargs(self):
        kwargs = super(NewReview, self).get_form_kwargs()
        kwargs["user"] = self.request.user
        kwargs["is_updating"] = False
        return kwargs

    # Taken from here: https://tinyurl.com/5xehfcxw
    # This sets the owner on the review model to the current user
    def form_valid(self, form):
        user = self.request.user
        form.instance.owner = user
        return super(NewReview, self).form_valid(form)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data["page_title"] = "New Review"

        return data


class UpdateReview(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Review
    template_name = "create_edit_review.html"
    form_class = ReviewForm
    success_url = "/reviews"
    success_message = "Your review has been updated successfully"
    # Send users to home page if they try and access a logged in page
    login_url = "/"

    # Taken from here: https://tinyurl.com/3bbxhb9n
    def get_form_kwargs(self):
        kwargs = super(UpdateReview, self).get_form_kwargs()
        kwargs["user"] = self.request.user
        kwargs["is_updating"] = True
        return kwargs

    # Taken from here: https://tinyurl.com/3fh5xcx3
    def get_object(self, *args, **kwargs):
        obj = super(UpdateReview, self).get_object(*args, **kwargs)
        if not obj.owner == self.request.user:
            raise Http404
        return obj

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data["page_title"] = "Update Review"

        return data


class DeleteReview(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Review
    template_name = "delete_review.html"
    success_url = "/reviews"
    context_object_name = "review"
    success_message = "Your review has been deleted successfully"
    # Send users to home page if they try and access a logged in page
    login_url = "/"

    def get_object(self, *args, **kwargs):
        obj = super(DeleteReview, self).get_object(*args, **kwargs)
        if not obj.owner == self.request.user:
            raise Http404
        return obj

    # Taken from here: https://tinyurl.com/5xyfmxm4
    # DeleteView doesn't work the same way as
    # Create and Update and we need to add this code
    # so the success message works
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(DeleteReview, self).delete(request, *args, **kwargs)


class NewPet(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Pet
    template_name = "create_edit_pet.html"
    form_class = PetForm
    success_url = "/pets"
    success_message = "Your pet %(name)s has been added successfully."
    # Send users to home page if they try and access a logged in page
    login_url = "/"

    def form_valid(self, form):
        user = self.request.user
        form.instance.owner = user
        return super(NewPet, self).form_valid(form)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data["page_title"] = "Register Your Pet"

        return data


class UpdatePet(LoginRequiredMixin, SuccessMessageMixin, UpdateView):  # noqa
    model = Pet
    template_name = "create_edit_pet.html"
    form_class = PetForm
    success_url = "/pets"
    success_message = "Your pet %(name)s has been updated successfully."
    # Send users to home page if they try and access a logged in page
    login_url = "/"

    def get_object(self, *args, **kwargs):
        obj = super(UpdatePet, self).get_object(*args, **kwargs)
        if not obj.owner == self.request.user:
            raise Http404
        return obj

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data["page_title"] = "Update Your Pet"

        return data


class DeletePet(LoginRequiredMixin, SuccessMessageMixin, DeleteView):  # noqa
    model = Pet
    template_name = "delete_pet.html"
    success_url = "/pets"
    context_object_name = "pet"
    success_message = "Your pet has been deleted successfully."
    # Send users to home page if they try and access a logged in page
    login_url = "/"

    def get_object(self, *args, **kwargs):
        obj = super(DeletePet, self).get_object(*args, **kwargs)
        if not obj.owner == self.request.user:
            raise Http404
        return obj

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(DeletePet, self).delete(request, *args, **kwargs)


class DeleteBooking(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Booking
    template_name = "delete_booking.html"
    success_url = "/bookings"
    context_object_name = "booking"
    success_message = "Your booking has been deleted successfully."
    # Send users to home page if they try and access a logged in page
    login_url = "/"

    def get_object(self, *args, **kwargs):
        obj = super(DeleteBooking, self).get_object(*args, **kwargs)
        if not obj.owner == self.request.user:
            raise Http404
        return obj

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(DeleteBooking, self).delete(request, *args, **kwargs)


class StartNewBooking(LoginRequiredMixin, TemplateView):
    template_name = "start_new_booking.html"
    # Send users to home page if they try and access a logged in page
    login_url = "/"


class NewPreVisit(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Booking
    template_name = "create_edit_booking.html"
    form_class = PreVisitBookingForm
    success_url = "/bookings"
    success_message = "Your pre-visit has been added successfully."
    # Send users to home page if they try and access a logged in page
    login_url = "/"

    # This allows us to filter the list of pet for the booking to show
    # the current users pets
    def get_form_kwargs(self):
        kwargs = super(NewPreVisit, self).get_form_kwargs()
        kwargs["user"] = self.request.user
        kwargs["is_updating"] = False
        return kwargs

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        # Change the title in the same template for new booking vs edit booking
        data["page_title"] = "New Pre Visit"

        return data

    def form_valid(self, form):
        user = self.request.user
        form.instance.owner = user
        form.instance.booking_type = 0
        form.instance.end_date = form.instance.start_date + timedelta(hours=1)

        return super(NewPreVisit, self).form_valid(form)


class UpdatePreVisit(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Booking
    template_name = "create_edit_booking.html"
    form_class = PreVisitBookingForm
    success_url = "/bookings"
    success_message = "Your pre-visit has been updated successfully."
    # Send users to home page if they try and access a logged in page
    login_url = "/"

    def get_form_kwargs(self):
        kwargs = super(UpdatePreVisit, self).get_form_kwargs()
        kwargs["user"] = self.request.user
        kwargs["is_updating"] = True
        return kwargs

    def get_object(self, *args, **kwargs):
        obj = super(UpdatePreVisit, self).get_object(*args, **kwargs)
        if not obj.owner == self.request.user:
            raise Http404
        return obj

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data["page_title"] = "Update Pre Visit"

        return data

    def form_valid(self, form):
        form.instance.end_date = form.instance.start_date + timedelta(hours=1)
        return super(UpdatePreVisit, self).form_valid(form)


class NewFullBooking(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Booking
    template_name = "create_edit_booking.html"
    form_class = FullVisitBookingForm
    success_url = "/bookings"
    success_message = "Your full booking has been added successfully."
    # Send users to home page if they try and access a logged in page
    login_url = "/"

    # This allows us to filter the list of pet for the booking to show
    # the current users pets
    def get_form_kwargs(self):
        kwargs = super(NewFullBooking, self).get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        # Change the title in the same template for new booking vs edit booking
        data["page_title"] = "New Full Booking"

        return data

    def form_valid(self, form):
        user = self.request.user
        form.instance.owner = user
        form.instance.booking_type = 1

        return super(NewFullBooking, self).form_valid(form)


class UpdateFullBooking(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Booking
    template_name = "create_edit_booking.html"
    form_class = FullVisitBookingForm
    success_url = "/bookings"
    success_message = "Your full booking has been updated successfully."
    # Send users to home page if they try and access a logged in page
    login_url = "/"

    def get_form_kwargs(self):
        kwargs = super(UpdateFullBooking, self).get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def get_object(self, *args, **kwargs):
        obj = super(UpdateFullBooking, self).get_object(*args, **kwargs)
        if not obj.owner == self.request.user:
            raise Http404
        return obj

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data["page_title"] = "Update Full Booking"

        return data
