# author : Mahsa Sarafrazi
# date : 2021-11-19

""" Downloads a csv data file from a url and save it to local file path as csv format.

Usage: download_data.py --url=<url> --out_file=<out_file>

Options:
--url=<url>               the path in which the data is available  (must be in standard csv format)
--out_file=<out_file>      the path where to locally write the file
"""


import pandas as pd
import os
from docopt import docopt

opt = docopt(__doc__)

def main(url, out_file):
    
    pumpkins_df= pd.read_csv(url)

    try:
        pumpkins_df.to_csv(out_file, index = False)
    except:
        os.makedirs(os.path.dirname(out_file))
        pumpkins_df.to_csv(out_file, index = False)

if __name__ == "__main__":
    main(opt['--url'],opt['--out_file'])
