from _datetime import datetime, time
from math import ceil

MIN_CART_VALUE = 1000
MIN_SURCHARGE_BY_DISTANCE = 200
INCLUDED_DISTANCE = 1000
EXTRA_DISTANCE_INTERVAL = 500
FEE_FOR_EXTRA_INTERVAL = 100
INCLUDED_ITEMS = 4
EXTRA_ITEMS_FEE = 50
BULK_ITEMS = 13
FEE_FOR_BULK_ITEMS = 120
CART_VALUE_FREE_DELIVERY = 20000
DELIVERY_FEE_LIMIT = 1500
RUSH_TIME_MULTIPLIER = 1.2
RUSH_START = '15:00:00'
RUSH_END = '19:00:00'
RUSH_DAYS = [5]  # from 1 for monday to 7 for saturday


class Calculations:

    @staticmethod
    def _get_surcharge_by_cart_value(value):
        surcharge = 0
        min_cart_value = MIN_CART_VALUE

        if value < min_cart_value:
            surcharge = min_cart_value - value

        return surcharge

    @staticmethod
    def _get_surcharge_by_distance(distance):
        min_surcharge = MIN_SURCHARGE_BY_DISTANCE
        included_distance = INCLUDED_DISTANCE
        extra_distance_interval = EXTRA_DISTANCE_INTERVAL
        fee_for_extra_interval = FEE_FOR_EXTRA_INTERVAL

        if distance > included_distance:
            surcharge = (min_surcharge +
                         ceil((distance - included_distance)/extra_distance_interval) * fee_for_extra_interval)
            return surcharge

        return min_surcharge

    @staticmethod
    def _get_surcharge_by_num_of_items(num_of_items):
        surcharge = 0
        included_items = INCLUDED_ITEMS
        extra_items_fee = EXTRA_ITEMS_FEE
        bulk_items = BULK_ITEMS
        fee_for_bulk_items = FEE_FOR_BULK_ITEMS

        if num_of_items > included_items:
            surcharge += (num_of_items - included_items) * extra_items_fee
            if num_of_items >= bulk_items:
                surcharge += fee_for_bulk_items

        return surcharge

    @staticmethod
    def _check_for_rush_time(order_time):
        """
        warn!
        rush_end time will be included into the rush time interval.
        I have not found instructions should it be the rush time or not, so, if should not, the next string
        if rush_start <= datetime.time(date_with_time) <= rush_end:
        can be changed to
        if rush_start <= datetime.time(date_with_time) < rush_end:
        """
        if order_time.endswith('Z'):  # to provide compatibility with python < 3.11
            order_time = order_time.rstrip('Z')
        date_with_time = datetime.fromisoformat(order_time)
        rush_days = RUSH_DAYS
        rush_start = time.fromisoformat(RUSH_START)
        rush_end = time.fromisoformat(RUSH_END)
        if datetime.isoweekday(date_with_time) in rush_days and rush_start <= datetime.time(date_with_time) <= rush_end:
            return True

    def get_delivery_fee(self, cart_value: int, delivery_distance: int, number_of_items: int, order_time: str) -> int:
        cart_value_free_delivery = CART_VALUE_FREE_DELIVERY
        delivery_fee_limit = DELIVERY_FEE_LIMIT
        rush_time_multiplier = RUSH_TIME_MULTIPLIER

        if cart_value >= cart_value_free_delivery:
            return 0

        surcharge_by_cart_value = self._get_surcharge_by_cart_value(cart_value)
        surcharge_by_distance = self._get_surcharge_by_distance(delivery_distance)
        surcharge_by_num_of_items = self._get_surcharge_by_num_of_items(number_of_items)
        delivery_fee = (surcharge_by_cart_value + surcharge_by_distance + surcharge_by_num_of_items)

        if self._check_for_rush_time(order_time):
            delivery_fee = delivery_fee * rush_time_multiplier

        if delivery_fee > delivery_fee_limit:
            return delivery_fee_limit

        return int(delivery_fee)
