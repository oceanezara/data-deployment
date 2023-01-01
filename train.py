import pandas as pd
import numpy as np
import mlflow
import time
from sklearn.model_selection import train_test_split, GridSearchCV 
from sklearn.preprocessing import  StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import Pipeline


if __name__ == "__main__":

# Set your variables for your environment
    EXPERIMENT_NAME="hyperparameter_tuning"
    # Set experiment's info 
    mlflow.set_experiment(EXPERIMENT_NAME)
    # Get our experiment info
    experiment = mlflow.get_experiment_by_name(EXPERIMENT_NAME)
    
    print("training model...")
    
    # Time execution
    start_time = time.time()

    # Call mlflow autolog
    mlflow.sklearn.autolog()

    # Import dataset
    df = pd.read_csv("https://julie-2-next-resources.s3.eu-west-3.amazonaws.com/full-stack-full-time/linear-regression-ft/californian-housing-market-ft/california_housing_market.csv")

    # X, y split 
    X = df.iloc[:, :-1]
    y = df.iloc[:, -1]

    # Train / test split 
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2)

    # Pipeline 
    pipe = Pipeline(steps=[
        ("standard_scaler", StandardScaler()),
        ("Random_Forest",RandomForestRegressor())
    ])

    with mlflow.start_run(experiment_id = experiment.experiment_id):

        params_grid = {
            "Random_Forest__n_estimators": [10, 50], # list(range(10,101, 10)),
            "Random_Forest__criterion": ["squared_error"],
            "Random_Forest__max_depth": [5, 20], #list(range(5, 35, 10)) + [None],
            "Random_Forest__min_samples_split": [2, 20] #list(range(2, 40, 3))
        }

        model = GridSearchCV(pipe, params_grid, n_jobs=-1, verbose=3, cv=3, scoring="r2")
        model.fit(X_train, y_train)


        mlflow.log_metric("Train Score", model.score(X_train, y_train))
        mlflow.log_metric("Test Score", model.score(X_test, y_test))
        
        mlflow.sklearn.log_model(
            sk_model=model,
            artifact_path="modeling_housing_market",
            registered_model_name="random_forest"
        )
       
    print("...Training Done!")
    print(f"---Total training time: {time.time()-start_time} seconds")

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

