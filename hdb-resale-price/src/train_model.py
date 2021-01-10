import joblib
import logging
import numpy as np
import pandas as pd
import os
from dateutil.relativedelta import relativedelta
from feature_engineering import transform_quarter, transform_storey_range
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

def preprocess_features(data):
    data['datetime'] = pd.to_datetime(data['month'])
    data['quarter'] = transform_quarter(data['datetime'])
    data['flat_type'] = data['flat_type'].replace({
        'MULTI GENERATION': 'MULTI GENERATION',
        'MULTI-GENERATION': 'MULTI GENERATION',
    })
    data['flat_model'] = data['flat_model'].str.upper()
    data['new_storey_range'] = transform_storey_range(data['storey_range'])
    data = data.drop_duplicates()
    data = data[data['datetime']>='2009-01-01'] # only want to train on records from 2009-01-01 onwards
    return data

def train_pipeline(X_train, y_train, onehot_feats):
    y_train_log = np.log(y_train)
    preprocessor = ColumnTransformer(
        transformers=[
            ('onehot', OneHotEncoder(drop='first'), onehot_feats),
            # ('impute', SimpleImputer(), impute_feats),
        ],
        remainder='passthrough',
    )
    pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('regression', LinearRegression(fit_intercept=True)),
    ])
    pipeline.fit(X_train, y_train_log)
    return pipeline

def predict_pipeline(pipeline, X):
    y_pred = pipeline.predict(X)
    y_pred = np.exp(y_pred)
    return y_pred

def main(raw_dir, model_dir):
    """
    Preprocess data & train model
    """
    logger = logging.getLogger(__name__)

    logger.info(f'importing dataset...')
    data_path = os.path.join(raw_dir, 'hdb_resale_price.csv')
    data = pd.read_csv(data_path)

    logger.info(f'preprocessing dataset...')
    data = preprocess_features(data)

    logger.info(f'train test split...')
    cat_feats = ['quarter', 'town', 'flat_type', 'flat_model', 'new_storey_range']
    num_feats = ['floor_area_sqm', 'lease_commence_date']
    label_col = ['resale_price']
    X_train, X_test, y_train, y_test = train_test_split(
        data[cat_feats + num_feats], 
        data[label_col], 
        test_size=0.30, 
        random_state=42
    )

    logger.info(f'save training data...')
    X_train.to_csv(os.path.join(model_dir, 'X_train.csv'), index=False)
    X_test.to_csv(os.path.join(model_dir, 'X_test.csv'), index=False)
    y_train.to_csv(os.path.join(model_dir, 'y_train.csv'), index=False)
    y_test.to_csv(os.path.join(model_dir, 'y_test.csv'), index=False)

    logger.info(f'training model...')
    pipeline = train_pipeline(X_train, y_train, cat_feats)

    logger.info(f'evaluating model...')
    metrics = {
        'mae': {
            'train': mean_absolute_error(y_train, predict_pipeline(pipeline, X_train)),
            'test': mean_absolute_error(y_test, predict_pipeline(pipeline, X_test)),
        },
        'r2': {
            'train': r2_score(y_train, predict_pipeline(pipeline, X_train)),
            'test': r2_score(y_test, predict_pipeline(pipeline, X_test)),
        }
    }
    
    logger.info(f'model performance = {metrics}')
    joblib.dump(metrics, f'{MODEL_DIR}/metrics.joblib')

    logger.info(f'save model...')
    joblib.dump(pipeline, f'{MODEL_DIR}/pipeline.joblib')

if __name__ == '__main__':
    from config import RAW_DIR, MODEL_DIR, LoggingConfig
    LoggingConfig()
    main(RAW_DIR, MODEL_DIR)