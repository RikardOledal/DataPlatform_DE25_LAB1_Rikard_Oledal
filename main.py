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

    products_df["price"] = pd.to_numeric(products_df["price"], errors="coerce")
    products_df["created_at"] = pd.to_datetime(products_df["created_at"], errors="coerce")

    # Flag for errors

    products_df["missing_id"] = products_df["id"].isna()
    products_df["missing_name"] = products_df["name"].isna()
    products_df["missing_price"] = products_df["price"].isna()
    products_df["negative price"] = products_df["price"] < 0
    products_df["to_low_price"] = products_df["price"].between(0,5)
    products_df["to_high_price"] = products_df["price"] >= 10000
    products_df["missing_currency"] = products_df["currency"].isna()
    products_df["missing_create_date"] = products_df["created_at"].isna()

    rejects_condition = (
        (products_df["missing_id"] == True)|
        (products_df["negative price"] == True)|
        (products_df["missing_currency"] == True)
    )
    
    # Rejected data
    rejected_df = products_df[rejects_condition].copy()
    
    rejected_df["reject_code"] = ""
    rejected_df["reject_reason"] = ""
    
    rejected_df.loc[rejected_df["missing_id"] == True, "reject_reason"] = "Missing ID"
    rejected_df.loc[rejected_df["missing_id"] == True, "reject_code"] = "31"
    rejected_df.loc[rejected_df["negative price"] == True, "reject_reason"] = "Price is negative"
    rejected_df.loc[rejected_df["negative price"] == True, "reject_code"] = "32"
    rejected_df.loc[rejected_df["missing_currency"] == True, "reject_reason"] = "Missing currency"
    rejected_df.loc[rejected_df["missing_currency"] == True, "reject_code"] = "33"
    
    # Validated data
    validated_df = products_df[~rejects_condition].copy()
    
    validated_df["status_code"] = "10"
    validated_df["status_reason"] = "Validated"
    
    validated_df.loc[validated_df["missing_name"] == True, "status_code"] = "21"
    validated_df.loc[validated_df["missing_name"] == True, "status_reason"] = "Flagged: Missing name"
    validated_df.loc[validated_df["missing_create_date"] == True, "status_code"] = "22"
    validated_df.loc[validated_df["missing_create_date"] == True, "status_reason"] = "Flagged: Missing Create-date"
    validated_df.loc[validated_df["missing_price"] == True, "status_code"] = "23"
    validated_df.loc[validated_df["missing_price"] == True, "status_reason"] = "Flagged: Missing price"
    validated_df.loc[validated_df["to_high_price"] == True, "status_code"] = "24"
    validated_df.loc[validated_df["to_high_price"] == True, "status_reason"] = "Flagged: Price over 10_000"
    validated_df.loc[validated_df["to_low_price"] == True, "status_code"] = "25"
    validated_df.loc[validated_df["to_low_price"] == True, "status_reason"] = "Flagged: Price under 6"
    
    cols_to_remove = [
        "missing_id", "missing_name", "missing_price", 
        "negative price", "to_low_price",
        "to_high_price", "missing_currency",
        "missing_create_date"
    ]
    
    validated_df = validated_df.drop(columns=cols_to_remove)
    rejected_df = rejected_df.drop(columns=cols_to_remove)