# Makefile
# author: Mahsa Sarafrazi, Rowan Sivanandam, Shiva Jena, and Vanessa Yuen
# date: 2021-12-03

# This script runs the Giant Pumpkin weight prediction model, creates output and generates the analysis report

#uncomment and run the below line if image file can't be generated in eda.py and evaluate.py
#npm install -g vega vega-cli vega-lite canvas

#example Usage: 
# make all

all: doc/pumpkin.Rmd 

# Download raw data
data/raw/pumpkins.csv : src/script/download_data.py
	python src/script/download_data.py --url="https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2021/2021-10-19/pumpkins.csv" --out_file="data/raw/pumpkins.csv"


# Clean data and split the data into train/test set
data/processed : data/raw/pumpkins.csv src/script/clean_split_train_test.py
	python src/script/clean_split_train_test.py --file="data/raw/pumpkins.csv" --out_dir="data/processed"
	
# Perform exploratory data anlysis
doc/result_eda : data/processed src/script/eda.py
	python src/script/eda.py --file="data/processed/pumpkins_train.csv" --out_dir="doc/result"
	
# Perform data preprocessing and tune regression model
doc/result_model : data/processed src/script/preprocessor_model.py
	python src/script/preprocessor_model.py --file="data/processed/pumpkins_train.csv" --out_dir="doc/result"


# Evalate the model with test result
doc/result_test : data/processed doc/result_model src/script/evaluate.py
	python src/script/evaluate.py --file='data/processed/pumpkins_test.csv' --object_file='doc/result/model.pickle' --out_dir='doc/result'


# Render final report
# modified by Vanessa
doc/pumpkin.Rmd : doc/result_model doc/result_test doc/result_eda 
	Rscript -e "rmarkdown::render('doc/pumpkin.Rmd')"

clean:
# modified by Vanessa
	rm -rf doc/result/*
	rm -rf data/raw/pumpkins.csv
	rm -rf data/processed/*
	