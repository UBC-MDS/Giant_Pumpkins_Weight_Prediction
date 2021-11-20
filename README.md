# Giant Pumpkins: weight prediction

-   **Authors:** Mahsa Sarafrazi, Rowan Sivanandam, Shiva Jena, and Vanessa Yuen

-   **Contributors:** Instructors, and Teaching Assistants of the course DSCI 522 of UBC Master of Data Science Vancouver program at the University of British Columbia, Vancouver

Analytical project prepared as part of the course DSCI 522 of the Master of Data Science 2021-22 program at University of British Columbia, Vancouver.

## About the project

This analytical project is an attempt at creating a machine learning linear regression model to predict a continuous variable, weight of giant pumpkins based on features such as type of pumpkin, place of cultivation (country, city, state province, GPC site), seed origins, pollinator father etc.

### Background on Giant Pumpkins and GPC

The data set used in this project is originally from BigPumpkins.com. The Great Pumpkin Commonwealth's (GPC) mission promotes the hobby of cultivating giant pumpkins throughout the world through standards and regulations to ensure quality of fruit, fairness of competition, recognition of achievement, fellowship and education for all participating growers and weigh-off sites. (Read more [here](https://gpc1.org/ "GPC website") and [here](http://www.bigpumpkins.com/ "Data on giant pumpkins from bigpumkins.com")).

### Raw data

The dataset is a public domain resource which pertains to the attributes of giant pumpkins grown in around 20 countries across the world in different regions. The raw data which was used in this project for the analysis can be found [here.](https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2021/2021-10-19/pumpkins.csv "Raw data")

### Predictive question and sub-questions

Given certain features of the seeds, place of cultivation, features of the parent pumpkin etc, what will be estimated weight of the giant pumpkin after harvesting?

To answer this predictive question, we need to first answer some underlying data related questions such as:

-   Is there a relationship between features of the seeds, place of cultivation etc and the weight of the pumpkins?

-   How are the weights distributed across regions?

## Method

The raw data comprises most of the features as character type where some of the features such as `id` contain important information like the pumpkin type. Therefore, in order to proceed, an initial data cleaning, preparation and pre-processing is required to make the features ready for training purposes. However, since the analysis is an attempt to answer a machine learning prediction problem, the dataset is first split into 70 % - 30 % sets of training and test sets respectively along with random seeding for reproducibility. Brief details of the tentative steps are mentioned below for an outline:

1.  **Train Test Split**  
    Splitting the dataset into train and test splits along with random seed for reproducibility will be the first step.

    The desired outputs are 70- 30 % splits of training and test data set respectively.

2.  **Exploratory Data Analysis (EDA):**

    Data cleaning and preparation is required for making features ready for the machine learning regression model. An analysis of the trends, correlation with actual pumpkin weights, . Both R and Python data wrangling tools such as tidyverse-deplyr, , numpy, pandas, and visualisation tools such as ggplot/ggplot2, Altair, Matplotlib are planned to be used.

    The desired outputs are processed data set in form of .csv file., RMD file/ Notebook for reproducible codes

3.  **Predictive Modelling**

    Linear Regression model is chosen since pumpkin weight is a continuous quantitative/ numerical variable. The model is planned to be trained and tested using Scikit Learn (sklearn) packages.

    There are few numerical features and more categorical features.For numerical features, SimpleImputer, StandardScaler is planned tentatively for transformations. For categorical features, One Hot Encoding, SimpleImputer for column transformations are planned.

    Using column transformers and pipe operators, cross-validation is planned to be performed for hyper-parameter optimization for sklearns LinearRegression model using GridSearchCV / RandomSearchCV.

    After optimising the hyperparameters, the model is to be fit on the training set and evaluation is to be done on the test set. For initial stages, accuracy and R-squared scores seem to be the metrics to asses

4.  **Report**

    Results of the analysis can be found [here](https://github.com/UBC-MDS/Giant_Pumpkins_Weight_Prediction/tree/a1eea45e1b158dd60859b46464fdf4cd987bc932/src) (folder link for WIP, report to be generated once analysis is completed).
