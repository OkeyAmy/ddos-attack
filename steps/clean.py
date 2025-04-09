import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import LabelEncoder

class Cleaner:
    def __init__(self):
        self.imputer = SimpleImputer(strategy='most_frequent', missing_values=np.nan)

    def clean_data(self, data: pd.DataFrame) -> pd.DataFrame:
        """Clean the dataset."""
        # Remove unnecessary columns
        data.drop(['ip.src', 'ip.dst', 'frame.time'], axis=1, inplace=True)

        # Remove duplicate entries
        data.drop_duplicates(inplace=True)

        # Handle missing values for categorical columns
        for col in data.columns:
            if data[col].dtype == 'object':
                data[col] = data[col].fillna(data[col].mode()[0]) 
            else:
                data[col] = self.imputer.fit_transform(data[[col]]).flatten()

        # Encode the label column
        label_encoder = LabelEncoder()
        data['Label_Numeric'] = label_encoder.fit_transform(data['Label'])
        data_transform = data.drop('Label', axis=1)
        
        return data_transform 

# Usage example
if __name__ == "__main__":
    clean = Cleaner()
    data = pd.read_csv('data/train.csv')
    cleaned_train = clean.clean_data(data)
    print(f"Clean data:\n{cleaned_train.head()}")
    print(cleaned_train.columns)
    print(cleaned_train['Label_Numeric'].value_counts().unique)
