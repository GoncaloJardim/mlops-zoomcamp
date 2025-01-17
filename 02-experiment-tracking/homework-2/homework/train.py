import os
import pickle
import click

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import mlflow


def load_pickle(filename: str):
    with open(filename, "rb") as f_in:
        return pickle.load(f_in)


@click.command()
@click.option(
    "--data_path",
    default="../output",
    help="Location where the processed NYC taxi trip data was saved"
)
def run_train(data_path: str):

    
    mlflow.set_tracking_uri("sqlite:///mlflow.db")
    mlflow.set_experiment("homework-2")
    print("Tracking URI and Experiment set.")
    with mlflow.start_run():

        mlflow.sklearn.autolog()
        print("Autolog set.")
        X_train, y_train = load_pickle(os.path.join(data_path, "train.pkl"))
        X_val, y_val = load_pickle(os.path.join(data_path, "val.pkl"))
        mlflow.set_tag("model", "random_forest")
        rf = RandomForestRegressor(max_depth=10, random_state=0)
        rf.fit(X_train, y_train)
        y_pred = rf.predict(X_val)

        print("Predictions complete.")

        rmse = mean_squared_error(y_val, y_pred, squared=False)
        mlflow.log_metric("rmse", rmse)
        print("RMSE Logged.")
        
        with open("mlruns/models/randon_forest_reg.bin", "wb") as f_out:
            pickle.dump(rf, f_out)

        mlflow.log_artifact(local_path="mlruns/models/randon_forest_reg.bin", artifact_path="models_pickle")
        mlflow.sklearn.log_model(rf, artifact_path="models_mlflow")

        print("Model logged.")


if __name__ == '__main__':
    run_train()



