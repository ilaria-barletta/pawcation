from datetime import date
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from cloudinary.models import CloudinaryField
from django.forms import ValidationError

BOOKING_TYPE = ((0, "Pre Visit"), (1, "Stay"))


def validate_date_is_present_or_future(datetime):
    if datetime.date() < date.today():
        raise ValidationError("Date cannot be in the past")


class Pet(models.Model):
    name = models.CharField(max_length=80)
    age = models.IntegerField(validators=[
        MaxValueValidator(12),
        MinValueValidator(1)
    ])
    breed = models.CharField(max_length=80)
    allergies = models.CharField(max_length=200)
    notes = models.CharField(max_length=200)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="pets")
    picture = CloudinaryField('image', default='placeholder')

    class Meta:
        ordering = ["-name"]

    def __str__(self):
        return self.name


class Booking(models.Model):
    start_date = models.DateTimeField(validators=[validate_date_is_present_or_future])
    end_date = models.DateTimeField(validators=[validate_date_is_present_or_future])
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="bookings")
    booking_type = models.IntegerField(choices=BOOKING_TYPE, default=0)
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name="bookings", null=True)

    class Meta:
        ordering = ["-start_date"]

    def __str__(self):
        # This will tell users if it's the first stay or a full booking 
        booking_type_name = BOOKING_TYPE[0][1]
        if self.booking_type == BOOKING_TYPE[1][0]:
            booking_type_name = BOOKING_TYPE[1][1]
        return f'{booking_type_name} for {self.pet.name} from {self.start_date.strftime("%x")} to {self.end_date.strftime("%x")}'


class Review(models.Model):
    score = models.IntegerField(validators=[
        MaxValueValidator(5),
        MinValueValidator(1)
    ])
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="reviews")
    booking = models.ForeignKey(
        Booking, related_name="booking", on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        if self.booking:
            return f'Review for booking on {self.booking.start_date.strftime("%x")}'
        return 'Review with no booking' 
