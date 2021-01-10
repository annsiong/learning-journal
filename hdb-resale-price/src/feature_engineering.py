import pandas as pd

def transform_quarter(datetime_obj):
    '''
    Convert date to YYYY-QQ format
    :param datetime_obj: pandas series
    :return: yyyyqq: pandas series
    '''
    year = datetime_obj.dt.year 
    quarter = datetime_obj.dt.quarter 
    yyyyqq = year.astype(str) + '-Q' + quarter.astype(str)
    return yyyyqq

def transform_storey_range(storey_range):
    '''
    Standardize original storey_range column
    :param storey_range: pandas series
    :return: new_storey_range: pandas series
    '''
    storey_lb = pd.to_numeric(storey_range.apply(lambda x: x[:2]))
    storey_ub = pd.to_numeric(storey_range.apply(lambda x: x[-2:]))
    new_storey_range = storey_range.copy()
    new_storey_range[(storey_ub <= 15)] = '01 TO 15'
    new_storey_range[(storey_lb > 15) & (storey_ub <= 30)] = '16 TO 30' 
    new_storey_range[(storey_lb > 30)] = '>30'
    return new_storey_range