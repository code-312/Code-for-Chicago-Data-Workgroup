import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn import metrics

def load_data():
    data = pd.read_csv()
    X_train, X_test, y_train, y_test = train_test_split(data, test_size=0.2, random_state=312)
    return X_train, X_test, y_train, y_test

def train(X_train, y_train):
    clf = RandomForestRegressor(n_estimators=1000, random_state=312)
    clf.fit(X_train, y_train)
    return clf
    
def evaluate(clf, X_test, y_test):
    yhat = clf.predict(X_test)
    mse = metrics.mean_squared_error(y_test, yhat)
    mae = metrics.mean_absolute_error(y_test, yhat)
    r2 = metrics.r2_score(y_test, yhat)
    
    metrics = {
        "mean squared error": mse,
        "mean absolute error": mae,
        "r2": r2,
    }
    
    return metrics


def main():
    X_train, X_test, y_train, y_test = load_data()
    clf = train(X_train, y_train)
    metrics = evaluate(clf, X_test, y_test)
    
    print(metrics)
    