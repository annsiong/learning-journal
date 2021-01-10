import logging
import numpy as np
import pandas as pd
import pytest
import sys

sys.path.append('.')
from src.feature_engineering import *

def test_transform_quarter():
    given = pd.to_datetime(pd.Series(['2020-11', '2010-04', '2016-09', '2017-03']))
    expected = pd.Series(['2020-Q4', '2010-Q2', '2016-Q3', '2017-Q1'])
    assert (transform_quarter(given) == expected).all()

def test_transform_storey_range():
    given = pd.Series(['13 TO 15', '16 TO 18', '26 TO 30', '31 TO 35'])
    expected = pd.Series(['01 TO 15', '16 TO 30', '16 TO 30', '>30'])
    assert (transform_storey_range(given) == expected).all()