import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import joblib
from data_preprocessing import preprocess_data

def train_model(df):
    X = df.drop(columns=["DelayMinutes", "FlightID", "ScheduledDeparture"])
    y = df["DelayMinutes"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = LinearRegression()
    model.fit(X_train, y_train)


    # Save model
    joblib.dump(model, "delay_model.pkl")
    print("✅ Model trained and saved as delay_model.pkl")

    return model, X_test, y_test

if __name__ == "__main__":
    # Load dataset
    df = pd.read_csv("dataset/india_flight_delay_synthetic.csv")
    df_encoded = preprocess_data(df)
    train_model(df_encoded)
