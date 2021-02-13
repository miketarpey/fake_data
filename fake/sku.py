import pandas as pd # type: ignore
import numpy as np
import logging
from typing import List, Union

log_fmt = '%(asctime)s %(name)-10s %(levelname)-4s %(funcName)-14s %(message)s'
logging.basicConfig(level=logging.INFO, format=log_fmt, datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)


def generate_status(choices:List=[1, 0], weights:List=[0.9, 0.1], seed=None) -> Union[str, int]:
    ''' Generate status (for example for a sku, order, shipnote etc.)

    Example
    -------
    generate_status()
    > 1

    generate_status(choices=['A', 'D'], weights=[0, 10], seed=42)
    > 'D'

    Parameters
    ----------
    choices: list of possible status choices. defaults[1, 0]

    weights: list of probabilties to skew returned distribution of returned statuses

    seed: int, default None - used for testing to deliver consistent results

    Returns
    -------
    status
    '''

    weights = list(map(lambda x: x/sum(weights), weights))

    status = np.random.choice(choices, size=1, p=weights)[0]

    return status


def generate_sku(sections:int=1, chars_per_section:int=2,
                 delimitter:str='-', seed:int=None) -> str:
    '''
    Generate SKU code

    Example
    -------
    generate_sku(sections=1, chars_per_section=2, delimitter='-'):
    > 'PQ-18416'

    Parameters
    ----------
    sections: default 1

    chars_per_section: default 2

    delimitter: default '-'

    seed: default None - used for testing to deliver consistent results

    Returns
    -------
    sku
    '''

    if seed:
        np.random.seed(seed)

    chars = list('abcdefghijklmnopqrstuvwxyz0123456789'.upper())

    get_chars = lambda : ''.join(np.random.choice(chars, size=chars_per_section))
    section_codes = [get_chars() for _ in range(1, sections+1)]
    sku = delimitter.join(section_codes)

    item_suffix = ''.join(str(np.random.randint(low=1, high=20000, size=1)[0]))

    sku = delimitter.join((sku, item_suffix))

    return sku


def generate_uom(uoms:List=['EA', 'VL', 'PK'], weights:List=[7, 2, 1],
                 seed:int=None) -> str:
    ''' Generate selected unit of measure

    Example
    -------
    generate_uom()
    > 'EA'

    Parameters
    ----------
    uoms: list of supplied units of measure to be used

    seed: default None - used for testing to deliver consistent results

    Returns
    -------
    uom
    '''
    if seed:
        np.random.seed(seed)

    weights = list(map(lambda x: x/sum(weights), weights))
    uom = np.random.choice(uoms, size=1, p=weights)[0]

    return uom


def generate_packfactor(pack_factors:List=[6, 12, 60, 100],
                        weights:List=[1, 4, 4, 1], seed:int=None) -> int:
    ''' Generate pack factor value

    Example
    -------
    generate_packfactor()
    > 24

    Parameters
    ----------
    pack_factors: list of supplied pack factors to be used

    seed: int, default None - used for testing to deliver consistent results

    Returns
    -------
    packfactor (int)
    '''

    weights = list(map(lambda x: x/sum(weights), weights))
    pack_factor = np.random.choice(pack_factors, size=1, p=weights)[0]

    return pack_factor


def generate_price(lower:int=1, upper:int=20, precision:int=4, seed:int=None) -> float:
    ''' generate list or contract price.

    Example
    -------
    generate_price(precision=5)
    > 6.78119

    Parameters
    ----------
    lower: default 1

    upper: default 20

    precision: default 4

    seed: default None - used for testing to deliver consistent results

    Returns
    -------
    price

    '''
    if seed:
        np.random.seed(seed)

    price = np.random.uniform(lower, upper)
    price = round(price, precision)

    return price


def generate_skus(sku_names:str='inputs/fake_data/sku_names.csv')-> pd.DataFrame:
    '''
    generate sku / item master record

    Example
    -------
    generate_skus()

    Parameters
    ----------
    sku_names: folder/file path to list of sku names
    '''
    skus = pd.read_csv(sku_names, sep='\t')

    item_data = []
    for row in skus.itertuples():
        row = {'sku': generate_sku(1, 3, '-'),
               'status': generate_status(),
               'brand_name': row[1].upper(),
               'generic_name': row[2].upper(),
               'pack_factor': generate_packfactor(),
               'uom': generate_uom(),
               'list_price': generate_price()}
        item_data.append(row)

    df = pd.DataFrame(item_data)

    return df
