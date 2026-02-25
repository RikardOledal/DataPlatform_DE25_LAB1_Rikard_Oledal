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
    unflagged["negative_price"] = unflagged["price"] < 0
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
            self.flaggdata["missing_id"]|
            self.flaggdata["missing_price"]|
            self.flaggdata["negative_price"]|
            self.flaggdata["missing_currency"]
        )


    
    def rejection(self) -> pd.DataFrame:
        rejected = self.flaggdata[self.rejects_condition].copy()

        # Create reject_code and reject_reason 
        rejected["reject_code"] = ""
        rejected["reject_reason"] = ""

        # Sums all error-columns row by row
        error_columns = ["missing_id", "negative_price", "missing_currency", "missing_price"]
        rejected["error_count"] = rejected[error_columns].sum(axis=1)

        # Update reject_code and reject_reason  
        rejected.loc[rejected["missing_id"], ["reject_code", "reject_reason"]] = ["31", "Missing ID"]
        rejected.loc[rejected["missing_currency"], ["reject_code", "reject_reason"]] = ["32", "Missing currency"]
        rejected.loc[rejected["negative_price"], ["reject_code", "reject_reason"]] = ["33", "Price is negative"]
        rejected.loc[rejected["missing_price"], ["reject_code", "reject_reason"]] = ["34", "Missing price"]
        rejected.loc[rejected["error_count"] > 1, ["reject_code", "reject_reason"]] = ["39", "Multiple reasons"]

        # Remove Columns
        cols_to_remove_rej = ["missing_name","to_low_price","to_high_price","missing_create_date","error_count"]
        rejected = rejected.drop(columns=cols_to_remove_rej)
                                                                                                                                                    
        return rejected

    def validation(self):
        validated = self.flaggdata[~self.rejects_condition].copy()
        
        validated["status_code"] = "10"
        validated["status_reason"] = "Validated"

        # Sums all error-columns row by row
        error_columns = ["missing_name", "missing_create_date", "to_high_price", "to_low_price"]
        validated["error_count"] = validated[error_columns].sum(axis=1)

        validated.loc[validated["missing_name"], ["status_code", "status_reason"]] = ["21", "Flagged: Missing name"]
        validated.loc[validated["missing_create_date"], ["status_code", "status_reason"]] = ["22", "Flagged: Missing Create-date"]
        validated.loc[validated["to_high_price"], ["status_code", "status_reason"]] = ["23", "Flagged: Price over 10_000"]
        validated.loc[validated["to_low_price"], ["status_code", "status_reason"]] = ["24", "Flagged: Price under 6"]
        validated.loc[validated["error_count"] > 1, ["status_code", "status_reason"]] = ["29", "Multiple reasons"]

        # Remove Columns 
        cols_to_remove_flg = ["missing_id","missing_price", "negative_price","missing_currency","error_count"]
        validated = validated.drop(columns=cols_to_remove_flg)

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

