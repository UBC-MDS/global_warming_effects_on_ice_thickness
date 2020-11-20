# author: Jayme Gordon
# date: 2020-11-19

"""This script downloads the ice thickness data set to /data dir
Usage:
    data_import.py

Options:

"""

import pandas as pd
from docopt import docopt
from pathlib import Path
import logging

# init logging
fmt_stream = logging.Formatter('%(levelname)-7s %(lineno)-4d %(name)-10s %(message)s')
sh = logging.StreamHandler()
sh.setLevel(logging.INFO)
sh.setFormatter(fmt_stream)
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)
log.addHandler(sh)

# opt = docopt(__doc__)

p_data = Path(__file__).parents[1] / 'data/ice_thickness.csv' # set download location

def download_data() -> None:
    """Download ice thickness data from url, write to csv in /data dir
    """    
    url = 'https://www.canada.ca/content/dam/eccc/migration/main/data/ice/products/ice-thickness-program-collection/ice-thickness-program-collection-1947-2002/original_program_data_20030304.xls'

    if p_data.exists():
        ans = _input(msg='Data file already exists, overwrite?')
        if not ans:
            log.info('User declined to overwrite.')
            return
        else:
            log.info('Overwriting data.')

    df = pd.read_excel(url, header=1)
    df.to_csv(p_data, index=False)

    log.info(f'Successfully downloaded data file with [{len(df)}] rows to "{p_data}"')

def load_data() -> pd.DataFrame:
    """Load data from download location to DataFrame

    Returns
    -------
    pd.DataFrame
        Dataframe containing ice thickness records
    """
    if not p_data.exists():
        log.warning(f'data file does not exist at: {p_data}')
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

if __name__ == '__main__':
    download_data()