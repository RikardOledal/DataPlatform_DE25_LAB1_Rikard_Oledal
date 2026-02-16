import pandas as pd

if __name__ == "__main__":

    print("---IMPORT DATA---")
    products_raw_df = pd.read_csv("data/Products_raw.csv", delimiter=";")
    print(products_raw_df.values)
    print("---CLEANING DATA---")

    products_df = products_raw_df.copy()

    # Sting cleaning
    products_df["id"] = (
        products_df["id"]
        .str.strip()
        .str.replace(r'\s{2,}', ' ', regex=True)
        .str.replace(" ", "")
        .str.upper()
    )

    products_df["name"] = (
        products_df["name"]
        .str.strip()
        .str.title()
        .str.replace(r'\s{2,}', ' ', regex=True)
    )

    products_df["price"] = (
        products_df["price"]
        .str.strip()
        .str.lower()
        .str.replace(r'\s{2,}', ' ', regex=True)
        .str.replace(" ", "")
        .str.replace("kr", "")
        .str.replace("sek", "")
    )

    products_df["currency"] = (
        products_df["currency"]
        .str.strip()
        .str.replace(r'\s{2,}', ' ', regex=True)
        .str.replace(" ", "")
        .str.upper()
    )

    products_df["created_at"] = (
        products_df["created_at"]
        .str.strip()
        .str.replace("/", "-")
    )

    print(products_df.values)

    print("---CONVERTING DATATYPES---")

    products_df["price"] = pd.to_numeric(products_df["price"], errors="coerce")
    products_df["created_at"] = pd.to_datetime(products_df["created_at"], errors="coerce")

    print("---FLAGG ERRORS---")

    products_df["missing_id"] = products_df["id"].isna()
    products_df["missing_name"] = products_df["name"].isna()
    products_df["missing_price"] = products_df["price"].isna()
    products_df["Non_positive_price"] = products_df["price"] <= 0
    products_df["To_high_price"] = products_df["price"] >= 10000
    products_df["missing_currency"] = products_df["currency"].isna()
    products_df["missing_create_date"] = products_df["created_at"].isna()









    