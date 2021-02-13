import pytest
from fake.sku import *
from pathlib import Path


directory = Path('./inputs/fake_data')


def test_generate_status():
    '''
    '''
    expected = 'D'
    actual = generate_status(choices=['A', 'D'], weights=[0, 10], seed=42)

    assert expected == actual


def test_generate_sku():
    '''
    '''
    expected = '2O-HU-6266'
    actual = generate_sku(sections=2, chars_per_section=2, delimitter='-', seed=42)

    assert expected == actual


def test_generate_uom():
    '''
    '''
    expected = 'EA'
    actual = generate_uom(seed=42)

    assert expected == actual


def test_generate_pack_factor():
    '''
    '''
    expected = 12
    actual = generate_packfactor(weights=[0, 1, 0, 0], seed=42)

    assert expected == actual


def test_generate_price():
    '''
    '''
    expected = 8.1163
    actual = generate_price(lower=1, upper=20, precision=4, seed=42)

    assert expected == actual


def test_generate_skus():
    '''
    '''
    expected = (1211, 7)
    actual = generate_skus(directory / 'sku_names.csv').shape

    assert expected == actual

