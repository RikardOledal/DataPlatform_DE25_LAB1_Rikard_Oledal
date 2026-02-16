import pandas as pd

if __name__ == "__main__":

    products_df = pd.read_csv("data/Products_raw.csv", delimiter=";")
    print(products_df)