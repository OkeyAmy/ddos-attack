import pandas as pd
import yaml
import os

class Ingestion:
    def __init__(self):
        self.config = self.load_config()

    def load_config(self):
        with open("config.yml", "r") as file:
            return yaml.safe_load(file)

    def load_data(self):
        data_dir = self.config['data']['data_dir']
        train_data_path = os.path.join(data_dir, self.config['data']['train_path'])
        test_data_path = os.path.join(data_dir, self.config['data']['test_path'])
        train_data = pd.read_csv(train_data_path)
        test_data = pd.read_csv(test_data_path)
        return train_data, test_data

# # Usage
# if __name__ == "__main__":
#     ingestion = Ingestion()
#     train, test = ingestion.load_data()
#     print(f"Training set\n{train.head()}")
#     print(f"Test set\n{test.head()}")