from django.contrib import admin
from .models import Pet, Booking, Review

admin.site.register([Pet, Booking, Review])
