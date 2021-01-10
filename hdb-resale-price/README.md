# HDB Resale Flats

## Purpose

Use case
1. Develop my own HDB resale price index to compare with publicly available index
2. Develop my own price predictor as an additional reference against actual valuation of HDB on sale

Technical learning
1. Learn price index methodology
2. Learn "click" by implementing CLI APIs
3. Learn "pytest" by implementing tests for feature engineering codes
4. Learn sklearn's pipeline by combining preprocessing steps & regressor into a single pipeline

## Setup

Perform steps to replicate model

1. Change path to project directory

2. Download external dataset
```
python src/download_data.py hdb
python src/download_index.py hdb
```

3. Train model
```
python src/train_model.py
```

## Results

- Refer to notebooks for data exploration & model evaluation
- Evaluaton results suggest that there is a gap between my price index vs publicly available price index
- Perhaps adding better predictors will improve prediction accuracy & price index difference

