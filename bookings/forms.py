import datetime
from .models import Review, Booking, Pet
from django import forms 
from django.db.models import Q


MAX_BOOKINGS_PER_DAY = 2


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

        if (end_date < start_date):
            raise forms.ValidationError(
                        "The booking end date must be after the start date"
                    )
        
        # Get list of dates inclusive of start_date -> end_date
        dates = [start_date+datetime.timedelta(days=x) for x in range((end_date-start_date).days)]
        dates.append(end_date)

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

    