import pandas as pd # type: ignore
import numpy as np # type: ignore
import logging
from pathlib import Path
from datetime import datetime
from fake.sku import generate_status

from typing import Tuple, Dict, Union, Callable

log_fmt = '%(asctime)s %(name)-10s %(levelname)-4s %(funcName)-14s %(message)s'
logging.basicConfig(level=logging.INFO, format=log_fmt, datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)


def get_sample_zipcodes(filename:Union[Path, str]='zipcodes_uk.tsv', sample:int=1000, seed:Union[int, None]=None) -> pd.DataFrame:
    '''
    Get/retrieve sample zipcodes from csv/tsv text file.
    (Implemented for now for only UK postcodes)

    Parameters
    ----------
    filename: str, filename location (path)

    sample: int, number of random examples to retrieve (default=1000)

    seed: int, default None - used for testing to deliver consistent results

    Returns
    -------
    DataFrame
    '''
    if seed:
       np.random.seed(seed)

    zipcodes = pd.read_csv(filename, sep='\t')
    zipcodes = zipcodes.loc[:, 'post_code':'area_covered']

    # Make sure only single spaces found in post codes
    zipcodes.post_code = zipcodes.post_code.str.replace(r'\s{2,}', ' ', regex=True)

    codes = np.random.choice(zipcodes['post_code'], size=sample)
    subset_codes = zipcodes[zipcodes['post_code'].isin(codes)]

    return subset_codes


def get_firstnames(filename:Union[Path, str]='first_names.csv') -> pd.DataFrame:
    '''
    Get firstnames from text file

    Parameters
    ----------
    filename: str, filename location (path)

    Returns
    -------
    DataFrame
    '''
    first_names = pd.read_csv(filename, sep='\t')
    first_names = first_names.loc[:, 'Name':'Gender']

    return first_names


def get_surnames(filename:Union[Path, str]='surnames.tsv') -> pd.DataFrame:
    '''
    Get firstnames from text file

    Parameters
    ----------
    filename: str, filename location (path)

    Returns
    -------
    DataFrame
    '''
    surnames = pd.read_csv(filename, sep='\t')
    surnames = surnames.loc[:, 'Surname']

    return surnames


