import pandas as pd

def load_data(path):
    df = pd.read_csv(path)
    return df

def preprocess_data(df):
    # Encode categorical variables
    df_encoded = pd.get_dummies(df, columns=["Airline", "Origin", "Destination", "DelayCause"], drop_first=True)
    return df_encoded
