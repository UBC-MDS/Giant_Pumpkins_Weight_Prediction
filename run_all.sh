# author: Mahsa Sarafrazi, Rowan Sivanandam, Shiva Jena, and Vanessa Yuen
# date: 2021-11-24

# This script runs the Giant Pumpkin weight prediction model, creates output and generates the analysis report

#uncomment and run the below line if image file can't be generated in eda.py and evaluate.py
#npm install -g vega vega-cli vega-lite canvas

# Download raw data
python src/script/download_data.py --url="https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2021/2021-10-19/pumpkins.csv" --out_file="data/raw/pumpkins.csv"

# Clean data and split the data into train/test set
python src/script/clean_split_train_test.py --file="data/raw/pumpkins.csv" --out_dir="data/processed"

# Perform exploratory data anlysis
python src/script/eda.py --file="data/processed/pumpkins_train.csv" --out_dir="doc/result"

# Perform data preprocessing and tune regression model
cv_result=$(python src/script/preprocessor_model.py --file="data/processed/pumpkins_train.csv" --out_dir="doc/result")
IFS=' '
read -a arr <<< "$cv_result"
best_alpha=${arr[0]}
best_score_cv=${arr[1]}

# Evalate the model with test result
test_score=$(python src/script/evaluate.py --file='data/processed/pumpkins_test.csv' --object_file='doc/result/model.pickle' --out_dir='doc/result')


# Render final report
Rscript -e "rmarkdown::render('doc/pumpkin.Rmd', params = list(best_alpha=$best_alpha, best_score_cv=$best_score_cv, test_score=$test_score))"

