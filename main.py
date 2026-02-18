from pathlib import Path
import pandas as pd

if __name__ == "__main__":
    base_path = Path(__file__).parent
    data_folder = base_path / "data"
    importfile_path = data_folder / "Products_raw.csv"

    if importfile_path.exists():
        products_raw_df = pd.read_csv(importfile_path, delimiter=";")
        print("====DATA EXTRACTED====")
    else:
        print(f"Did not find file at: {importfile_path}")

    print("====TRANSFORM DATA====")

    products_df = products_raw_df.copy()

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

    # Converting Datatypes
    products_df["price"] = pd.to_numeric(products_df["price"], errors="coerce")
    products_df["created_at"] = pd.to_datetime(products_df["created_at"], errors="coerce")

    print("====REJECTING ROWS====")
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
        (products_df["missing_price"] == True)|
        (products_df["negative price"] == True)|
        (products_df["missing_currency"] == True)
    )

    # Rejected data
    rejected_df = products_df[rejects_condition].copy()

    rejected_df["reject_code"] = ""
    rejected_df["reject_reason"] = ""

    rejected_df.loc[rejected_df["missing_id"] == True, "reject_reason"] = "Missing ID"
    rejected_df.loc[rejected_df["missing_id"] == True, "reject_code"] = "31"
    rejected_df.loc[rejected_df["missing_currency"] == True, "reject_reason"] = "Missing currency"
    rejected_df.loc[rejected_df["missing_currency"] == True, "reject_code"] = "32"
    rejected_df.loc[rejected_df["negative price"] == True, "reject_reason"] = "Price is negative"
    rejected_df.loc[rejected_df["negative price"] == True, "reject_code"] = "33"
    rejected_df.loc[rejected_df["missing_price"] == True, "reject_reason"] = "Missing price"
    rejected_df.loc[rejected_df["missing_price"] == True, "reject_code"] = "34"

    cols_to_remove = [
        "missing_id", "missing_name", "missing_price", 
        "negative price", "to_low_price",
        "to_high_price", "missing_currency",
        "missing_create_date"
    ]

    print("====LOAD rejected_products.csv====")
    rejected_df = rejected_df.drop(columns=cols_to_remove)
    rejects_file_path = data_folder / "rejected_products.csv"
    rejected_df.to_csv(rejects_file_path, index=False)

    # Validated data
    validated_df = products_df[~rejects_condition].copy()

    validated_df["status_code"] = "10"
    validated_df["status_reason"] = "Validated"

    validated_df.loc[validated_df["missing_name"] == True, "status_code"] = "21"
    validated_df.loc[validated_df["missing_name"] == True, "status_reason"] = "Flagged: Missing name"
    validated_df.loc[validated_df["missing_create_date"] == True, "status_code"] = "22"
    validated_df.loc[validated_df["missing_create_date"] == True, "status_reason"] = "Flagged: Missing Create-date"
    validated_df.loc[validated_df["to_high_price"] == True, "status_code"] = "23"
    validated_df.loc[validated_df["to_high_price"] == True, "status_reason"] = "Flagged: Price over 10_000"
    validated_df.loc[validated_df["to_low_price"] == True, "status_code"] = "24"
    validated_df.loc[validated_df["to_low_price"] == True, "status_reason"] = "Flagged: Price under 6"
    
    print("====LOAD validated_products.csv====")
    validated_df = validated_df.drop(columns=cols_to_remove)
    validated_file_path = data_folder / "validated_products.csv"
    validated_df.to_csv(validated_file_path, index=False)

    print("====CALCULATING analytics summary====")
    product_mean = validated_df.query("status_code == '10'")["price"].mean().round(2)
    product_mean_fl = validated_df["price"].mean().round(2)
    product_median = validated_df.query("status_code == '10'")["price"].median().round(2)
    product_median_fl = validated_df["price"].median().round(2)
    product_count = validated_df.query("status_code == '10'")["status_code"].count()
    product_count_fl = validated_df["status_code"].count()
    price_missing = rejected_df.query("reject_code == '34'")["reject_code"].count()

    analytics_summary_df = pd.DataFrame(
        {
            "snittpris": [product_mean],
            "snittpris_fl": [product_mean_fl],
            "medianpris": [product_median],
            "medianpris_fl": [product_median_fl],
            "antal_produkter":[product_count],
            "antal_produkter_fl":[product_count_fl],
            "saknar_pris":[price_missing]
        }
    )

    print("====LOAD analytics_summary.csv====")
    analytics_file_path = data_folder / "analytics_summary.csv"
    analytics_summary_df.to_csv(analytics_file_path, index=False)

    print("====CALCULATING price analysis====")

    price_analysis_df = validated_df.copy()

    dev_median = price_analysis_df["price"].median()
    price_analysis_df["diff"] = abs(price_analysis_df["price"] - dev_median)
    price_analysis_df["diff_rank"] = price_analysis_df["diff"].rank(ascending=False)
    price_analysis_df["highest_price"] = price_analysis_df["price"].rank(ascending=False)

    price_analysis_df = price_analysis_df.query("diff_rank <= 10 or highest_price <= 10").sort_values("price", ascending=False)

    print("====LOAD price analysis.csv====")
    price_analysis_path = data_folder / "price_analysis.csv"
    price_analysis_df.to_csv(price_analysis_path, index=False)
