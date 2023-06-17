from django.shortcuts import render
from django.views import generic
from .models import Pet


# When users come to the site we want to show the home page 
# We are using TemplateView so we can just render 
# a template without any model
class Home(generic.TemplateView):
    template_name = "home.html"

class PetList(generic.ListView):
    model = Pet
    template_name = "pets.html"