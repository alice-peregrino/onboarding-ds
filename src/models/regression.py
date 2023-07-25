from sklearn.model_selection import GridSearchCV # reference: https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.GridSearchCV.html
from sklearn.model_selection import train_test_split

from sklearn.ensemble import RandomForestRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.svm import SVR

from sklearn.metrics import mean_squared_error, mean_absolute_error, explained_variance_score, r2_score, mean_absolute_percentage_error

import pandas as pd
import os
import csv

import click
from tqdm import tqdm
import time

available_models = {
        
    'RandomForestRegressor': {
        'model': RandomForestRegressor(), 
        'parameters': {
            'n_estimators': [10, 100], 
            'criterion': ['squared_error', 'absolute_error', 'friedman_mse', 'poisson']
        }
    },

    'KNeighborsRegressor': {
        'model': KNeighborsRegressor(),
        'parameters': {
            'n_neighbors': [5, 7, 9, 11]
        }
    },

    'MLPRegressor': {
        'model': MLPRegressor(), 
        'parameters': {
            'activation': ['identity', 'logistic', 'tanh', 'relu'], 
            'solver': ['lbfgs', 'sgd', 'adam']
        }
    }
}
  
@click.command()
@click.option('--features_path', default='../../data/processed/features.csv')
@click.option('--target_col', default='rating')
@click.option('--test_size', default=0.3)
@click.option('--results_path', default='./')
def regression(
    features_path: str, 
    target_col: str, 
    test_size: float, 
    results_path: str):
    
    df = pd.read_csv(features_path)
    y = df[target_col]
    X = df[[col for col in df.columns if col != target_col]]
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=42)
    
    results = {}
    
    with open(os.path.join(results_path, 'results.csv'), 'w') as output:
        
        cols = ['model', 'best_params', 'mean_squared_error', 'explained_variance', 'r2', 
                'mean_absolute_error', 'mean_absolute_percentage_error', 'execution_time']
        
        writer = csv.DictWriter(output, fieldnames=cols)
        writer.writeheader()
        
        for model in tqdm(available_models.keys()):

            init = time.time()

            clf = GridSearchCV(
                available_models[model]['model'], 
                available_models[model]['parameters'], 
                scoring='neg_root_mean_squared_error', 
                verbose=10)

            clf.fit(X_train, y_train)

            y_pred = clf.predict(X_test)

            final = time.time() - init

            results['model'] = model
            results['best_params'] = clf.best_params_
            results['mean_squared_error'] = mean_squared_error(y_test, y_pred)
            results['explained_variance'] = explained_variance_score(y_test, y_pred)
            results['r2'] = r2_score(y_test, y_pred)
            results['mean_absolute_error'] = mean_absolute_error(y_test, y_pred)
            results['mean_absolute_percentage_error'] = mean_absolute_percentage_error(y_test, y_pred)
            results['execution_time'] = final
            
            writer.writerow(results)
        
if __name__ == '__main__':
    regression()