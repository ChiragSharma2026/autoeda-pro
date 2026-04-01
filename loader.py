import pandas as pd
import sys

def load_csv(path):
    df = pd.read_csv(path)
    print(f"Loaded: {df.shape[0]} rows, {df.shape[1]} columns")
    return df

if __name__ == "__main__":
    df = load_csv(sys.argv[1])