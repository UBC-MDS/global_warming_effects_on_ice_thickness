# author: Jayme Gordon, Sasha Babicki
# date: 2020-11-26

"""Download data from the web to save locally as csv and provide functions for reading locally.

Usage: src/import_data.py [--url=<url>] [--output_path=<output_path>]

Options:
[--url=<url>]            Optional: The url of the data to save
[--output_path=<output_path>]  Optional: The local path of where to save the downloaded data
"""

import logging
import os
from pathlib import Path

import pandas as pd
from docopt import docopt

from __init__ import getlog

opt = docopt(__doc__)
log = getlog(__file__)

# set default download dir and url
file_name = 'ice_thickness.csv'
save_dir_default = Path(__file__).parents[1] / f'data/raw/{file_name}'
url_default = 'https://www.canada.ca/content/dam/eccc/migration/main/data/ice/products/ice-thickness-program-collection/ice-thickness-program-collection-1947-2002/original_program_data_20030304.xls'

def download_data(url : str = None, save_dir : str = None) -> None:
    """Download ice thickness data from url, write to csv in /data dir

    Parameters
    ----------
    url : str, optional
        url to download data for analysis, default None
    save_dir : str, optional
        filepath to save data, default None
    """    
    if url is None:
        url = url_default
        log.info('No url provided, using default.')
    
    # use default, or convert save_dir string to Path obj
    if save_dir is None:
        p_data = save_dir_default
        log.info('No save dir provided, using default.')
    else:
        # check user input save dir is valid directory
        p_dir = Path(save_dir)
        if not p_dir.suffix == '':
            log.error(f'save_dir must be a directory.')
            return

        p_data = p_dir / f'{file_name}'
        
        # ask to create directory
        if not p_dir.exists():
            # ans = _input(msg=f'save_dir "{p_dir}" does not exist, create now?')
            # if not ans:
            #     log.info('User declined to create save_dir.')
            #     return
            # else:
            log.info(f'Creating save_dir at {p_dir}')
            p_dir.mkdir(parents=True)

    # ask if okay to overwrite
    if p_data.exists():
        ans = _input(msg='Data file already exists, overwrite?')
        if not ans:
            log.info('User declined to overwrite.')
            return
        else:
            log.info('Overwriting data.')

    log.info(f'Downloading data file from: {url}')

    try: 
        df = pd.read_excel(url, header=1)
        df.to_csv(p_data, index=False)
    except:
        log.info('Problem reading file. Please try again.')
        return

    log.info(f'Successfully downloaded data file with [{len(df)}] rows to "{p_data}"')

    return p_data

def load_data() -> pd.DataFrame:
    """Load data from download location to DataFrame

    Returns
    -------
    pd.DataFrame
        Dataframe containing ice thickness records
    """
    p_data = save_dir_default

    if not p_data.exists():
        log.warning(f'Data file does not exist at: {p_data}')
        return

    return pd.read_csv(p_data)

def _input(msg : str) -> bool:
    """Get yes/no answer from user in terminal

    Parameters
    ----------
    msg : str
        Prompt to ask user

    Returns
    -------
    bool
        User's answer y/n, True/False
    """    
    reply = str(input(msg + ' (y/n): ')).lower().strip()
    if len(reply) <= 0:
        return False

    if reply[0] == 'y':
        return True
    elif reply[0] == 'n':
        return False
    else:
        return False
    
def read_file(file_name : str) -> pd.DataFrame:
    """Load data based on file name, download and save if file doesn't exist

    Parameters
    ----------
    file_name : str
        The local path (including filename) of the csv file
        
    Returns
    -------
    pd.DataFrame
        Dataframe containing ice thickness records
    """
    try: 
        df = pd.read_csv(file_name)
    
    # if file does not exist or cannot be read, download from default url
    except: 
        df = download_data()
        
    return df

if __name__ == "__main__":
    download_data(
        url=opt["--url"],
        save_dir=opt["--output_path"])
