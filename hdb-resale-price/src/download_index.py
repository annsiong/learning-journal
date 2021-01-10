import click
import json
import logging
import os
import pandas as pd
import requests

def download_hdb_index(download_dir):
    """ 
    Download HDB quarterly price index to /data/raw
    """
    logger = logging.getLogger(__name__)

    logger.info('requesting data...')
    url = 'https://data.gov.sg/api/action/datastore_search?resource_id=52e93430-01b7-4de0-80df-bc83d0afed40&limit=200'
    response = requests.get(url)
    response_data = json.loads(response.content)
    response_data = pd.DataFrame(response_data['result']['records']).set_index('_id')

    logger.info('saving data...')
    download_path = os.path.join(download_dir, 'hdb_index.csv')
    response_data.to_csv(download_path)

def download_other_index(download_dir):
    pass

@click.command()
@click.argument('name')
def main(name):
    from config import RAW_DIR, LoggingConfig
    LoggingConfig()
    if name == 'hdb':
        download_hdb_index(RAW_DIR)

if __name__ == '__main__':
    main()