def generate_address(zipcodes:pd.DataFrame, house_range:Tuple=(1, 350), seed:Union[int, None]=None) -> Dict:
    ''' Generate uk address data

    Example
    -------
    generate_sku_status()
    > 1

    Parameters
    ----------
    zipcodes: DataFrame, zipcode/postcode values

    choices: tuple, list of possible status choices.
            defaults[1, 0]

    probablities: list, list of probabilties to allow skew of
        returned distribution of returned statuses

    seed: int, default None - used for testing to deliver consistent results

    Returns
    -------
    dictionary
    '''
    if seed:
        np.random.seed(seed)

    street_names = ['High', 'Station', 'Main', 'Park', 'Station', 'Warren', 'Peacock',
        'Wilson', 'Greenhill', 'Hillview', 'Elmsleigh', 'Heather', 'Arkwright',
        'Herbert', 'Greenfinch', 'Leyton', 'Roxborough', 'Charnwood', 'Larch',
        'Templeton', 'Dukes', 'Bishop', 'Astoria', 'Grosvenor', 'Roberts', 'Elmtree',
        'Highgrove', 'Old', "St. John's", 'Christchurch', 'Oakington', 'Fox',
        'Badger', 'Birdcage', 'Swallow', 'Robin', 'Henry', 'Wellesley', 'Carrington',
        'Mornington', "St. David's", 'Shepherd', 'Barnhill', 'Church', 'London',
        'Victoria', 'Lowlands', 'Green', 'Manor', 'Church', 'Park', 'Queens',
        'Newgate', 'Grange', 'Kings', 'Marquis', 'Nightingale', 'Alexander',
        'Palliser', 'Kings', 'Windsor', 'Highfield', 'Mill', 'Winston', 'Gibson',
        'Bayswater', 'Earl', "Baron's", 'Prince', 'Luther', 'Barn', 'Squirrel',
        'Alexander', 'York', 'St. John’s', 'Main', 'Lascelles', 'King', 'Batley',
        'Green', 'Springfield', 'Byron', 'Edward', 'Wallis Grove', 'Ridge', 'Hunt',
        'Castle', 'Cathedral', 'George', 'Park', 'Victoria', 'Albert', 'Charles',
        'Queens', 'New', 'West', 'Chestnut', 'North', 'East', 'Grove Hill',
        "St Ann's", "Heath", "Thatcher", "Keats", "Joyce", "Corporation", 'Baddeley',
        'Richmond', 'Woodland Heights', 'Grove', 'South', 'School', 'Denzil', 'Scally',
        'Symonds', 'Storrington', 'Hazlemere', 'Warminster', 'Cadbury', 'Eastman',
        'North', 'Castle', 'Stanley', 'Chester', 'Mill', 'Windmill', 'Bridge',
        'Farm Hill', 'Bakers', 'Vaughn', 'Katherine', 'Monk', 'Fisher', 'Eastwood']

    street_types = ['Street', 'Road', 'Lane', 'Avenue', 'Way', 'Close', 'Gardens', 'Pass',
                    'Vale', 'Mews', 'Circus', 'Place', 'Grove', 'Crescent', 'Approach',
                    'Terrace', 'Drive', 'Way', 'Square', 'Rise', 'Row', 'Walk', 'Park',
                    'Court', 'View', 'Gate']

    house_names = ['The Orchard', 'The Meadow', 'Rose Cottage', 'Holly', 'The Oak', 'Willow',
                   'The School House', 'The Willows', 'Sunnyside Inn', 'Springfield', 'Hollyrood',
                   'Corner', 'Highfield', 'The Old School', 'Primrose', 'The Mill House',
                   'The Old Rectory', 'Yew Tree Cottage', 'The Old Vicarage', 'Oaklands', 'Balmoral',
                   'The Old Post Office', 'Lilac', 'Honeysuckle', 'Hillside', 'Treetops', 'Woodside',
                   'The Old School House', 'Ivy House', 'Woodlands', 'Poets Corner', 'Red House',
                   'The White House', 'Wayside', 'The Granary', 'Lakeside', 'Stables', 'Toad Hall',
                   'Haven', 'The Vicarage', 'Fairview', 'The Fairway', 'The Laurels', 'Thornfield',
                   'Hillcrest', 'The Barn', 'Firs', 'Hawthorns', 'The Cottage', 'The Nook',
                   'The Coach House', 'Clarence House', 'Millpond', 'The Beeches', 'Highclere',
                   'The Gables', 'Caprica', 'Lakeview', 'Lake House']

    house_number = np.random.randint(*house_range)
    street_name = np.random.choice(street_names, size=1)[0]
    street_type = np.random.choice(street_types, size=1)[0]

    weights = [1, 1, 1, 9]
    weights = list(map(lambda x: x/sum(weights), weights))

    suffixes = list('abc ')
    flat_suffix = np.random.choice(suffixes, size=1, p=weights)[0]

    # house names generated based on 'threshold' house number
    if house_number > 325:
        house_name = np.random.choice(house_names, size=1)[0]
        street = f'{house_name}, {house_number}{flat_suffix.strip()} {street_name} {street_type}'
    # street names
    else:
        street = f'{house_number}{flat_suffix.strip()} {street_name} {street_type}'

    pcode = np.random.choice(zipcodes.post_code, size=1)[0]
    area = zipcodes.loc[zipcodes.post_code == pcode, 'area_covered']

    return {'street': street, 'area': area.values[0], 'pcode': pcode}


def get_dob(from_age:int=20, to_age:int=80, seed:Union[int, None]=None) -> pd.Timestamp:
    '''
    '''
    if seed:
        np.random.seed(seed)

    days = np.random.randint(from_age*365, to_age*365, 100)[0]
    dob = pd.to_datetime(datetime.now().date()) - pd.to_timedelta(days, 'D')

    return dob


