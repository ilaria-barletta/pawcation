from . import views
from django.urls import path

urlpatterns = [
    path("", views.Home.as_view(), name="home"),
    path("pets", views.PetList.as_view(), name="pets"),
    path("bookings", views.BookingList.as_view(), name="bookings"),
    path("reviews", views.ReviewList.as_view(), name="reviews"),
    path("new-review", views.NewReview.as_view(), name="new_review"),
]
