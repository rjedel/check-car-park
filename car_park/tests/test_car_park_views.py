import pytest
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.test import Client
from django.urls import reverse

from car_park.models import CarPark, Tariff, Category, Opinion


@pytest.mark.django_db
def test_car_park_detail(client: Client, car_park: CarPark):
    """Checks whether detailed data about the car park is displayed."""
    car_park_obj, tariff_obj, category_obj_1, category_obj_2, category_obj_3 = car_park

    response = client.get(reverse('car_park_detail', args=[car_park_obj.pk]))

    assert response.status_code == 200

    assert response.context['object'].name == car_park_obj.name
    assert response.context['object'].description == car_park_obj.description
    assert response.context['object'].location == car_park_obj.location
    assert response.context['object'].created == car_park_obj.created
    assert response.context['object'].update == car_park_obj.update
    assert response.context['object'].free_of_charge == car_park_obj.free_of_charge

    assert response.context['object'].tariff.tariffs_name == car_park_obj.tariff.tariffs_name
    assert response.context['object'].tariff.first_hour_fee == car_park_obj.tariff.first_hour_fee
    assert response.context['object'].tariff.maximum_additional_fee == car_park_obj.tariff.maximum_additional_fee
    assert response.context['object'].tariff.additional_fee_description \
           == car_park_obj.tariff.additional_fee_description

    zipped_categories = zip(response.context['object'].categories.all(), car_park_obj.categories.all())
    for category_response, category_fixture in zipped_categories:
        assert category_response.name == category_fixture.name
        assert category_response.description == category_fixture.description


@pytest.mark.django_db
def test_add_car_park_1(client: Client):
    """
    Test add a car park to the database.
    Car park without categories and free of charge.
    """
    assert len(CarPark.objects.all()) == 0
    assert len(Tariff.objects.all()) == 0
    post_data = {
        'name': 'New Car Park',
        'description': 'New description',
        'longitude': '22.5640742804202',
        'latitude': '51.2464395',
        'free_of_charge': 'on',
    }
    response = client.post(reverse('add_car_park'), post_data)
    assert CarPark.objects.count() == 1
    assert Tariff.objects.count() == 0
    assert response.status_code == 302


@pytest.mark.django_db
def test_add_car_park_2(client: Client):
    """
    Test add a car park to the database.
    Car park without categories, with a car park tariff.
    """
    assert len(CarPark.objects.all()) == 0
    assert len(Tariff.objects.all()) == 0
    post_data = {
        'name': 'New Car Park',
        'description': 'New description',
        'longitude': '22.5640742804202',
        'latitude': '51.2464395',
        'free_of_charge': '',
        'tariffs_name': 'New TarRiF',
        'first_hour_fee': '4',
        'maximum_additional_fee': '567',
        'additional_fee_description': 'No ticket',
    }
    response = client.post(reverse('add_car_park'), post_data)
    assert CarPark.objects.count() == 1
    assert Tariff.objects.count() == 1
    assert response.status_code == 302


@pytest.mark.django_db
def test_add_car_park_3(client: Client):
    """
    Test add a car park to the database.
    Car park with two categories, with a car park tariff.
    """
    category_obj_1 = Category.objects.create(
        name='category Name ONE',
        description='category description ONE',
    )
    category_obj_2 = Category.objects.create(
        name='category Name TWO',
        description='category description TWO',
    )
    assert len(CarPark.objects.all()) == 0
    assert len(Tariff.objects.all()) == 0
    post_data = {
        'name': 'New Car Park',
        'description': 'New description',
        'longitude': '22.5640742804202',
        'latitude': '51.2464395',
        'free_of_charge': '',
        'tariffs_name': 'New TarRiF',
        'first_hour_fee': '4',
        'maximum_additional_fee': '567',
        'additional_fee_description': 'No ticket',
        'categories': [f'{category_obj_1.pk}', f'{category_obj_2.pk}'],
    }
    response = client.post(reverse('add_car_park'), post_data)
    assert CarPark.objects.count() == 1
    assert Tariff.objects.count() == 1
    assert CarPark.objects.first().categories.count() == 2
    assert response.status_code == 302


@pytest.mark.django_db
def test_signup_view_1(client: Client):
    """Test user registration on the website."""
    assert len(User.objects.all()) == 0
    post_data = {
        'username': 'test_user',
        'password1': 'very?secret',
        'password2': 'very?secret',
        'first_name': 'Alex',
        'last_name': 'Smith',
        'email': 'very@email.com',
    }
    response = client.post(reverse('signup'), post_data)
    assert User.objects.count() == 1
    assert response.url == '/login/'
    assert response.status_code == 302


