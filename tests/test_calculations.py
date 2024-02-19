import datetime
import random
from math import ceil
from unittest import mock

import pytest

import defaults
from calculations import Calculations


class TestCalculations:

    def test__get_surcharge_by_cart_value_value_is_less_than_min_value(self):
        cart_value = random.randint(0, defaults.MIN_CART_VALUE - 1)

        assert Calculations()._get_surcharge_by_cart_value(cart_value) == defaults.MIN_CART_VALUE - cart_value

    def test__get_surcharge_by_cart_value_value_is_min_value(self):
        assert Calculations()._get_surcharge_by_cart_value(defaults.MIN_CART_VALUE) == 0

    def test__get_surcharge_by_cart_value_value_is_more_than_min_value(self):
        cart_value = (defaults.MIN_CART_VALUE +
                      random.randint(1, defaults.CART_VALUE_FREE_DELIVERY - defaults.MIN_CART_VALUE - 1))

        assert Calculations()._get_surcharge_by_cart_value(cart_value) == 0

    def test__get_surcharge_by_distance_included_distance(self):
        distance = random.randint(0, defaults.INCLUDED_DISTANCE - 1)

        assert Calculations()._get_surcharge_by_distance(distance) == defaults.MIN_DISTANCE_SURCHARGE

    def test__get_surcharge_by_distance_max_included_distance(self):
        assert Calculations()._get_surcharge_by_distance(defaults.INCLUDED_DISTANCE) == defaults.MIN_DISTANCE_SURCHARGE

    def test__get_surcharge_by_distance_distance_is_one_meter_more_than_included(self):
        distance = defaults.INCLUDED_DISTANCE + 1

        assert (Calculations()._get_surcharge_by_distance(distance) ==
                defaults.MIN_DISTANCE_SURCHARGE + defaults.FEE_FOR_DISTANCE_INTERVAL)

    def test__get_surcharge_by_distance_distance_is_more_than_included(self):
        distance = random.randint(defaults.INCLUDED_DISTANCE + 2, defaults.MAX_DISTANCE)
        num_of_extra_intervals = ceil((distance - defaults.INCLUDED_DISTANCE) / defaults.DISTANCE_INTERVAL)
        expected_surcharge = (defaults.MIN_DISTANCE_SURCHARGE +
                              defaults.FEE_FOR_DISTANCE_INTERVAL * num_of_extra_intervals)

        assert Calculations()._get_surcharge_by_distance(distance) == expected_surcharge, f'distance is {distance}'

    def test__get_surcharge_by_distance_distance_is_on_the_top_edge_of_an_extra_interval(self):
        distance = random.randrange(defaults.INCLUDED_DISTANCE + defaults.DISTANCE_INTERVAL,
                                    defaults.MAX_DISTANCE, defaults.DISTANCE_INTERVAL)
        num_of_extra_intervals = (distance - defaults.INCLUDED_DISTANCE) / defaults.DISTANCE_INTERVAL
        expected_surcharge = (defaults.MIN_DISTANCE_SURCHARGE +
                              defaults.FEE_FOR_DISTANCE_INTERVAL * num_of_extra_intervals)

        assert Calculations()._get_surcharge_by_distance(distance) == expected_surcharge, f'distance is {distance}'

    @pytest.mark.parametrize("num_of_items",
                             [random.randint(1, defaults.INCLUDED_ITEMS - 1),
                              defaults.INCLUDED_ITEMS])
    def test__get_surcharge_by_num_of_items_free_items(self, num_of_items):
        assert Calculations()._get_surcharge_by_num_of_items(num_of_items) == 0

    @pytest.mark.parametrize("num_of_items",
                             [defaults.INCLUDED_ITEMS + 1,
                              defaults.BULK_ITEMS - 1])
    def test__get_surcharge_by_num_of_items_items_with_additional_fee(self, num_of_items):
        expected_surcharge = (num_of_items - defaults.INCLUDED_ITEMS) * defaults.EXTRA_ITEMS_FEE

        assert Calculations()._get_surcharge_by_num_of_items(num_of_items) == expected_surcharge

    @pytest.mark.parametrize("num_of_items",
                             [defaults.BULK_ITEMS,
                              defaults.MAX_ITEMS_NUM])
    def test__get_surcharge_by_num_of_items_items_with_bulk_fee(self, num_of_items):
        expected_surcharge = ((num_of_items - defaults.INCLUDED_ITEMS) * defaults.EXTRA_ITEMS_FEE +
                              defaults.BULK_ITEMS_FEE)

        assert Calculations()._get_surcharge_by_num_of_items(num_of_items) == expected_surcharge

    @pytest.mark.parametrize("time",
                             [f"T{defaults.RUSH_START}Z",
                              f"T{defaults.RUSH_END}Z"])
    def test__check_for_rush_time_rush_time(self, time):
        date = datetime.date.today()
        while date.isoweekday() not in defaults.RUSH_DAYS:
            date += datetime.timedelta(days=1)

        date_time = str(date) + time

        assert Calculations()._check_for_rush_time(date_time), f'time is {date_time}, check if it is the rush time'

    @pytest.mark.parametrize("time",
                             [f"T{defaults.RUSH_START}Z",
                              f"T{defaults.RUSH_END}Z"])
    def test__check_for_rush_time_rush_hours_wrong_day(self, time):
        date = datetime.date.today()
        while date.isoweekday() in defaults.RUSH_DAYS:
            date += datetime.timedelta(days=1)

        date_time = str(date) + time

        assert Calculations()._check_for_rush_time(date_time) is not True, \
            f'time is {date_time}, check if it is the rush time'

    def test__check_for_rush_time_rush_day_just_before_rush_time(self):
        date = datetime.date.today()
        while date.isoweekday() not in defaults.RUSH_DAYS:
            date += datetime.timedelta(days=1)

        combined_date = datetime.datetime.combine(date, datetime.time.fromisoformat(defaults.RUSH_START))
        combined_date += datetime.timedelta(seconds=-1)
        formatted_combined_date = combined_date.isoformat() + 'Z'

        assert Calculations()._check_for_rush_time(formatted_combined_date) is not True, \
            f'time is {combined_date}, check if it is the rush time'

    def test__check_for_rush_time_rush_day_right_after_rush_time(self):
        date = datetime.date.today()
        while date.isoweekday() not in defaults.RUSH_DAYS:
            date += datetime.timedelta(days=1)

        combined_date = datetime.datetime.combine(date, datetime.time.fromisoformat(defaults.RUSH_END))
        combined_date += datetime.timedelta(seconds=1)
        formatted_combined_date = combined_date.isoformat() + 'Z'

        assert Calculations()._check_for_rush_time(formatted_combined_date) is not True, \
            f'time is {combined_date}, check if it is the rush time'

    @pytest.mark.parametrize("cart_value",
                             [defaults.CART_VALUE_FREE_DELIVERY,
                              random.randint(defaults.CART_VALUE_FREE_DELIVERY + 1, defaults.MAX_CART_VALUE)])
    def test_get_delivery_fee_free_delivery_by_card_value(self, cart_value):
        delivery_distance, number_of_items, order_time = 0, 0, ''

        assert Calculations().get_delivery_fee(cart_value, delivery_distance, number_of_items, order_time) == 0

    @mock.patch('calculations.Calculations._check_for_rush_time',
                return_value=defaults.PLACEHOLDERS['check_rush'])
    @mock.patch('calculations.Calculations._get_surcharge_by_num_of_items',
                return_value=defaults.PLACEHOLDERS['number_of_items'])
    @mock.patch('calculations.Calculations._get_surcharge_by_distance',
                return_value=defaults.PLACEHOLDERS['delivery_distance'])
    @mock.patch('calculations.Calculations._get_surcharge_by_cart_value',
                return_value=defaults.PLACEHOLDERS['cart_value'])
    def test_get_delivery_fee_paid_delivery_by_card_value(self, res_by_cart, res_by_dist, res_by_items, _):
        cart_value = defaults.CART_VALUE_FREE_DELIVERY - 1

        assert (Calculations().get_delivery_fee(cart_value, defaults.PLACEHOLDERS['delivery_distance'],
                                                defaults.PLACEHOLDERS['number_of_items'],
                                                defaults.PLACEHOLDERS['order_time']) ==
                res_by_cart() + res_by_dist() + res_by_items())

    @mock.patch('calculations.Calculations._check_for_rush_time',
                return_value=defaults.PLACEHOLDERS['check_rush'])
    @mock.patch('calculations.Calculations._get_surcharge_by_num_of_items',
                return_value=defaults.PLACEHOLDERS['number_of_items'])
    @mock.patch('calculations.Calculations._get_surcharge_by_distance',
                return_value=defaults.FEE_LIMIT)
    @mock.patch('calculations.Calculations._get_surcharge_by_cart_value',
                return_value=defaults.PLACEHOLDERS['cart_value'])
    def test_get_delivery_fee_check_limit_fee_rush_false(self, *_args):
        assert (Calculations().get_delivery_fee(defaults.PLACEHOLDERS['cart_value'],
                                                defaults.PLACEHOLDERS['delivery_distance'],
                                                defaults.PLACEHOLDERS['number_of_items'],
                                                defaults.PLACEHOLDERS['order_time']) == defaults.FEE_LIMIT)

    @mock.patch('calculations.Calculations._check_for_rush_time',
                return_value=True)
    @mock.patch('calculations.Calculations._get_surcharge_by_num_of_items',
                return_value=defaults.PLACEHOLDERS['number_of_items'])
    @mock.patch('calculations.Calculations._get_surcharge_by_distance',
                return_value=defaults.PLACEHOLDERS['delivery_distance'])
    @mock.patch('calculations.Calculations._get_surcharge_by_cart_value',
                return_value=defaults.PLACEHOLDERS['cart_value'])
    def test_get_delivery_fee_check_rush_time_multiplication(self, res_by_cart, res_by_dist, res_by_items, _):
        assert (Calculations().get_delivery_fee(defaults.PLACEHOLDERS['cart_value'],
                                                defaults.PLACEHOLDERS['delivery_distance'],
                                                defaults.PLACEHOLDERS['number_of_items'],
                                                defaults.PLACEHOLDERS['order_time']) ==
                int((res_by_cart() + res_by_dist() + res_by_items()) * defaults.RUSH_TIME_MULTIPLIER))

    @mock.patch('calculations.Calculations._check_for_rush_time',
                return_value=True)
    @mock.patch('calculations.Calculations._get_surcharge_by_num_of_items',
                return_value=defaults.PLACEHOLDERS['number_of_items'])
    @mock.patch('calculations.Calculations._get_surcharge_by_distance',
                return_value=defaults.PLACEHOLDERS['delivery_distance'])
    @mock.patch('calculations.Calculations._get_surcharge_by_cart_value',
                return_value=defaults.FEE_LIMIT - defaults.
                PLACEHOLDERS['delivery_distance'] - defaults.PLACEHOLDERS['number_of_items'] - 1)
    def test_get_delivery_fee_check_limit_fee_reached_because_of_rush_time(self, *_args):
        assert (Calculations().get_delivery_fee(defaults.PLACEHOLDERS['cart_value'],
                                                defaults.PLACEHOLDERS['delivery_distance'],
                                                defaults.PLACEHOLDERS['number_of_items'],
                                                defaults.PLACEHOLDERS['order_time']) == defaults.FEE_LIMIT)

    @mock.patch('calculations.Calculations._check_for_rush_time',
                return_value=True)
    @mock.patch('calculations.Calculations._get_surcharge_by_num_of_items',
                return_value=defaults.FEE_LIMIT)
    @mock.patch('calculations.Calculations._get_surcharge_by_distance',
                return_value=defaults.PLACEHOLDERS['delivery_distance'])
    @mock.patch('calculations.Calculations._get_surcharge_by_cart_value',
                return_value=defaults.PLACEHOLDERS['cart_value'])
    def test_get_delivery_fee_check_limit_fee_reached_plus_rush_time_multiplication(self, *_args):
        assert (Calculations().get_delivery_fee(defaults.PLACEHOLDERS['cart_value'],
                                                defaults.PLACEHOLDERS['delivery_distance'],
                                                defaults.PLACEHOLDERS['number_of_items'],
                                                defaults.PLACEHOLDERS['order_time']) == defaults.FEE_LIMIT)
