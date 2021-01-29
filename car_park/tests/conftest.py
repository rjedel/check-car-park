from datetime import datetime
from decimal import Decimal

import pytest
from django.contrib.auth.models import User
from django.test import Client

from car_park.models import CarPark, Tariff, Category


@pytest.fixture
def client():
    """Create a dummy web browser."""
    client = Client()
    return client


@pytest.fixture
def car_park():
    """Create a dummy car park object with tariff and categories."""
    tariff_obj = Tariff.objects.create(
        tariffs_name='TeSt TaRiFfS Name',
        first_hour_fee=Decimal('20.50'),
        maximum_additional_fee=Decimal('120.03'),
        additional_fee_description='additional fee description',
    )
    category_obj_1 = Category.objects.create(
        name='category Name ONE',
        description='category description ONE',
    )
    category_obj_2 = Category.objects.create(
        name='category Name TWO',
        description='category description TWO',
    )
    category_obj_3 = Category.objects.create(
        name='category Name Three',
        description='',
    )
    car_park_obj = CarPark.objects.create(
        name='tEsT cArPaRk NaMe',
        description='cp description',
        location='0101000020E6100000E20511A9699136409E6D24BF34A14940',
        created=datetime(2021, 1, 25, 22, 27, 47, 947197),
        update=datetime(2021, 1, 29, 23, 10, 47, 947197),
        free_of_charge=True,
    )
    car_park_obj.tariff = tariff_obj
    car_park_obj.save()
    car_park_obj.categories.set([category_obj_1, category_obj_2, category_obj_3])
    return car_park_obj, tariff_obj, category_obj_1, category_obj_2, category_obj_3


@pytest.fixture
def test_user():
    """Create a dummy user."""
    user_data = {
        'username': 'test_user',
        'password': 'very?secret',
        'first_name': 'Alex',
        'last_name': 'Smith',
        'email': 'very@email.com',
    }
    test_user = User.objects.create_user(**user_data)
    return test_user