@pytest.mark.django_db
def test_signup_view_2(client: Client):
    """
    Test user registration on the website.
    User provide passwords that does not match.
    """
    assert len(User.objects.all()) == 0
    post_data = {
        'username': 'test_user',
        'password1': 've',
        'password2': 'not matching',
        'first_name': 'Alex',
        'last_name': 'Smith',
        'email': 'very@email.com',
    }
    response = client.post(reverse('signup'), post_data)
    assert User.objects.count() == 0
    assert response.status_code == 200


@pytest.mark.django_db
def test_signup_view_3(client: Client):
    """
    Test user registration on the website.
    User provide too short passwords.
    """
    assert len(User.objects.all()) == 0
    post_data = {
        'username': 'test_user',
        'password1': 'short',
        'password2': 'short',
        'first_name': 'Alex',
        'last_name': 'Smith',
        'email': 'very@email.com',
    }
    response = client.post(reverse('signup'), post_data)
    assert User.objects.count() == 0
    assert response.status_code == 200


@pytest.mark.django_db
def test_login_view_1(test_user: User, client: Client):
    """Test the login of a registered user."""
    post_data = {
        'username': 'test_user',
        'password': 'very?secret',
    }
    login_result = client.login(**post_data)
    assert login_result
    response = client.post(reverse('login'), post_data)
    assert response.status_code == 302


@pytest.mark.django_db
def test_login_view_2(test_user: User, client: Client):
    """Test the login of an unregistered user."""
    post_data = {
        'username': 'non-exist',
        'password': 'any password',
    }
    login_result = client.login(**post_data)
    assert login_result is False
    response = client.post(reverse('login'), post_data)
    assert response.status_code == 200


@pytest.mark.django_db
def test_add_opinion_not_logged_in(client: Client, car_park: CarPark):
    """Test of adding opinion by a not logged in user."""
    assert Opinion.objects.count() == 0
    car_park_obj, *_ = car_park

    response = client.get(reverse('add_opinion', args=[car_park_obj.pk]))
    assert response.status_code == 302
    assert response.url == reverse('login') + '?next=' + reverse('add_opinion', args=[car_park_obj.pk])

    post_data = {
        'opinion': 'user opinion about the car park',
        'stars': '5',
        'recommendation': '1',
    }
    response = client.post(reverse('add_opinion', args=[car_park_obj.pk]), post_data)
    assert response.url == reverse('login') + '?next=' + reverse('add_opinion', args=[car_park_obj.pk])
    assert response.status_code == 302
    assert Opinion.objects.count() == 0


@pytest.mark.django_db
def test_add_opinion_logged_in_1(test_user: User, client: Client, car_park: CarPark):
    """Test of adding opinion by a logged in user."""
    assert Opinion.objects.count() == 0
    car_park_obj, *_ = car_park

    client.force_login(test_user)
    response = client.get(reverse('add_opinion', args=[car_park_obj.pk]))
    assert response.status_code == 200

    post_data = {
        'opinion': 'user opinion about the car park',
        'stars': '5',
        'recommendation': '1',
    }
    response = client.post(reverse('add_opinion', args=[car_park_obj.pk]), post_data)
    assert response.status_code == 302
    assert Opinion.objects.count() == 1


@pytest.mark.django_db(transaction=True)
def test_add_opinion_logged_in_2(test_user: User, client: Client, car_park: CarPark):
    """
    Test of adding another opinion to the same car park by a logged in user.
    """
    assert Opinion.objects.count() == 0
    car_park_obj, *_ = car_park

    client.force_login(test_user)

    opinion_data = {
        'opinion': 'first user opinion',
        'stars': 5,
        'car_park': car_park_obj,
        'user': test_user,
        'votes': 1,
    }
    Opinion.objects.create(**opinion_data)

    response = client.get(reverse('add_opinion', args=[car_park_obj.pk]))
    assert response.status_code == 200

    opinion_data_2 = {
        'opinion': 'second user opinion',
        'stars': 5,
        'car_park': car_park_obj,
        'user': test_user,
        'votes': 1,
    }
    with pytest.raises(IntegrityError):
        Opinion.objects.create(**opinion_data_2)

    post_data = {
        'opinion': 'user opinion about the car park',
        'stars': '5',
        'recommendation': '1',
    }
    response = client.post(reverse('add_opinion', args=[car_park_obj.pk]), post_data)
    assert response.context['msg'] == 'Twoja opinia na temat tego parkingu została już dodana.'
    assert response.status_code == 200
    assert Opinion.objects.count() == 1
