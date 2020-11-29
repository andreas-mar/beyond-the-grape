# Beyond the grape
A repo containing scraper utilities, data preprocessing, and machine learning implementations of the underlying Vivino.com data. The data is served on a flask webserver, which contains an online XG Boost predictive model. The repos is the underlying code for our Vivino machine learning project in Data Science for Business Applications course at Copenhagen Business School.

The features fall into these main categories.

## Scraping
This folder contains the scrips used to scrape vivino.com, along with a file describing their functionality. Some of these scrips require an somewhat intimate knowledge of the underlying data structures to fully understand. We have not saved intermediate files or outputs in this folder.

## Data
The priliminary data is saved here. The data sets are the result of the scraping process, but have only been processed to a very limited extent.

## Notebooks
The primary analysis is conducted in .ipynb format, and linked here. Note: Some outputs (primarity JS charts) do not translate well from Google Colab to Jupyter, so each notebook contains a link to the original colab notebook, from which the contains can be viewed as originally intended. These nootbooks will take the reader through data subsetting, selection, merging, preprocessing and analysis. There are 3 notebooks - one for each main chapter of the paper (Preprocessing and EDA, Regression Analysis and Natural Language Processing). Links to the original Notebooks can also be found below:

Exploratory data analysis:
https://drive.google.com/file/d/1bTdJi-BtXCiIq8jhSqaTmMTrWaV53xoR/view?usp=sharing

Supervised Machine Learning and Deep Learning:
https://colab.research.google.com/drive/1NL417renbq77Lm488I7erQhVAMD_Nm3Q?usp=sharing

Natural Language Processing:
https://colab.research.google.com/drive/1XpE4Kqe9xo1lFELULC32-3yuh8N6zo6a?usp=sharing

## App
This is the foldering containing the source code for our companion website www.dsba-vinoveritas.com, which is a flask-served webapp. The website contains a live-updating version of the final XGBoost regression model in .joblib format, deployed online.


