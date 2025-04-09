import pandas as pd
import yaml
from sklearn.model_selection import train_test_split
import os

class DataSplitter:
    def __init__(self):
        self.config = self.load_config()

    @staticmethod
    def load_config():
        with open("config.yml", "r") as file:
            return yaml.safe_load(file)

    def split_and_save_data(self, raw_data_path=None, test_size=None, random_state=None, startify=None):
        data_dir = self.config['data']['data_dir']
        raw_data_path = raw_data_path or self.config['data']['raw_data_path']
        test_size = test_size or self.config['train']['test_size']
        random_state = random_state or self.config['train']['random_state']
        
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
        
        data = pd.read_csv(raw_data_path)
        
        train_data, test_data = train_test_split(
            data,
            test_size=test_size,
            random_state=random_state,
            shuffle=self.config['train']['shuffle'],
            stratify= data["Label"]
        )
        
        train_path = os.path.join(data_dir, self.config['data']['train_path'])
        test_path = os.path.join(data_dir, self.config['data']['test_path'])
        
        # Ensure the parent directory for train_path and test_path exists
        os.makedirs(os.path.dirname(train_path), exist_ok=True)
        os.makedirs(os.path.dirname(test_path), exist_ok=True)

        train_data.to_csv(train_path, index=False)
        test_data.to_csv(test_path, index=False)
        
        print(f"Train data saved to: {train_path}")
        print(f"Test data saved to: {test_path}")
        print(f"Train data shape: {train_data.shape}")
        print(f"Test data shape: {test_data.shape}")
        
        return train_data, test_data

    # Uncommet this section for testing
    def load_split_data(self):
        data_dir = self.config['data']['data_dir']
        train_path = os.path.join(data_dir, self.config['data']['train_path'])
        test_path = os.path.join(data_dir, self.config['data']['test_path'])
        
        train_data = pd.read_csv(train_path)
        test_data = pd.read_csv(test_path)
        
        return train_data, test_data

# Usage
if __name__ == "__main__":
    data_splitter = DataSplitter()
    train_data, test_data = data_splitter.split_and_save_data()
    train_data, test_data = data_splitter.load_split_data()
    print(f"Training set\n{train_data.head()}")
    print(train_data['Label'].value_counts().unique)