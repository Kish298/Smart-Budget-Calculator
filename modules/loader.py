import pandas as pd

def load_data():
    df = pd.read_csv("data/expenses.csv")
    df["Date"] = pd.to_datetime(df["Date"])
    return df