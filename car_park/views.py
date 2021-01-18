from django.shortcuts import render
from django.views import View
from django.views.generic import DetailView, ListView, CreateView

from .forms import CustomUserCreationForm, AddCarParkForm
from .models import CarPark


class ShowMapView(View):
    def get(self, request):
        return render(request, 'car_park/add_car_park.html', {'form': AddCarParkForm()})


class AllCarParksListView(ListView):
    model = CarPark


class CarParkDetailView(DetailView):
    model = CarPark


class AddCarParkView(View):
    def get(self, request):
        return render(request, 'car_park/add_car_park.html', {'form': AddCarParkForm()})


class AboutView(View):
    def get(self, request):
        return render(request, 'car_park/about.html')


class ContactView(View):
    def get(self, request):
        return render(request, 'car_park/contact.html')


class SignupView(CreateView):
    form_class = CustomUserCreationForm
    success_url = '/'
    template_name = 'car_park/signup.html'
