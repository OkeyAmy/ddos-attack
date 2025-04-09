import os
import joblib
from sklearn.metrics import accuracy_score, classification_report, roc_auc_score, confusion_matrix
import pandas as pd

class Predictor:
    def __init__(self):
        self.model_path = self.load_config()['model'][1]['store_path']
        self.pipeline = self.load_model()

    def load_config(self):
        import yaml
        with open('config.yml', 'r') as config_file:
            return yaml.safe_load(config_file)

    def load_model(self):
        model_file_path = os.path.join(self.model_path, 'model.pkl')
        return joblib.load(model_file_path)

    def feature_target_separator(self, data):
        X = data.iloc[:, :-1]
        y = data.iloc[:, -1]
        return X, y

    def evaluate_model(self, X_test, y_test):
        y_pred_proba = self.pipeline.predict_proba(X_test)
        y_pred = self.pipeline.predict(X_test)

        accuracy = accuracy_score(y_test, y_pred)
        class_report = classification_report(y_test, y_pred, zero_division=1.0, target_names=["Benign", "DDoS-ACK", "DDoS-PSH-ACK"])
        conf_matrix = confusion_matrix(y_test, y_pred)
        roc_auc = roc_auc_score(y_test, y_pred_proba, multi_class='ovr')

        return accuracy, class_report, roc_auc, conf_matrix

# Usage
if __name__ == "__main__":
    data = pd.read_csv('data/train.csv')
    predictor = Predictor()
    predictor.load_model()
    X, y = predictor.feature_target_separator(data=data)
    accuracy, class_report, roc_auc = predictor.evaluate_model(X, y)

