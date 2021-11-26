# Giant Pumpkins: weight prediction

-   **Authors:** Mahsa Sarafrazi, Rowan Sivanandam, Shiva Jena, and Vanessa Yuen

-   **Contributors:** Instructors, and Teaching Assistants of the course DSCI 522 of UBC Master of Data Science Vancouver program at the University of British Columbia, Vancouver

Analytical project prepared as part of the course DSCI 522 of the Master of Data Science 2021-22 program at University of British Columbia, Vancouver.

## About the project

This analytical project is an attempt at creating a machine learning linear regression model to predict a continuous variable, weight of giant pumpkins based on features such as type of pumpkin, place of cultivation (country, city, state province, GPC site), seed origins, pollinator father, etc.

### Background on Giant Pumpkins and GPC

The data set used in this project is originally from BigPumpkins.com. The Great Pumpkin Commonwealth's (GPC) mission promotes the hobby of cultivating giant pumpkins throughout the world through standards and regulations to ensure quality of fruit, fairness of competition, recognition of achievement, fellowship and education for all participating growers and weigh-off sites. (Read more [here](https://gpc1.org/ "GPC website") and [here](http://www.bigpumpkins.com/ "Data on giant pumpkins from bigpumkins.com")).

### Raw data

The dataset is a public domain resource which pertains to the attributes of giant pumpkins grown in around 20 countries across the world in different regions. The raw data which was used in this project for the analysis can be found [here.](https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2021/2021-10-19/pumpkins.csv "Raw data")

### Predictive question and sub-questions

Given certain features of the seeds, place of cultivation, features of the parent pumpkin etc, what will be estimated weight of the giant pumpkin after harvesting?

To answer this predictive question, we need to first answer some underlying data related questions such as:

-   Is there a relationship between features of the seeds, place of cultivation, and the weight of the pumpkins?

-   How are the weights distributed across regions?

## Method

The majority of the raw data comprises of features of the character type where some of the features such as `id` contain important information such as the pumpkin type. Therefore, in order to proceed, an initial data cleaning, preparation and pre-processing is required to make the features ready for training purposes. However, since the analysis is an attempt to answer a machine learning prediction problem, the dataset is first split into a 70/30 split for the training and test sets respectively along with random seeding for reproducibility. Brief details of the steps are mentioned below for an outline:

1.  **Train Test Split**  
    Splitting the dataset into train and test splits along with random seed for reproducibility.

    The desired outputs are a 70/30 split of training and test data.

2.  **Exploratory Data Analysis (EDA):**

    Data cleaning and preparation is required for making features ready for the machine learning regression model. An analysis of the trends and correlation with actual pumpkin weights and various features will be used. Both R and Python data wrangling tools such as tidyverse-deplyr, numpy, pandas, and visualisation tools such as ggplot/ggplot2, Altair, Matplotlib are planned to be used.

    On initial observations, the data seems to be mostly from the US. The distribution of the GPC sites, city and state/province are more evenly distributed. We consider these columns as good features to be used. Plots of the mean weight of giant pumpkins against different features (ott, country, city, state, gpc site) also suggest these features relates to the target (weight).

    The desired outputs are processed data sets in form of .csv files and RMD files/Notebooks for reproducible codes.

    The initial EDA can be viewed and explored [here](/src/eda/pumpkin_eda.pdf).

3.  **Predictive Modelling**

    The Ridge Linear Regression model will be used as pumpkin weight is a continuous, quantitative, numerical variable. The model is planned to be trained and tested using Scikit Learn (sklearn) packages.

    There are few numerical features and more categorical features. For numerical features, SimpleImputer and StandardScaler will be used during the preprocessing stage where as for categorical features, One-Hot Encoding and SimpleImputer for will ready the data
    for analysis.

    Using column transformers and pipe operators, cross-validation will be performed for hyperparameter optimization of sklearn's LinearRegression model using GridSearchCV.

    After optimising the hyperparameters, the model will be fit on the training set and evaluation to be done on the test set. In the initial stages, the R-squared score will be the underlying metrics used to assess our model.

## Report

Results of the analysis can be found [here](/doc) .

## Usage

For replicating the analysis and usage, clone this GitHub repository and download the data by running the commands provided below at terminal/command line from the root directory of this project folder (".../Giant_Pumpkins_Weight_Prediction/"):

    python src/data/data_download.py --url="https://github.com/UBC-MDS/Giant_Pumpkins_Weight_Prediction" --outputfile="data/raw/pumpkins.data"

## Dependencies

The dependencies for this project can be found in `environment.yaml` located [here](https://raw.githubusercontent.com/UBC-MDS/Giant_Pumpkins_Weight_Prediction/main/environment.yaml). The yaml file needs to be run to create the environment required for running the analysis. If conda is installed, the following command can be run at the terminal/ command line from the root directory of this project folder (".../Giant_Pumpkins_Weight_Prediction/") to install the dependencies:

    conda env create -f environment.yaml

## References
