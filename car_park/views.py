from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render
from django.views import View
from django.views.generic import DetailView, ListView, CreateView

from .forms import CustomUserCreationForm, AddCarParkForm
from .models import CarPark


class SignupView(CreateView):
    form_class = CustomUserCreationForm
    success_url = '/login/'
    template_name = 'car_park/signup.html'


class CustomLoginView(LoginView):
    redirect_authenticated_user = True
    template_name = 'car_park/login.html'


class CustomLogoutView(LogoutView):
    template_name = 'car_park/logged_out.html'


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
