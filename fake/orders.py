import pandas as pd # type: ignore
import numpy as np
from fake.customer import generate_customers
from fake.sku import generate_skus
from datetime import datetime
import logging

from typing import Tuple, List, Dict, Union, Any

log_fmt = '%(asctime)s %(name)-10s %(levelname)-4s %(funcName)-14s %(message)s'
logging.basicConfig(level=logging.INFO, format=log_fmt, datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)


def get_offset_date(date:Union[pd.Timestamp, None]=None, offset_range_start:int=1,
                    offset_range_end:int=10, seed:Union[int, None]=None) -> datetime:
    '''
    Get transaction offset date

    Example
    -------
    order_date = pd.to_datetime('2021-02-15')
    get_offset_date(order_date, seed=42)
    > Timestamp('2021-02-22 00:00:00')

    Parameters
    ----------
    date: base transaction date to add/subtract offset to

    offset_range_start: lower range offset in days

    offset_range_end: upper range offset in days

    seed: int, default None - used for testing to deliver consistent results

    Returns
    -------

    '''
    if seed:
        np.random.seed(seed)

    if date is None:
        _date = pd.to_datetime(datetime.now())
    else:
        _date = date

    offset = np.random.randint(offset_range_start, offset_range_end)
    _date = _date + pd.Timedelta(offset, 'D')

    return _date


def get_order_types(filename:str='inputs/fake_data/order_types.tsv') -> pd.DataFrame:
    '''
    Get order types

    Parameters
    ----------
    filename: location of order types data

    Returns
    -------
    order types (pd.DataFrame)
    '''

    order_types = pd.read_csv(filename, sep='\t')

    return order_types


def generate_order(company='8500', year='2021', month=1, order_type=None,
                   order_no=1, max_lines=1, customers=None, products=None,
                   seed:Union[int, None]=None) -> List[Dict[str, Any]]:
    '''
    Generate order record(s)


    Example
    -------
    company: company code


    Parameters
    ----------

    year: order year to be applied to this order

    month: order month to be applied to this order

    order_type: order type, default None -> use 'SA'

    order_no: order number to be applied

    lines: number of order lines

    customers: list of customers from which to select against order

    products: list of products from which to select against order

    seed: int, default None - used for testing to deliver consistent results

    Returns
    -------
    order (dict)

    '''
    if seed:
        np.random.seed(seed)

    if order_type is None:
        order_type = 'SA'

    order_day = np.random.randint(1, 28)
    order_date = pd.to_datetime(f'{year}-{month}-{order_day}')

    shipping_date = get_offset_date(order_date, 1, 4)
    delivery_date = get_offset_date(shipping_date, 1, 5)

    customer_idx = np.random.randint(low=1, high=customers.shape[0], size=1)[0]
    customer = customers.iloc[customer_idx]

    if max_lines > 1:
        lines = np.random.randint(low=1, high=max_lines+1, size=1)[0]
        order_line_range = range(lines)
    else:
        order_line_range = range(1)

    order = []
    for line in order_line_range:

        sku_idx = np.random.randint(low=1, high=products.shape[0], size=1)[0]
        sku = products.iloc[sku_idx]

        discounts = [.10, .20, .40, .60, 0]
        discount = np.random.choice(discounts, size=1, p=[.1, .1, .05, .05, .7])[0]

        data = {
            'order_no': order_no,
            'order_type': order_type,
            'company': company,
            'order_line': line+1,
            'order_date': order_date,
            'shipping_date': shipping_date,
            'delivery_date': delivery_date,
            'customer_no': customer['customer_no'],
            'product_code': sku['sku'],
            'description': sku['brand_name'],
            'order_quantity': np.random.randint(low=1, high=40, size=1)[0],
            'unit_price': sku['list_price'],
            'discount_%': discount
        }

        order.append(data)

    return order


def generate_orders(year='2021', number_orders = 2, max_lines=3, order_start=200000,
                    order_types=None, customers=None, skus=None, seed=None):
    '''


    seed: int, default None - used for testing to deliver consistent results

    Returns
    -------
    orders (DataFrame)

    '''
    if seed:
        np.random.seed(seed)

    if order_types is None:
        order_types = get_order_types()

    if customers is None:
        customers = generate_customers()

    if skus is None:
        skus = generate_skus()

    # Monthly weighting to vary frequency of generated orders
    month_weights = [1, 4, 3, 8, 4, 5, 5, 3, 4, 6, 7, 2]
    month_weights = list(map(lambda x: x/sum(month_weights), month_weights))

    type_weights = [6, 1, 2, 2, 2, 3, 2]
    type_weights = list(map(lambda x: x/sum(type_weights), type_weights))

    df_orders = pd.DataFrame(None)
    for order_no in range(order_start, order_start+number_orders):

        month = np.random.choice(range(1, 13), size=1, p=month_weights)[0]
        order_type = np.random.choice(order_types.type_, size=1, p=type_weights)[0]

        order = generate_order(month=month, order_no=order_no,
                               max_lines=max_lines, order_type=order_type,
                               customers=customers, products=skus)

        df_order = pd.DataFrame(order)
        df_orders = pd.concat([df_orders, df_order])

    df_orders = df_orders.reset_index(drop=True)

    return df_orders
