# author: Mahsa Sarafrazi, Rowan Sivanandam, Shiva Jena, and Vanessa Yuen
# date: 2021-11-24

"""This script performs exploratory data analysis on the processed data
Usage: eda.py --file=<file> --out_dir=<out_dir>

Options:
--file=<file>              the path and filename of the train data set  (must be in standard csv format)
--out_dir=<out_dir>       the path of where the output eda figures will be saved

""" 

import pandas as pd
import os
import altair as alt
from pathlib import Path

alt.data_transformers.enable("data_server")
alt.renderers.enable("mimetype")

from docopt import docopt

opt = docopt(__doc__)

def main(file, out_dir):

    train_df= pd.read_csv(file)

    # weight distribution
    weight_dist_plot = (
    alt.Chart(train_df)
    .mark_bar()
    .encode(
        alt.X("weight_lbs", bin=alt.Bin(maxbins=20)),
        y="count()",
    )
    .properties(width=300, height=200)
    )

    # ott distribution
    ott_dist_plot = (
    alt.Chart(train_df)
    .mark_bar()
    .encode(
        alt.X("ott", bin=alt.Bin(maxbins=20)),
        y="count()",
    )
    .properties(width=300, height=200)
    )

    # country distribution
    country_dist_plot = (
    alt.Chart(train_df)
    .mark_bar()
    .encode(x="count()", y=alt.Y("country"))
    .properties(width=300, height=200)
    )
    
    # state, city, gpc_site distributions
    state_dist = (
    alt.Chart(train_df, title="Distribution of State/Province")
    .mark_bar()
    .encode(y="count()", x=alt.X("state_prov", axis=None))
    .properties(width=300, height=200)
    )

    gpc_dist = (
    alt.Chart(train_df, title="Distribution of GPC Site")
    .mark_bar()
    .encode(y="count()", x=alt.X("gpc_site", axis=None))
    .properties(width=300, height=200)
    )
    city_dist = (
    alt.Chart(train_df, title="Distribution of city")
    .mark_point(opacity=0.5, clip=True)
    .encode(
        y=alt.Y("count()", scale=alt.Scale(domain=(0, 100))), x=alt.X("city", axis=None)
    )
    .properties(width=300, height=200)
    )

    dist_compile = alt.vconcat(alt.hconcat(weight_dist_plot, ott_dist_plot, country_dist_plot), alt.hconcat(state_dist, city_dist, gpc_dist))

    # avg weight vs OTT
    ott = (
        alt.Chart(train_df, title="Mean Weight Vs OTT")
        .mark_point()
        .encode(x="ott", y="mean(weight_lbs)")
        .properties(width=500, height=200)
    )


    # avg weight by country
    country = (
        alt.Chart(train_df, title="Mean Weight Vs Country")
        .mark_point(opacity=0.5, clip=True)
        .encode(
            y=alt.Y("mean(weight_lbs)", scale=alt.Scale(domain=(0, 2500))),
            x=alt.X("country", sort="y"),
        )
        .properties(width=300, height=200)
    )


    # avg weight by city
    city = (
        alt.Chart(train_df, title="Mean Weight Vs City")
        .mark_point(opacity=0.5, clip=True)
        .encode(
            y=alt.Y("mean(weight_lbs)", scale=alt.Scale(domain=(0, 2500))),
            x=alt.X("city", axis=None, sort="y"),
        )
        .properties(width=300, height=200)
    )

    # avg weight by state/provience
    state = (
        alt.Chart(train_df, title="Mean Weight Vs State/Prov")
        .mark_point(opacity=0.5, clip=True)
        .encode(
            y=alt.Y("mean(weight_lbs)", scale=alt.Scale(domain=(0, 2500))),
            x=alt.X("state_prov", axis=None, sort="y"),
        )
        .properties(width=300, height=200)
    )
    # avg weight by gpc_site
    gpc_site = (
        alt.Chart(train_df, title="Mean Weight Vs GPC Site")
        .mark_point(opacity=0.5, clip=True)
        .encode(
            y=alt.Y("mean(weight_lbs)", scale=alt.Scale(domain=(0, 2500))),
            x=alt.X("gpc_site", axis=None, sort="y"),
        )
        .properties(width=300, height=200)
    )


    compiled = alt.vconcat(
        alt.hconcat(ott), alt.hconcat(country, city), alt.hconcat(state, gpc_site)
    )

    Path(out_dir).mkdir(parents=True, exist_ok=True)
    dist_compile.save(out_dir+"/eda_distribution.png")
    compiled.save(out_dir+"/eda_relationship.png")


    

if __name__ == "__main__":
    main(opt['--file'],opt['--out_dir'])