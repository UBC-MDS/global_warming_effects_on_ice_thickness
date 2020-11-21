# author: Group 13
# date: 2020-11-19

"""Entry point script to download a Canadian ice thickness data set

Usage:
    download.py [--url=<url>] [--save_dir=<save_dir>]

Options:
    [--url=<url>]             Optionalal url, fallback to default
    [--save_dir=<save_dir>]   Optional save_dir, must be a directory NOT filename, fallback to default
"""

from docopt import docopt
from src.import_data import download_data

if __name__ == '__main__':
    opt = docopt(__doc__)
    
    download_data(
        url=opt.get('--url', None),
        save_dir=opt.get('--save_dir', None))