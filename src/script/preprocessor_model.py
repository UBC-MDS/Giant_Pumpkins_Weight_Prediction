# author: Mahsa Sarafrazi, Rowan Sivanandam, Shiva Jena, and Vanessa Yuen
# date: 2021-11-24

"""This script performs fit and tuning of the machine learning model with the processed data
Usage: fit_predict.py --file=<file> --out_dir=<out_dir>

Options:
--file<file>            the path and filename of the train data set  (must be in standard csv format)
--out_dir=<out_dir>     the path of where the output eda figures will be saved
"""

import os
from docopt import docopt
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


def main(file, out_dir):

    pumpkins_df = pd.read_csv(file)

    # split features and target X_train, y_train
    X_train = pumpkins_df.drop(columns=["weight_lbs"])
    y_train = pumpkins_df["weight_lbs"]

    # Create Column Transformer for data transformation
    categorical_features = ["country", "city", "state_prov", "gpc_site"]
    numeric_features = ["ott", "year"]

    # Use different SimpleImputer for city (constant="missing") and ott (strategy="mean)
    # numerical transformer
    numeric_transformer = make_pipeline(
        # SimpleImputer(strategy="mean"), StandardScaler())
        SimpleImputer(strategy="median"), StandardScaler())

    # categorical transformer
    categorical_transformer = make_pipeline(
        SimpleImputer(strategy="constant", fill_value="missing"),
        OneHotEncoder(handle_unknown="ignore", sparse=False),
    )

    preprocessor = make_column_transformer(
        (numeric_transformer, numeric_features),
        (categorical_transformer, categorical_features),
    )
    preprocessor.fit_transform(X_train, y_train)
    

    # Tune hyperparameter alpha with GridSearchCV
    param_grid = {"ridge__alpha": 10.0 ** np.arange(-3, 3, 1)}
    pipe_ridge = make_pipeline(preprocessor, Ridge())

    search = GridSearchCV(
        pipe_ridge,
        param_grid,
        n_jobs=-1,
        return_train_score=True,
    )
    search.fit(X_train, y_train)
    train_scores = search.cv_results_["mean_train_score"]
    cv_scores = search.cv_results_["mean_test_score"]

    # Plot tuning result
    plt.semilogx(param_grid["ridge__alpha"],
                 train_scores.tolist(), label="train")
    plt.semilogx(param_grid["ridge__alpha"], cv_scores.tolist(), label="cv")
    plt.legend()
    plt.xlabel("alpha")
    plt.ylabel("score")

    # save result to png
    Path(out_dir).mkdir(parents=True, exist_ok=True)

    plt.savefig(out_dir+"/tuning_ridge.png")

    # Report CV score
    best_alpha = search.best_params_
    best_score = search.best_score_

    # print("The best alpha value is " + str(best_alpha))
    # print("The best CV score is " + str(best_score))
    print(str(best_alpha.get("ridge__alpha")) + " " + str(best_score))
    
    # Coefficients of features estimated by model
    # 1. Extracting categorical features 
    ohe_columns = list(
    preprocessor.named_transformers_["pipeline-2"]
      .named_steps["onehotencoder"]
      .get_feature_names_out(categorical_features)
    )
    
    # 2. Creating columns in sequence same as preprocessor
    new_columns = (
        numeric_features + ohe_columns
    )
    
    # 3. Creating pipeline and fitting tuned model on Training data
    pipe_bestalpha = make_pipeline(
        preprocessor, 
        Ridge(alpha=best_alpha["ridge__alpha"]
      )
    )
    pipe_bestalpha.fit(X_train, y_train)
    
    # 4. Extracting all coefficients
    bestalpha_coeffs = pipe_bestalpha.named_steps["ridge"].coef_
    coefficients_results = pd.DataFrame(
        data=bestalpha_coeffs, 
        index=new_columns, 
        columns=["Coefficients"]
    )
    
    # 5. Top 5 Numeric features coefficients
    numeric_coefficients = coefficients_results[
      :len(numeric_features)
    ].sort_values(
      by="Coefficients", 
      ascending=False
    ).round(2)
    
    # 6. Top 5 Categorical features with positive and negative coefficients
    top_five_positive = coefficients_results[
      len(numeric_features):
        ].sort_values(
          by="Coefficients", 
          ascending=False
    ).round(2).head(5)
    
    top_five_negative = coefficients_results[
      len(numeric_features):
        ].sort_values(
          by="Coefficients"
    ).round(2).head(5)
    categorical_coefficients = pd.concat(
      [top_five_positive,top_five_negative]
    )


    with open(out_dir+"/model.pickle", "wb") as f:
        pickle.dump(search, f, pickle.HIGHEST_PROTOCOL)

    # Saving results and coefficients
    save_results(out_dir+"/cvresults.csv", best_alpha, best_score)
    save_coefficients(out_dir+"/coefficients_numeric.csv", numeric_coefficients)
    save_coefficients(out_dir+"/coefficients_categorical.csv", categorical_coefficients)

def save_results(filename, best_alpha, best_score):
    """
    Save the cross validation result to a csv file,
    in the form for "best alpha,best_score"
    """
    with open(filename, 'w') as output:
        output.write("best_alpha,best_score\n")
        output.write(str(best_alpha.get("ridge__alpha")))
        output.write(",")
        output.write(str(best_score))
    output.close()

def save_coefficients(filename, coefficient):
    """
    Save the features with highest magnitudes of coefficients to a csv file
    """
    # with open(filename, 'w') as output:
    #     output.write(coefficient)
    # output.close()

if __name__ == "__main__":
    main(opt['--file'], opt['--out_dir'])
