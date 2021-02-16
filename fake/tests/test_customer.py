import pytest
from fake.customer import *
from pandas import Timestamp
from pathlib import Path


directory = Path('./inputs/fake_data')

@pytest.fixture
def get_first_names():
    return get_firstnames(directory / 'first_names.csv')


@pytest.fixture
def get_last_names():
    return get_surnames(directory / 'surnames.csv')


@pytest.fixture
def get_zip_codes():
    return get_sample_zipcodes(directory / 'zipcodes_uk.tsv', seed=42)


def test_zipcodes():
    '''
    '''
    filename = directory / 'zipcodes_uk.tsv'

    expected = (1000, 3)
    actual = get_sample_zipcodes(filename, seed=42).shape

    assert expected == actual


def test_firstnames():
    '''
    '''
    filename = directory / 'first_names.csv'

    expected = (1002, 2)
    actual = get_firstnames(filename).shape

    assert expected == actual


def test_surnames():
    '''
    '''
    filename = directory / 'surnames.csv'

    expected = (1000,)
    actual = get_surnames(filename).shape

    assert expected == actual


def test_generate_customer(get_first_names, get_last_names):
    '''
    '''
    first_names = get_first_names
    surnames = get_last_names

    expected = {'salutation': 'Ms', 'first_name': 'Evelyn',
                'type': 'Hospital patient', 'initial': 'E',
                'surname': 'Bray', 'email': 'evelyn_bray@protonmail.com',
                'dob': Timestamp('1972-03-29 00:00:00'), 'status': 1}

    actual = generate_customer(first_names, surnames, seed=42)

    assert expected == actual


def test_generate_address(get_zip_codes):
    '''
    '''
    zip_codes = get_zip_codes

    expected = {'area': 'Portsmouth', 'pcode':'PO22 7TB',
                'street': '103 Charles Approach'}

    actual = generate_address(zip_codes, seed=42)

    assert expected == actual
