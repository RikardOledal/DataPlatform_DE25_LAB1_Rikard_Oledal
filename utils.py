import pandas as pd

def cleaning(uncleandata: pd.DataFrame) -> pd.DataFrame:
    uncleandata["id"] = (
        uncleandata["id"]
        .str.strip()
        .str.replace(r'\s{2,}', ' ', regex=True)
        .str.replace(" ", "")
        .str.upper()
    )

    uncleandata["name"] = (
        uncleandata["name"]
        .str.strip()
        .str.title()
        .str.replace(r'\s{2,}', ' ', regex=True)
    )

    uncleandata["price"] = (
        uncleandata["price"]
        .str.strip()
        .str.lower()
        .str.replace(r'\s{2,}', ' ', regex=True)
        .str.replace(" ", "")
        .str.replace("kr", "")
        .str.replace("sek", "")
    )

    uncleandata["currency"] = (
        uncleandata["currency"]
        .str.strip()
        .str.replace(r'\s{2,}', ' ', regex=True)
        .str.replace(" ", "")
        .str.upper()
    )

    uncleandata["created_at"] = (
        uncleandata["created_at"]
        .str.strip()
        .str.replace("/", "-")
    )

    # Converting Datatypes
    uncleandata["price"] = pd.to_numeric(uncleandata["price"], errors="coerce")
    uncleandata["created_at"] = pd.to_datetime(uncleandata["created_at"], errors="coerce")

    cleandata = uncleandata

    return cleandata

def flagg(unflagged:pd.DataFrame) -> pd.DataFrame:
    unflagged["missing_id"] = unflagged["id"].isna()
    unflagged["missing_name"] = unflagged["name"].isna()
    unflagged["missing_price"] = unflagged["price"].isna()
    unflagged["negative price"] = unflagged["price"] < 0
    unflagged["to_low_price"] = unflagged["price"].between(0,5)
    unflagged["to_high_price"] = unflagged["price"] >= 10000
    unflagged["missing_currency"] = unflagged["currency"].isna()
    unflagged["missing_create_date"] = unflagged["created_at"].isna()

    flagged = unflagged

    return flagged

class Evaluate():
    """
    Handles the evaluation of flagged product data by separating it into 
    validated rows and rejected rows.

    The class identifies rows that do not meet minimum data quality requirements 
    and assigns specific status codes and descriptions for both approved 
    and rejected data.

    Attributes:
        flaggdata (pd.DataFrame): The input DataFrame containing original data 
            alongside boolean flag columns.
        rejects_condition (pd.Series): A boolean mask defining rows to be rejected 
            (missing ID, price, currency, or negative price).
        cols_to_remove (list): A list of helper/flag columns to be dropped 
            before returning the results.
    """
    def __init__(self, flaggdata):
        self.flaggdata = flaggdata
        self.rejects_condition = (
            (self.flaggdata["missing_id"] == True)|
            (self.flaggdata["missing_price"] == True)|
            (self.flaggdata["negative price"] == True)|
            (self.flaggdata["missing_currency"] == True)
        )
        self.cols_to_remove = [
            "missing_id", "missing_name", "missing_price", 
            "negative price", "to_low_price",
            "to_high_price", "missing_currency",
            "missing_create_date"
        ]
    
    def rejection(self) -> pd.DataFrame:
        rejected = self.flaggdata[self.rejects_condition].copy()

        rejected["reject_code"] = ""
        rejected["reject_reason"] = ""

        rejected.loc[rejected["missing_id"] == True, "reject_reason"] = "Missing ID"
        rejected.loc[rejected["missing_id"] == True, "reject_code"] = "31"
        rejected.loc[rejected["missing_currency"] == True, "reject_reason"] = "Missing currency"
        rejected.loc[rejected["missing_currency"] == True, "reject_code"] = "32"
        rejected.loc[rejected["negative price"] == True, "reject_reason"] = "Price is negative"
        rejected.loc[rejected["negative price"] == True, "reject_code"] = "33"
        rejected.loc[rejected["missing_price"] == True, "reject_reason"] = "Missing price"
        rejected.loc[rejected["missing_price"] == True, "reject_code"] = "34"

        rejected = rejected.drop(columns=self.cols_to_remove)

        return rejected

    def validation(self):
        validated = self.flaggdata[~self.rejects_condition].copy()

        validated["status_code"] = "10"
        validated["status_reason"] = "Validated"
    
        validated.loc[validated["missing_name"] == True, "status_code"] = "21"
        validated.loc[validated["missing_name"] == True, "status_reason"] = "Flagged: Missing name"
        validated.loc[validated["missing_create_date"] == True, "status_code"] = "22"
        validated.loc[validated["missing_create_date"] == True, "status_reason"] = "Flagged: Missing Create-date"
        validated.loc[validated["to_high_price"] == True, "status_code"] = "23"
        validated.loc[validated["to_high_price"] == True, "status_reason"] = "Flagged: Price over 10_000"
        validated.loc[validated["to_low_price"] == True, "status_code"] = "24"
        validated.loc[validated["to_low_price"] == True, "status_reason"] = "Flagged: Price under 6"
    
        validated = validated.drop(columns=self.cols_to_remove)

        return validated

def analytics_summary(validdata: pd.DataFrame, rejectdata) -> pd.DataFrame:
    product_mean = validdata.query("status_code == '10'")["price"].mean().round(2)
    product_mean_fl = validdata["price"].mean().round(2)
    product_median = validdata.query("status_code == '10'")["price"].median().round(2)
    product_median_fl = validdata["price"].median().round(2)
    product_count = validdata.query("status_code == '10'")["status_code"].count()
    product_count_fl = validdata["status_code"].count()
    price_missing = rejectdata.query("reject_code == '34'")["reject_code"].count()

    analytics_summary = pd.DataFrame(
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

    return analytics_summary

def price_analysis(validdata: pd.DataFrame) -> pd.DataFrame:
    price_analysis = validdata.copy()

    dev_median = price_analysis["price"].median()
    price_analysis["diff"] = abs(price_analysis["price"] - dev_median)
    price_analysis["diff_rank"] = price_analysis["diff"].rank(ascending=False)
    price_analysis["highest_price"] = price_analysis["price"].rank(ascending=False)

    price_analysis = price_analysis.query("diff_rank <= 10 or highest_price <= 10").sort_values("price", ascending=False)

    return price_analysis

