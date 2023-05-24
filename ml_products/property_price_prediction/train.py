from pprint import pprint

import numpy as np
from sklearn.linear_model import LinearRegression
import duckdb
import os
import mlflow


features = ["MedInc",	"HouseAge",	"AveRooms", "AveBedrms", "Population",	"AveOccup",	"Latitude",
            "Longitude"]

def main():
    # enable autologging
    mlflow.sklearn.autolog()
    X, y = None, None
    conn = duckdb.connect(os.getenv("FEATURE_STORE_HOME"))
    Xy = conn.sql("select * from raw.housing").df()
    X = Xy[features]
    y = Xy["target"]
    conn.close()


    # train a model
    model = LinearRegression()
    model.fit(X, y)
    run_id = mlflow.last_active_run().info.run_id
    print("Logged data and model in run {}".format(run_id))

    # show logged data
    # for key, data in fetch_logged_data(run_id).items():
    #     print("\n---------- logged {} ----------".format(key))
    #     pprint(data)


if __name__ == "__main__":
    main()