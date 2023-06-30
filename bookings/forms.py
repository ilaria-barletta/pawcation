import datetime
from .models import Review, Booking, Pet
from django import forms 
from django.db.models import Q


MAX_BOOKINGS_PER_DAY = 2
MAX_STAY_DURATION_DAYS = 30
MAX_PRE_VISIT_DURATION_DAYS = 1


class ReviewForm(forms.ModelForm):

    # Taken from here: https://stackoverflow.com/questions/45847561/how-do-i-filter-values-in-django-createview-updateview
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        if user:
            self.fields['booking'].queryset = Booking.objects.filter(owner=user)

    class Meta:
        model = Review
        fields = ('score', 'booking',)

class PetForm(forms.ModelForm):

    class Meta:
        model = Pet
        fields = ('name', 'age', 'breed','allergies','notes','picture',)


class BookingForm(forms.ModelForm):

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

        if (end_date < start_date):
            raise forms.ValidationError(
                        "The booking end date must be after the start date"
                    )
        
        # Get list of dates inclusive of start_date -> end_date
        dates = [start_date+datetime.timedelta(days=x) for x in range((end_date-start_date).days)]
        dates.append(end_date)

        bookings_for_pet = Booking.objects.filter(pet=pet)
        is_pre_visit = len(bookings_for_pet) < 1

        # This will validate if this is the first visit for this pet 
        # and change the maximum number of days
        max_days = MAX_PRE_VISIT_DURATION_DAYS if is_pre_visit else MAX_STAY_DURATION_DAYS
        pre_visit_validation_days_message = "As this pet has not had a stay before we need to have a pre-visit. Please choose at most one day for your booking"
        full_stay_validation_message = f"You have chosen to book for too many days. Please choose at most {max_days} days"
        max_days_message = pre_visit_validation_days_message if is_pre_visit else full_stay_validation_message

        if (len(dates) > max_days):
            raise forms.ValidationError(max_days_message)

        for date in dates:
            # Get all the bookings that start or end on this date
            bookings_on_date = Booking.objects.filter(Q(start_date=date) | Q(end_date=date))
            # If we have too many then error 
            if bookings_on_date.count() >= MAX_BOOKINGS_PER_DAY:
                raise forms.ValidationError(
                        "We don't have enough space for those dates. Please choose different dates"
                    )

    class Meta:
        model = Booking
        fields = ('start_date', 'end_date', 'pet',)
        # Adapted from here: https://stackoverflow.com/questions/22846048/django-form-as-p-datefield-not-showing-input-type-as-date 
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'})
        }

    