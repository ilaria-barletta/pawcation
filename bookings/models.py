from datetime import date, timedelta
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from cloudinary.models import CloudinaryField
from django.forms import ValidationError

BOOKING_TYPE = ((0, "Pre Visit"), (1, "Stay"))


def validate_date_is_present_or_future(datetime):
    if datetime.date() < date.today():
        raise ValidationError("Date cannot be in the past")


def validate_date_is_future(datetime):
    if datetime.date() < date.today() + timedelta(days=1):
        raise ValidationError("Date must be in the future")


class Pet(models.Model):
    name = models.CharField(max_length=80)
    age = models.IntegerField(
        validators=[MaxValueValidator(12), MinValueValidator(1)]
    )  # age between 1 and 12
    breed = models.CharField(max_length=80)
    allergies = models.CharField(max_length=200)
    notes = models.CharField(max_length=200)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="pets"
    )  # noqa
    picture = CloudinaryField("image", default="placeholder")

    class Meta:
        ordering = ["-name"]

    def __str__(self):
        return self.name


class Booking(models.Model):
    start_date = models.DateTimeField(validators=[validate_date_is_future])
    end_date = models.DateTimeField(
        validators=[validate_date_is_present_or_future]
    )  # noqa
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="bookings"
    )  # noqa
    booking_type = models.IntegerField(choices=BOOKING_TYPE, default=0)
    pet = models.ForeignKey(
        Pet, on_delete=models.CASCADE, related_name="bookings", null=True
    )

    class Meta:
        ordering = ["-start_date"]

    # A booking has ended if the end date is in the past
    def has_ended(self):
        return self.end_date.date() < date.today()

    def __str__(self):
        # This will tell users if it's the first stay or a full booking
        booking_type_name = BOOKING_TYPE[0][1]
        if self.booking_type == BOOKING_TYPE[1][0]:
            booking_type_name = BOOKING_TYPE[1][1]
        return f"""{booking_type_name} for {self.pet.name}
        from {self.start_date.strftime("%x %X")} to
        {self.end_date.strftime("%x %X")}"""


class Review(models.Model):
    score = models.IntegerField(
        validators=[MaxValueValidator(5), MinValueValidator(1)]
    )  # noqa
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="reviews"
    )  # noqa
    booking = models.ForeignKey(
        Booking, related_name="booking", on_delete=models.CASCADE, null=True
    )

    def __str__(self):
        if self.booking:
            return f"Review for: {self.booking} by {self.owner.username}"
        return "Review with no booking"
