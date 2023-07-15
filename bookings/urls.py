from . import views
from django.urls import path

urlpatterns = [
    path("", views.Home.as_view(), name="home"),
    path("pets", views.PetList.as_view(), name="pets"),
    path("bookings", views.BookingList.as_view(), name="bookings"),
    path("reviews", views.ReviewList.as_view(), name="reviews"),
    path("other-users-reviews", views.OtherUsersReviewList.as_view(), name="other_users_reviews"),
    path("new-review", views.NewReview.as_view(), name="new_review"),
    # Found here: https://www.pythontutorial.net/django-tutorial/django-updateview/ 
    path("reviews/update/<pk>/", views.UpdateReview.as_view(), name="update_review"),
    path("reviews/delete/<pk>/", views.DeleteReview.as_view(), name="delete_review"),
    path("new-pet", views.NewPet.as_view(), name="new_pet"),
    path("pets/update/<pk>/", views.UpdatePet.as_view(), name="update_pet"),
    path("pets/delete/<pk>/", views.DeletePet.as_view(), name="delete_pet"),
    path("start-new-booking", views.StartNewBooking.as_view(), name="start_new_booking"),
    path("new-pre-visit", views.NewPreVisit.as_view(), name="new_pre_visit"),
    path("pre-visit/update/<pk>/", views.UpdatePreVisit.as_view(), name="update_pre_visit"),
    path("new-full-booking", views.NewFullBooking.as_view(), name="new_full_booking"),
    path("full-booking/update/<pk>/", views.UpdateFullBooking.as_view(), name="update_full_booking"),
    path("bookings/delete/<pk>/", views.DeleteBooking.as_view(), name="delete_booking"),
]
