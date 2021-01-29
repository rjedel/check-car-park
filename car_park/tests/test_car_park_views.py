import pytest
from django.test import Client

from car_park.models import CarPark


@pytest.mark.django_db
def test_car_park_detail(client: Client, car_park: CarPark):
    car_park_obj, tariff_obj, category_obj_1, category_obj_2, category_obj_3 = car_park

    response = client.get(f'/car_park_detail/{car_park_obj.id}/')

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
