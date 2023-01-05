# data-deployment

#Model 
````
import mlflow
logged_model = 'runs:/d2489a417f6f4003bf1c1ee1758874de/price_car'

# Load model as a PyFuncModel.
loaded_model = mlflow.pyfunc.load_model(logged_model)

# Predict on a Pandas DataFrame.
import pandas as pd
loaded_model.predict(pd.DataFrame(data))
```