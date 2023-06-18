from .models import Review, Booking
from django import forms 

class ReviewForm(forms.ModelForm):

    # Taken from here: https://stackoverflow.com/questions/60104231/django-3-making-models-fk-dropdown-display-current-users-data-only 
    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            self.fields['booking'].queryset = Booking.objects.filter(owner=user)

    class Meta:
        model = Review
        fields = ('score', 'booking',)