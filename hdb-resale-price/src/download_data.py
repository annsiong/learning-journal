import click
import glob
import json
import logging
import os
import pandas as pd
import requests
import zipfile

def download_hdb_resale_price(downloaded_dir, temp_dir):
    """ 
    Download HDB resale prices from data.gov.sg
    """
    logger = logging.getLogger(__name__)

    logger.info('downloading zip file...')
    temp_path = os.path.join(temp_dir, 'hdb_resale_prices.zip')
    url = 'https://data.gov.sg/dataset/7a339d20-3c57-4b11-a695-9348adfd7614/download'
    response = requests.get(url)
    open(temp_path, 'wb').write(response.content)

    logger.info('extracting contents...')
    with zipfile.ZipFile(temp_path, 'r') as zip_ref:
        zip_ref.extractall(temp_dir)

    logger.info('importing all csvs...')
    temp_csvs = os.path.join(temp_dir, '*.csv')
    files = glob.glob(temp_csvs)
    data = [pd.read_csv(f) for f in files]
    data = pd.concat(data)

    logger.info('saving combined data...')
    downloaded_path = os.path.join(downloaded_dir, 'hdb_resale_price.csv')
    data.to_csv(downloaded_path, index=False)

@click.command()
@click.argument('name')
def main(name):
    from config import RAW_DIR, TEMP_DIR, LoggingConfig
    LoggingConfig()
    if name == 'hdb':
        download_hdb_resale_price(RAW_DIR, TEMP_DIR)

if __name__ == '__main__':
    main()