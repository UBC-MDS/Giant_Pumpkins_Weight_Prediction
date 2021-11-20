# author : Mahsa Sarafrazi
# date : 2021-11-19

# Downloads a csv data from https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2021/2021-10-19/pumpkins.csv
# and save it to data/pumpkins_data.csv


import pandas as pd
import os

def main():
    url = "https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2021/2021-10-19/pumpkins.csv"
    out_file = "data/pumpkins_data.csv"
    data = pd.read_csv(url)
    try:
        data.to_csv(out_file, index = False)
    except:
         os.makedirs(os.path.dirname(out_file))
         data.to_csv(out_file, index = False)

if __name__ == "__main__":
    main()
