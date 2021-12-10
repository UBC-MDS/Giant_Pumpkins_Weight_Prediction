# author: Mahsa Sarafrazi, Rowan Sivanandam, Shiva Jena, and Vanessa Yuen
# date: 2021-11-24
# This script runs the Giant Pumpkin weight prediction model, creates output and generates the analysis report
# example usage: 
# make all


all : doc/pumpkin.html

# Download raw data
data/raw/pumpkins.csv : 
	python src/script/download_data.py --url="https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2021/2021-10-19/pumpkins.csv" --out_file="data/raw/pumpkins.csv"

# Clean data and split the data into train/test set
data/processed/pumpkins_train.csv data/processed/pumpkins_test.csv : data/raw/pumpkins.csv
	python src/script/clean_split_train_test.py --file="data/raw/pumpkins.csv" --out_dir="data/processed"

# Perform exploratory data anlysis
doc/result/eda_relationship.png doc/result/eda_distribution.png : data/processed/pumpkins_train.csv
	python src/script/eda.py --file="data/processed/pumpkins_train.csv" --out_dir="doc/result"

# Perform data preprocessing and tune regression model
doc/result/model.pickle doc/result/cvresults.csv doc/result/tuning_ridge.png: data/processed/pumpkins_train.csv
	python src/script/preprocessor_model.py --file="data/processed/pumpkins_train.csv" --out_dir="doc/result"

# Evalate the model with test result
doc/result/testscore.csv doc/result/test_result.csv doc/result/predict_result.png: doc/result/model.pickle data/processed/pumpkins_test.csv
	python src/script/evaluate.py --file='data/processed/pumpkins_test.csv' --object_file='doc/result/model.pickle' --out_dir='doc/result'

# Dependencies for sub documents of R markdown
doc/pumpkin.Rmd : doc/01_Summary.Rmd  doc/02_Intro.Rmd  doc/03_Data.Rmd  doc/04_EDA.Rmd  doc/05_Method.Rmd  doc/06_Results.Rmd doc/pumpkin_ref.bib 

# Render final report
doc/pumpkin.html : doc/pumpkin.Rmd  doc/result/eda_relationship.png doc/result/eda_distribution.png doc/result/cvresults.csv doc/result/testscore.csv doc/result/tuning_ridge.png doc/result/predict_result.png

	Rscript -e "rmarkdown::render('doc/pumpkin.Rmd')"

clean :
	rm -rf data
	rm -rf doc/result
	rm -rf doc/*.html

