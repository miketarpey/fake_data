import pandas as pd
import pytest
from fake.customer import *
from fake.orders import *
from fake.sku import *
from pandas import Timestamp


def test_get_offset_date_with_pandas_timestamp():
    '''
    '''
    order_date = pd.to_datetime('2021-02-15 13:45:47.536960')

    expected = pd.to_datetime('2021-02-22 13:45:47.536960')
    actual = get_offset_date(order_date, seed=42)

    assert expected == actual


def test_get_offset_date_with_datetime():
    '''
    '''
    order_date = datetime.strptime('2021-02-15', '%Y-%m-%d')

    expected = datetime(2021, 2, 22, 0, 0)
    actual = get_offset_date(order_date, seed=42)

    assert expected == actual


def test_generate_order_single_line():
    '''
    '''

    expected = [{'order_no': 1, 'order_type': 'SA', 'company': '8500',
                 'order_line': 1,
                 'order_date': Timestamp('2021-01-19 00:00:00'),
                 'shipping_date': Timestamp('2021-01-21 00:00:00'),
                 'delivery_date': Timestamp('2021-01-23 00:00:00'),
                 'customer_no': 49529317,
                 'product_code': 'PAB-17511',
                 'description': 'INFLECTRA ',
                 'order_quantity': 11,
                 'unit_price': 1.9504,
                 'discount_%': 0.0}]

    np.random.seed(42)
    customers = generate_customers()
    skus = generate_skus()

    actual = generate_order(customers=customers, products=skus)

    assert expected == actual


def test_generate_order_multi_line():
    '''
    '''
    expected = [{'order_no': 1, 'order_type': 'SA', 'company': '8500', 'order_line': 1,
                  'order_date': Timestamp('2021-01-19 00:00:00'),
                  'shipping_date': Timestamp('2021-01-21 00:00:00'),
                  'delivery_date': Timestamp('2021-01-23 00:00:00'),
                  'customer_no': 49529317,
                  'product_code': '8KD-8217', 'description': 'CREON DELAYED-RELEASE CAPSULES ',
                  'order_quantity': 34, 'unit_price': 1.6796, 'discount_%': 0.0},
                 {'order_no': 1, 'order_type': 'SA', 'company': '8500', 'order_line': 2,
                  'order_date': Timestamp('2021-01-19 00:00:00'),
                  'shipping_date': Timestamp('2021-01-21 00:00:00'),
                  'delivery_date': Timestamp('2021-01-23 00:00:00'),
                  'customer_no': 49529317,
                  'product_code': 'DHA-9956', 'description': 'NEPRO WITH CARB STEADY ',
                  'order_quantity': 28, 'unit_price': 10.7362, 'discount_%': 0.0},
                 {'order_no': 1, 'order_type': 'SA', 'company': '8500', 'order_line': 3,
                  'order_date': Timestamp('2021-01-19 00:00:00'),
                  'shipping_date': Timestamp('2021-01-21 00:00:00'),
                  'delivery_date': Timestamp('2021-01-23 00:00:00'),
                  'customer_no': 49529317,
                  'product_code': 'YGW-8432', 'description': 'UPLIZNA ',
                  'order_quantity': 9, 'unit_price': 4.9791, 'discount_%': 0.0}]

    np.random.seed(42)
    customers = generate_customers()
    skus = generate_skus()

    actual = generate_order(max_lines=4, customers=customers, products=skus)

    assert expected == actual


def test_generate_multi_orders():
    '''
    '''
    np.random.seed(42)

    customers = generate_customers()
    skus      = generate_skus()

    dx = generate_orders(number_orders=2, max_lines=1, customers=customers, skus=skus)
    actual = dx.loc[dx.description == 'SOMAVERT ', 'order_quantity'].values[0]

    expected = 24
    assert expected == actual
