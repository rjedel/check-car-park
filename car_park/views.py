from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.gis.geos import fromstr
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import DetailView, ListView, CreateView

from .forms import CustomUserCreationForm, AddCarParkForm
from .models import CarPark, Tariff


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

    def post(self, request):
        form = AddCarParkForm(data=request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            longitude = form.cleaned_data['longitude']
            latitude = form.cleaned_data['latitude']
            # longitude = "20.892127886317226"
            # latitude = "52.232701199999994"

            free_of_charge = form.cleaned_data['free_of_charge']
            tariffs_name = form.cleaned_data['tariffs_name']
            first_hour_fee = form.cleaned_data['first_hour_fee']
            maximum_additional_fee = form.cleaned_data['maximum_additional_fee']
            additional_fee_description = form.cleaned_data['additional_fee_description']

            tariff = None
            if not free_of_charge:
                tariff = Tariff.objects.create(
                    tariffs_name=tariffs_name,
                    first_hour_fee=first_hour_fee,
                    maximum_additional_fee=maximum_additional_fee,
                    additional_fee_description=additional_fee_description,
                )
            car_park = CarPark.objects.create(
                name=name,
                description=description,
                location=fromstr('POINT({} {})'.format(longitude, latitude), srid=4326),
                free_of_charge=free_of_charge,
                tariff=tariff,
            )
            return redirect(reverse('car_park_detail', args=[car_park.pk]))
        return render(request, 'car_park/add_car_park.html', {'form': AddCarParkForm(
            data=request.POST,
            initial={
                'spot_name': '',
                'street': '',
                'street_number': None,
            }
        )})


class AboutView(View):
    def get(self, request):
        return render(request, 'car_park/about.html')


class ContactView(View):
    def get(self, request):
        return render(request, 'car_park/contact.html')
