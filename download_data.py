# author : Mahsa Sarafrazi
# date : 2021-11-19

""" Downloads a csv data file from a url and save it to local file path as csv format.

Usage: download_data.py --url=<url> --out_file=<out_file>

Options:
--url =<url>               the path in which the data is available  (must be in standard csv format)
--out_file=<out_file>      the path where to localy write the file
"""

import pandas as pd
import os
from docopt import docopt

opt = docopt(__doc__)

def main(url, out_file):
    
    data = pd.read_csv(url,skiprows= [292, 496, 2178, 2330, 2620, 2894, 3225, 3411, 5312, 5505, 5800, 6073, 6393, 6613, 8594, 8801, 9116, 9392, 9727, 9984, 11783, 11990, 12317, 12610, 12939, 13140, 14883, 15111, 15476, 15755, 16072, 16292, 18198, 18378, 18745, 19060, 19361, 19616, 21500, 21698, 22150, 22441, 22688, 22915, 24485, 24645, 25029, 25301, 25585, 25780, 27279, 27440, 27811, 28065])
    
    try:
        data.to_csv(out_file, index = False)
    except:
         os.makedirs(os.path.dirname(out_file))
         data.to_csv(out_file, index = False)

if __name__ == "__main__":
    main(opt['--url'],opt['--out_file'])
