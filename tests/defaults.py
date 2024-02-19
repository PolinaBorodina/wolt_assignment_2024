MIN_CART_VALUE = 1000
CART_VALUE_FREE_DELIVERY = 20000
MAX_CART_VALUE = 10000000  # warn! it's a supposed max cart value. Can be changed if any requirements appear
MIN_DISTANCE_SURCHARGE = 200
INCLUDED_DISTANCE = 1000
DISTANCE_INTERVAL = 500
FEE_FOR_DISTANCE_INTERVAL = 100
MAX_DISTANCE = 6500  # warn! it's a supposed max delivery distance. Can be changed if any requirements appear
INCLUDED_ITEMS = 4
EXTRA_ITEMS_FEE = 50
BULK_ITEMS = 13
BULK_ITEMS_FEE = 120
MAX_ITEMS_NUM = 24  # warn! it's a supposed max number of items. Can be changed if any requirements appear
FEE_LIMIT = 1500
RUSH_TIME_MULTIPLIER = 1.2
RUSH_DAYS = [5]  # from 1 for monday to 7 for saturday
RUSH_START = '15:00:00'
RUSH_END = '19:00:00'
PLACEHOLDERS = {'cart_value': 1,
                'delivery_distance': 1,
                'number_of_items': 1,
                'order_time': "2024-01-15T13:00:00Z",
                'check_rush': False,
                'default_fee': 710,
                }
