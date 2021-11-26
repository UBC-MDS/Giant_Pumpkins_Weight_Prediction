# author: Mahsa Sarafrazi, Rowan Sivanandam, Shiva Jena, and Vanessa Yuen
# date: 2021-11-24

"""This script performs data tidying, preprocessing, transformation and splitting of the giant pumpkin raw data
Usage: preprocclean_split_train_test.py --file=<file> --out_dir=<out_dir>

Options:
--file=<file>               the path of the raw data file  (must be in standard csv format)
--out_dir=<out_dir>         the path of the directory where the processed data will be saved 

""" 

import os
from pathlib import Path
import pandas as pd
from sklearn.model_selection import train_test_split
from docopt import docopt

opt = docopt(__doc__)

def main(file, out_dir):

    temp_file = "temp.csv"

    # read raw csv data with numeric values
    pumpkins_df= pd.read_csv(file)

    # skip separator rows between groups of same id (format: place column with the string "N Entries")
    pumpkins_df = pumpkins_df[-pumpkins_df["place"].str.contains("Entries")]

    # create temp file with separator rows removed and call read_csv again to get numeric fields
    pumpkins_df.to_csv(temp_file, index=False)
    pumpkins_df = pd.read_csv(temp_file, thousands=",")
    os.remove(temp_file)

    
    # split column 'id' to 'year' and 'type' columns
    year_type_df = pumpkins_df["id"].str.split("-", expand=True)
    year_type_df.columns = ["year", "type"]

      
    # merge new columns with original columns
    pumpkins_df_processed = pd.concat([pumpkins_df, year_type_df], axis=1)

    # filter with giant pumpkins data only (type=P)
    pumpkins_df_processed = pumpkins_df_processed.query("type=='P'")

    # remove drop features and 'id' which are split into new columns
    # drop features: 'est_weight', 'pct_chart', 'variety', 'seed_mother', 'pollinator_father', 'grower_name'
    pumpkins_df_processed = pumpkins_df_processed.drop(
        columns=[
            "id",
            "place",
            "grower_name",
            "seed_mother",
            "pollinator_father",
            "variety",
            "est_weight",
            "pct_chart",
        ]
    )
    # reorder columns - move weight_lbs to last column (target)
    cols = pumpkins_df_processed.columns.tolist()
    cols = cols[1:] + cols[0:1]
    pumpkins_df_processed = pumpkins_df_processed[cols]

    # Split train and test data
    train_df, test_df = train_test_split(
        pumpkins_df_processed, test_size=0.3, random_state=123
    )

    # Write train data and test data to file
    Path(out_dir).mkdir(parents=True, exist_ok=True)

    train_df.to_csv(out_dir + "/pumpkins_train.csv", index = False)
    test_df.to_csv(out_dir + "/pumpkins_test.csv", index = False)


if __name__ == "__main__":
    main(opt['--file'],opt['--out_dir'])