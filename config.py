import os

# Set the tracking URI for MLflow, pointing to your desired location
os.environ["MLFLOW_TRACKING_URI"] = "mlruns"

# Set the experiment name specific to your use case
os.environ["MLFLOW_EXPERIMENT_NAME"] = "network_traffic_prediction"