def generate_customer(first_names:pd.DataFrame, surnames:pd.DataFrame, seed:Union[int, None]=None) -> Dict:
    '''
    Generate customer record

    <source data:: https://namecensus.com>

    Parameters
    ----------
    first_names: str,

    surnames: str,

    seed: int, default None - used for testing to deliver consistent results

    Returns
    -------
    dictionary
    '''
    if seed:
       np.random.seed(seed)

    # first name
    first_name = np.random.choice(first_names.Name.values, size=1)[0]
    male_salutations = ['Mr', 'Dr']
    female_salutations = ['Ms', 'Mrs', 'Dr']

    # Gender/salutation
    gender = first_names.loc[first_names['Name'] == first_name, 'Gender'].values[0]
    if gender == 'Male':
        weights =[9, 1]
        weights = list(map(lambda x: x/sum(weights), weights))
        salutation = np.random.choice(male_salutations, size=1, p=weights)[0]
    else:
        weights =[9, 1, 1]
        weights = list(map(lambda x: x/sum(weights), weights))
        salutation = np.random.choice(female_salutations, size=1, p=weights)[0]

    # Customer type
    if salutation == 'Dr':
        customer_types = ['Pharmacist', 'Consultant', 'Surgeon']
    else:
        customer_types = ['Outpatient', 'HomeCare', 'Hospital patient']

    customer_type = np.random.choice(customer_types, size=1)[0]

    # Middle initial
    a = np.random.random(size=27)
    a /= a.sum()
    alphabet = list('AEIOU '.upper())
    middle_initial = np.random.choice(alphabet, size=1, p=[.04,.04,.04,.04,.04,.8])[0]

    # Surname
    surname = np.random.choice(surnames.values, size=1)[0].title()

    #email address
    domains = ['hotmail.com', 'gmail.com', 'google.com', 'outlook.com', 'gmx.com',
               'yahoo.com', 'protonmail.com', 'icloud.com']
    domain = np.random.choice(domains, size=1)[0]

    add_email = np.random.choice([1, 0], size=1, p=[0.9, 0.1])[0]
    email = ''

    if add_email:
        delimitter = np.random.choice(['_', '.', ''], size=1, p=[.4, .4, .2])[0]
        email_type = np.random.choice(['use_initials', 'full_name'], size=1, p=[.2, .8])[0]
        if email_type == 'use_initials':
            email = first_name[0].lower() + delimitter + surname.lower() + '@' + domain
        else:
            email = first_name.lower() + delimitter + surname.lower() + '@' + domain

    customer = {'salutation': salutation, 'first_name': first_name, 'type': customer_type,
                'initial': middle_initial, 'surname': surname,
                'email': email, 'dob': get_dob(), 'status': generate_status()}

    return customer


def generate_customers(rows:int=50, data_directory:str='inputs/fake_data',
                     seed:Union[int, None]=None) -> pd.DataFrame:
    '''
    Generate customer rows/records data

    Parameters
    ----------
    rows: the number of returned rows/records

    data_directory: location of required postcodes, first names, surnames data

    seed: int, default None - used for testing to deliver consistent results

    Returns
    -------
    customers (DataFrame)
    '''
    if seed:
        np.random.seed(seed)

    directory   = Path(data_directory)
    postcodes   = get_sample_zipcodes(directory / 'zipcodes_uk.tsv')
    first_names = get_firstnames(directory / 'first_names.csv')
    surnames    = get_surnames(directory / 'surnames.csv')

    start_number = np.random.randint(48000000, 50000000)

    customers = []
    for idx in range(start_number, start_number+rows):
        customer = {'customer_no': idx}
        customer.update(generate_customer(first_names, surnames))
        customer.update(generate_address(postcodes))
        customers.append(customer)

    df_customers = pd.DataFrame(customers)

    return df_customers
