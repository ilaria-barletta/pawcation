from . import views
from django.urls import path

urlpatterns = [
    path("", views.Home.as_view(), name="home"),
    path("pets", views.PetList.as_view(), name="pets"),
    path("bookings", views.BookingList.as_view(), name="bookings"),
    path("reviews", views.ReviewList.as_view(), name="reviews"),
    path("new-review", views.NewReview.as_view(), name="new_review"),
    # Found here: https://www.pythontutorial.net/django-tutorial/django-updateview/ 
    path("reviews/update/<pk>/", views.UpdateReview.as_view(), name="update_review"),
    path("reviews/delete/<pk>/", views.DeleteReview.as_view(), name="delete_review"),
    path("new-pet", views.NewPet.as_view(), name="new_pet"),
    path("pets/update/<pk>/", views.UpdatePet.as_view(), name="update_pet"),
    path("pets/delete/<pk>/", views.DeletePet.as_view(), name="delete_pet"),
]
