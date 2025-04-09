import joblib
import pandas as pd
from steps.clean import Cleaner
from evidently.report import Report
from evidently.metric_preset import (
    DataDriftPreset, 
    DataQualityPreset, 
    TargetDriftPreset, 
    ClassificationPreset
)
from evidently.test_suite import TestSuite
from evidently.test_preset import MulticlassClassificationTestPreset
from evidently import ColumnMapping
import mlflow
import warnings

warnings.filterwarnings("ignore")

# Load the model (MLflow or Joblib)
model = joblib.load('models/model.pkl') 

# Loading data
train = pd.read_csv("data/train.csv")
test = pd.read_csv("data/test.csv")

# Clean data
cleaner = Cleaner()
train = cleaner.clean_data(train)
test = cleaner.clean_data(test)

# Apply model predictions
train['prediction'] = model.predict(train.iloc[:, :-1])
test['prediction'] = model.predict(test.iloc[:, :-1])

# Apply column mapping based on the dataset
target = 'Label_Numeric'
prediction = 'prediction'
numerical_features = ['Packets', 'Bytes', 'Tx Packets', 'Tx Bytes', 
                      'Rx Packets', 'Rx Bytes', 'tcp.srcport', 'tcp.dstport', 
                      'ip.proto', 'frame.len', 'tcp.flags.syn', 'tcp.flags.reset', 
                      'tcp.flags.push', 'tcp.flags.ack', 'ip.flags.mf', 
                      'ip.flags.df', 'ip.flags.rb', 'tcp.seq', 'tcp.ack']
category_features = ['Label_Numeric']

# Define column mapping
column_mapping = ColumnMapping()
column_mapping.target = target
column_mapping.prediction = prediction
column_mapping.numerical_features = numerical_features
column_mapping.categorical_features = category_features

# Define custom metrics for detailed observability
custom_metrics = [
    DataDriftPreset(),  # Measures feature drift between training and test data
    DataQualityPreset(),  # Checks data quality, e.g., missing values, outliers, etc.
    TargetDriftPreset(),  # Measures target variable drift
    ClassificationPreset()  # Includes confusion matrix, precision, recall, F1-score
]

# Create a report with the custom metrics
data_drift_report = Report(metrics=custom_metrics)

# Run the report with the reference and current data
data_drift_report.run(reference_data=train, current_data=test, column_mapping=column_mapping)


# Save the report as HTML (you can view this in the browser)
data_drift_report.save_html("data_drift_report.html")

# Run the classification tests separately with TestSuite (to assess model performance)
classification_tests = TestSuite(tests=[MulticlassClassificationTestPreset()])

# Run the classification tests on the data
classification_tests.run(reference_data=train, current_data=test, column_mapping=column_mapping)

# Save the classification test results as HTML (including confusion matrix, precision/recall, F1-score)
classification_tests.save_html("classification_tests.html")
