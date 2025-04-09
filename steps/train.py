import os
import joblib
import yaml
from sklearn.preprocessing import StandardScaler, RobustScaler, MinMaxScaler
from sklearn.compose import ColumnTransformer
from imblearn.pipeline import Pipeline 
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier
from sklearn.linear_model import SGDClassifier
from sklearn.naive_bayes import GaussianNB
import pandas as pd
from imblearn.over_sampling import SMOTE, ADASYN

class Trainer:
    def __init__(self):
        self.config = self.load_config()
        self.model_name = self.config['model'][5]['name']
        """
        To use just the first model in the config.yml use this code "self.model_name = self.config['model'][0]['name']"
        """
        self.model_params = self.config['model'][5]['params']
        self.model_path = self.config['model'][5]['store_path']
        self.pipeline = self.create_pipeline()

    def load_config(self):
        with open('config.yml', 'r') as config_file:
            return yaml.safe_load(config_file)
        
    def create_pipeline(self):
        preprocessor = ColumnTransformer(transformers=[
            ('standardize', MinMaxScaler(), ["tcp.srcport", 'tcp.dstport', "frame.len", 'Packets', 'Bytes', 'Tx Packets', 'Tx Bytes', 'Rx Bytes', 'Rx Packets']),
        ])
        
        smote = ADASYN(random_state=42, sampling_strategy="auto")
        model_map = {
            'RandomForestClassifier': RandomForestClassifier,
            'DecisionTreeClassifier': DecisionTreeClassifier,
            'SVC': SVC,
            'MLPClassifier': MLPClassifier,
            'SGDClassifier': SGDClassifier,
            'GaussianNB': GaussianNB
        }
    
        model_class = model_map[self.model_name]
        model = model_class(**self.model_params)

        pipeline = Pipeline([
            ('preprocessor', preprocessor),
            ('smote', smote),
            ('model', model)
        ])

        return pipeline

    def feature_target_separator(self, data):
        X = data.iloc[:, :-1]
        y = data.iloc[:, -1]
        return X, y
    
        
    def train_model(self, X_train, y_train):
        self.pipeline.fit(X_train, y_train)

    def save_model(self):
        model_file_path = os.path.join(self.model_path, 'model.pkl')
        
        # Ensure the directory exists
        os.makedirs(self.model_path, exist_ok=True)
        
        joblib.dump(self.pipeline, model_file_path)

# # Usage
# if __name__ == "__main__":
#     trainer = Trainer()
#     data = pd.read_csv('data/train.csv')
#     X, y = trainer.feature_target_separator(data)
#     trainer.train_model(X, y)
#     trainer.save_model()
