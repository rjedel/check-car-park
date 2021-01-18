"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from car_park.views import SignupView, AllCarParksListView, CarParkDetailView, AddCarParkView, \
    AboutView, ContactView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/', SignupView.as_view(), name="signup"),
    path("", AllCarParksListView.as_view(), name='all_car_parks_map'),
    path("car_park_detail/<int:pk>/", CarParkDetailView.as_view(), name='car_park_detail'),
    path('add_car_park/', AddCarParkView.as_view(), name='add_car_park'),
    path('about/', AboutView.as_view(), name='about'),
    path('contact/', ContactView.as_view(), name='contact'),
]
