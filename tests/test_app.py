from unittest import mock
import pytest

import defaults

from app import app


@pytest.fixture()
def application():
    application = app

    yield application


@pytest.fixture()
def client(application):
    return app.test_client()


@mock.patch('calculations.Calculations.get_delivery_fee', return_value=defaults.PLACEHOLDERS['default_fee'])
def test_calc_delivery_fee_response(_, client):
    response = client.post("/calc_fee", json={
        "cart_value": defaults.PLACEHOLDERS['cart_value'],
        "delivery_distance": defaults.PLACEHOLDERS['delivery_distance'],
        "number_of_items": defaults.PLACEHOLDERS['number_of_items'],
        "time": defaults.PLACEHOLDERS['order_time']
    })

    assert response.status_code == 200, f'status code of response ({response.status_code}) is not 200'
    assert response.content_type == 'application/json', \
        f'content type of response ({response.content_type}) is not application/json'
    assert {'delivery_fee': defaults.PLACEHOLDERS['default_fee']} == response.json, \
        (f"response content can be wrong, "
         f"expected: {{'delivery_fee': {defaults.PLACEHOLDERS['default_fee']}}}, actual: {response.json}")
