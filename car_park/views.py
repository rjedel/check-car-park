from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import fromstr
from django.db import IntegrityError
from django.db.models import Max, Q, Sum
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import View
from django.views.generic import DetailView, ListView, CreateView

from .forms import CustomUserCreationForm, AddCarParkForm, EditProfileForm, CustomPasswordChangeForm, SearchForm, \
    OpinionForm
from .models import CarPark, Tariff, Opinion


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

    def get_car_park(self):
        car_park_id = self.kwargs['pk']
        car_park = get_object_or_404(CarPark, pk=car_park_id)
        return car_park

    def get_context_data(self, **kwargs):
        context = super(CarParkDetailView, self).get_context_data(**kwargs)
        car_park = self.get_car_park()
        car_park_opinions = Opinion.objects.filter(car_park=car_park)
        sum_votes = car_park_opinions.aggregate(Sum('votes'))['votes__sum']
        up_votes = car_park_opinions.filter(votes=1).count()
        down_votes = car_park_opinions.filter(votes=-1).count()
        logged_user_opinion = None
        if self.request.user.is_authenticated \
                and Opinion.objects.filter(user=self.request.user, car_park=car_park).exists():
            logged_user_opinion = Opinion.objects.get(user=self.request.user, car_park=car_park)
        context['up_votes'] = up_votes
        context['down_votes'] = down_votes
        context['sum_votes'] = sum_votes
        context['logged_user_opinion'] = logged_user_opinion
        return context


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
        return render(request, 'car_park/add_car_park.html', {'form': AddCarParkForm(data=request.POST)})


class AboutView(View):
    def get(self, request):
        return render(request, 'car_park/about.html')


class ContactView(View):
    def get(self, request):
        return render(request, 'car_park/contact.html')


class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        return render(request, 'car_park/profile.html', {'user': user})


class EditProfileView(LoginRequiredMixin, View):
    def get(self, request):
        form = EditProfileForm(instance=request.user)
        return render(request, 'car_park/edit_profile.html', {'form': form})

    def post(self, request):
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect(reverse('view_profile'))
        return render(request, 'car_park/edit_profile.html', {'form': form})


class ChangePasswordView(LoginRequiredMixin, View):
    def get(self, request):
        form = CustomPasswordChangeForm(user=request.user)
        return render(request, 'car_park/change_password.html', {'form': form})

    def post(self, request):
        form = CustomPasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect(reverse('view_profile') + '#password_changed')
        return render(request, 'car_park/change_password.html', {'form': form})


class SearchView(View):
    def get(self, request):
        form = SearchForm()

        name = request.GET.get('name')
        longitude = request.GET.get('longitude')
        latitude = request.GET.get('latitude')
        free_of_charge = request.GET.get('free_of_charge') == 'on'
        tariffs_name = request.GET.get('tariffs_name')
        first_hour_fee_from = float(request.GET.get('first_hour_fee_from', '0'))
        first_hour_fee_to = float(request.GET.get('first_hour_fee_to', '0'))
        maximum_additional_fee = float(request.GET.get('maximum_additional_fee', '0'))

        has_distance = False

        to_filter = CarPark.objects.order_by('free_of_charge', '-tariff__first_hour_fee')
        if len(request.GET) > 0:
            if name:
                to_filter = to_filter.filter(name__icontains=name)
            if free_of_charge:
                to_filter = to_filter.filter(free_of_charge=True)
            if not free_of_charge:
                if tariffs_name:
                    to_filter = to_filter.filter(tariff__tariffs_name__icontains=tariffs_name)
                if maximum_additional_fee >= 0:
                    to_filter = to_filter.filter(
                        Q(tariff__maximum_additional_fee__lte=maximum_additional_fee) | Q(free_of_charge=True)
                    )
                if first_hour_fee_from > 0:
                    to_filter = to_filter.filter(tariff__first_hour_fee__gte=first_hour_fee_from)
                if first_hour_fee_from == 0:
                    to_filter = to_filter.filter(
                        Q(tariff__first_hour_fee__gte=0) | Q(free_of_charge=True)
                    )
                if first_hour_fee_to > 0:
                    to_filter = to_filter.filter(
                        Q(tariff__first_hour_fee__lte=first_hour_fee_to) | Q(free_of_charge=True)
                    )
                if first_hour_fee_to == 0:
                    to_filter = to_filter.filter(free_of_charge=True)
                if longitude and latitude:
                    user_location = fromstr('POINT({} {})'.format(longitude, latitude), srid=4326)
                    to_filter = to_filter.annotate(
                        distance=Distance('location', user_location)
                    ).order_by('distance')
                    for obj in to_filter:
                        if bool(obj.distance.km):
                            has_distance = True
                            break
            form = SearchForm(data=request.GET)

        db_max_first_hour_fee = str(
            float(Tariff.objects.all().aggregate(Max('first_hour_fee'))['first_hour_fee__max'])
        )
        db_max_maximum_additional_fee = str(
            float(Tariff.objects.all().aggregate(Max('maximum_additional_fee'))['maximum_additional_fee__max'])
        )

        ctx = {
            'form': form,
            'db_max_first_hour_fee': db_max_first_hour_fee,
            'db_max_maximum_additional_fee': db_max_maximum_additional_fee,
            'has_distance': has_distance,
            'outcome': to_filter,
            'name': name or '',
            'free_of_charge': 'on' if free_of_charge else '',
            'first_hour_fee_from': first_hour_fee_from,
            'first_hour_fee_to': first_hour_fee_to,
            'maximum_additional_fee': maximum_additional_fee,
        }
        return render(request, 'car_park/search.html', ctx)


class OpinionView(LoginRequiredMixin, View):
    def get(self, request, pk):
        return render(request, 'car_park/opinion_form.html', {'form': OpinionForm()})

    def post(self, request, pk):
        form = OpinionForm(data=request.POST)
        if form.is_valid():
            opinion = form.cleaned_data['opinion']
            stars = form.cleaned_data['stars']
            user = request.user
            car_park = CarPark.objects.get(pk=pk)
            recommendation = form.cleaned_data['recommendation']
            try:
                opinion_obj = Opinion.objects.create(
                    opinion=opinion,
                    stars=stars,
                    user=user,
                    car_park=car_park,
                )
                if recommendation == '1':
                    opinion_obj.up_vote(user)
                if recommendation == '0':
                    opinion_obj.down_vote(user)
            except IntegrityError:
                ctx = {
                    'form': OpinionForm(),
                    'msg': 'Twoja opinia na temat tego parkingu została już dodana'
                }
                return render(request, 'car_park/opinion_form.html', ctx)
            else:
                return redirect(reverse('car_park_detail', args=[car_park.pk]))
        return render(request, 'car_park/opinion_form.html', {'form': form})


class UserOpinionsView(LoginRequiredMixin, View):
    def get(self, request):
        user_opinions = None
        if request.user.is_authenticated:
            user_opinions = Opinion.objects.filter(user=request.user)
        ctx = {'user_opinions': user_opinions}
        return render(request, 'car_park/user_opinion.html', ctx)


class OpinionDetailView(LoginRequiredMixin, View):
    def get(self, request, opinion_pk):
        logged_user_opinion = get_object_or_404(Opinion, user=request.user, pk=opinion_pk)
        ctx = {'logged_user_opinion': logged_user_opinion}
        return render(request, 'car_park/opinion_detail.html', ctx)
