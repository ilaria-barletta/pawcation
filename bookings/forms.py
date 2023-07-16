import datetime
from .models import Review, Booking, Pet
from django import forms 
from django.db.models import Q


MAX_BOOKINGS_PER_DAY = 2
MAX_STAY_DURATION_DAYS = 30


class ReviewForm(forms.ModelForm):

    # Taken from here: https://stackoverflow.com/questions/45847561/how-do-i-filter-values-in-django-createview-updateview
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        if user:
            # Only show bookings that have ended so we can't review future bookings 
            self.fields['booking'].queryset = Booking.objects.filter(Q(owner=user) & Q(end_date__lte=datetime.datetime.now()))

    def clean(self):
        cleaned_data = super().clean()
        booking = cleaned_data.get('booking')

        reviews_for_booking = Review.objects.filter(booking=booking)
        if reviews_for_booking.count() > 0:
            raise forms.ValidationError("You have already reviewed this booking and cannot review it again. If you would like, you can edit your existing review.")

    class Meta:
        model = Review
        fields = ('score', 'booking',)

class PetForm(forms.ModelForm):

    class Meta:
        model = Pet
        fields = ('name', 'age', 'breed','allergies','notes','picture',)


class PreVisitBookingForm(forms.ModelForm):

    is_updating = False

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        self.is_updating = kwargs.pop('is_updating')
        super().__init__(*args, **kwargs)
        if user:
            self.fields['pet'].queryset = Pet.objects.filter(owner=user)

    # From here: https://docs.djangoproject.com/en/4.2/ref/forms/validation/#cleaning-and-validating-fields-that-depend-on-each-other
    def clean(self):
        cleaned_data = super().clean()
        pet = cleaned_data.get("pet")

        bookings_for_pet = list(Booking.objects.filter(pet=pet))
        pre_visits_for_pet = list(filter(lambda booking: booking.booking_type == 0, bookings_for_pet))
        has_already_booked_pre_visit = len(pre_visits_for_pet) > 0

        if (not self.is_updating and has_already_booked_pre_visit):
            raise forms.ValidationError("You have already booked a pre-visit for this pet, and cannot book another. If you would like to change the one you have booked, please visit the bookings page and edit your existing pre-visit. Please note that if your pet has already completed a pre-visit, you won't be able to book another one. Only one pre-visit is allowed per pet.")

    class Meta:
        model = Booking
        fields = ('start_date', 'pet',)
        # Adapted from here: https://stackoverflow.com/questions/22846048/django-form-as-p-datefield-not-showing-input-type-as-date 
        widgets = {
            'start_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    
class FullVisitBookingForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        if user:
            self.fields['pet'].queryset = Pet.objects.filter(owner=user)

    # From here: https://docs.djangoproject.com/en/4.2/ref/forms/validation/#cleaning-and-validating-fields-that-depend-on-each-other
    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")
        pet = cleaned_data.get("pet")

        # Validate start date and end date 
        if (end_date < start_date + datetime.timedelta(hours=1)):
            raise forms.ValidationError(
                        "The booking must end at least an hour after the start date"
                    )
        
        bookings_for_pet = list(Booking.objects.filter(pet=pet))
        pre_visits_completed_for_pet = list(filter(lambda booking: booking.has_ended() and booking.booking_type == 0, bookings_for_pet))
        has_completed_pre_visit = len(pre_visits_completed_for_pet) > 0

        if not has_completed_pre_visit:
            raise forms.ValidationError("This pet has not had a successful pre-visit yet so you cannot make a full booking. Please book and complete a pre-visit first.")
        
        
        # Check that the booking isn't too long
        dates = [start_date+datetime.timedelta(days=x) for x in range((end_date-start_date).days)]
        dates.append(end_date)
        max_days = MAX_STAY_DURATION_DAYS
        if (len(dates) > max_days):
            raise forms.ValidationError(f"You have chosen to book for too many days. Please choose at most {max_days} days")

        # Check that we have capacity for those dates.
        for date in dates:
            # Get all the bookings that start or end on this date
            all_bookings = list(Booking.objects.all())
            start_date_date = start_date.date()
            end_date_date = end_date.date()
            bookings_on_date = list(filter(lambda booking: booking.start_date.date() == start_date_date or booking.end_date.date() == end_date_date, all_bookings))
            # If we have too many then error 
            if len(bookings_on_date) >= MAX_BOOKINGS_PER_DAY:
                raise forms.ValidationError(
                        "We don't have enough space for those dates. Please choose different dates"
                    )

    class Meta:
        model = Booking
        fields = ('start_date', 'end_date', 'pet',)
        # Adapted from here: https://stackoverflow.com/questions/22846048/django-form-as-p-datefield-not-showing-input-type-as-date 
        widgets = {
            'start_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_date': forms.DateTimeInput(attrs={'type': 'datetime-local'})
        }