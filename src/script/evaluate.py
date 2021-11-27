# author: Mahsa Sarafrazi, Rowan Sivanandam, Shiva Jena, and Vanessa Yuen
# date: 2021-11-24

"""This script evaluates the machine learning model with the test data
Usage: evaluate.py --file=<file> --object_file=<object_file> --out_dir=<out_dir>

Options:
--file=<file>               the path and filename of the test data set  (must be in standard csv format)
-object_file=<object_file>  the path of the model object trained
--out_dir=<out_dir>         the path of where the results will be saved

"""

import os
from docopt import docopt
import altair as alt
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pickle
from sklearn import set_config
from sklearn.compose import ColumnTransformer, make_column_transformer
from sklearn.dummy import DummyRegressor
from sklearn.impute import SimpleImputer
from sklearn.linear_model import Ridge, RidgeCV
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV, cross_validate
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

opt = docopt(__doc__)


def main(file, object_file, out_dir):

    pumpkins_test_df = pd.read_csv(file)

    # split features and target X_test, y_test
    X_test = pumpkins_test_df.drop(columns=["weight_lbs"])
    y_test = pumpkins_test_df["weight_lbs"]

    # load the tuned model
    with open(object_file, "rb") as f:
        model = pickle.load(f)

    predict_y = model.predict(X_test)
    score = model.score(X_test, y_test)

    out_df = pd.DataFrame({"actual_weight_lbs": y_test,
                          "predicted_weight_lbs": predict_y})

    # plot an actual/prediction graph
    prediction = (
        alt.Chart(out_df, title="Predicted weight vs Actual weight")
        .mark_point(opacity=0.5)
        .encode(x=alt.X("actual_weight_lbs", title="Actual Weight (lbs)"),
                y=alt.Y("predicted_weight_lbs", title="Predicted Weight (lbs)")
                )
    )
    dummy_df = pd.DataFrame(
        {
            "actual_weight_lbs": [0, 3500],
            "predicted_weight_lbs": [0, 3500],
        }
    )

    line_plot = prediction.mark_line(color="red").encode(
        x="actual_weight_lbs",
        y="actual_weight_lbs",
    )

    compiled = (prediction + line_plot)

    # save the prediction result in output folder
    Path(out_dir).mkdir(parents=True, exist_ok=True)
    out_df.to_csv(out_dir + "/test_result.csv", index=False)
    compiled.save(out_dir+"/predict_result.png")

    # Report score
    print(score)
    #print("The testing score is " + str(score))


if __name__ == "__main__":
    # main(opt['--file'],opt['--out_dir'])
    main(opt['--file'], opt['--object_file'], opt['--out_dir'])
