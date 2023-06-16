from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from cloudinary.models import CloudinaryField

BOOKING_TYPE = ((0, "Pre Visit"), (1, "Stay"))


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
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="bookings")
    booking_type = models.IntegerField(choices=BOOKING_TYPE, default=0)


class Review(models.Model):
    score = models.IntegerField(validators=[
        MaxValueValidator(5),
        MinValueValidator(1)
    ])
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="reviews")
    booking = models.ForeignKey(
        Booking, related_name="booking", on_delete=models.CASCADE, null=True)
