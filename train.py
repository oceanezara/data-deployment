import pandas as pd
import numpy as np
import mlflow
import time
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler, OneHotEncoder 
from sklearn.model_selection import train_test_split
from mlflow.models.signature import infer_signature


import os
import time
import joblib
import mlflow

import pandas as pd

from sklearn.model_selection import train_test_split
from mlflow.models.signature import infer_signature

from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler, OneHotEncoder 

if __name__ == "__main__":

    print("training model...")
    start_time = time.time()

   # Set your variables for your environment
    EXPERIMENT_NAME="price_car"
    # Set experiment's info 
    mlflow.set_experiment(EXPERIMENT_NAME)
    # Get our experiment info
    experiment = mlflow.get_experiment_by_name(EXPERIMENT_NAME)

    df = pd.read_csv("./get_around_pricing_project.csv")
    df = df.iloc[: , 1:]

    target = "rental_price_per_day"

    x = df.drop(target, axis=1)
 
    y = df.loc[:,target]

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.2, random_state=0)

    def categorie(x):
        numeric_features = []
        categorical_features = []
        for i,t in x.dtypes.items():
            if ('float' in str(t)) or ('int' in str(t)) :
                numeric_features.append(i)
            else :
                categorical_features.append(i)
        return numeric_features, categorical_features

    numeric_features, categorical_features = categorie(x)

    numeric_transformer = Pipeline(steps=[
            ('scaler', StandardScaler())
            ])
    categorical_transformer = Pipeline(steps=[
            ('encoder', OneHotEncoder(drop='first', handle_unknown='ignore')) 
            ])
    preprocessor = ColumnTransformer(
            transformers=[
                ('num', numeric_transformer, numeric_features),
                ("cat", categorical_transformer, categorical_features)
            ])
        
    model = Pipeline(steps=[("Preprocessing", preprocessor),
                            ("Regressor", LinearRegression())
                            ]) 
       

    with mlflow.start_run(experiment_id = experiment.experiment_id):

        model.fit(x_train, y_train)

        predictions = model.predict(x_train)
        
        mlflow.sklearn.log_model(
            sk_model=model,
            artifact_path="price_car",
            registered_model_name="price_car_model",
            signature=infer_signature(x_train, predictions)
        )

    # joblib.dump(model, "model.joblib")

    print("...Done!")
    print(f"---Total training time: {time.time()-start_time}")

# df = pd.read_csv("./get_around_pricing_project.csv")
# df = df.iloc[: , 1:]

# target = "rental_price_per_day"

# x = df.drop(target, axis=1)

# y = df.loc[:,target]

# x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.2, random_state=0)

# def categorie(x):
#     numeric_features = []
#     categorical_features = []
#     for i,t in x.dtypes.items():
#         if ('float' in str(t)) or ('int' in str(t)) :
#             numeric_features.append(i)
#         else :
#             categorical_features.append(i)
#     return numeric_features, categorical_features

# numeric_features, categorical_features = categorie(x)

# categorical_transformer = Pipeline(
#     steps=[
#     ('encoder', OneHotEncoder(drop='first', handle_unknown='ignore'))
#     ])

# numeric_transformer = Pipeline(steps=[
#     ('scaler', StandardScaler())
# ])

# preprocessor = ColumnTransformer(
#     transformers=[
#         ('num', numeric_transformer, numeric_features),
#         ('cat', categorical_transformer, categorical_features)
#     ])

# # Preprocessings on train set
# x_train = preprocessor.fit_transform(x_train)

# # Preprocessings on test set
# x_test = preprocessor.transform(x_test) 

