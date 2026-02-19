from pathlib import Path
import pandas as pd
from utils import cleaning, flagg, Evaluate, analytics_summary, price_analysis

if __name__ == "__main__":
    #Datapaths
    BASE_PATH = Path(__file__).parent
    DATA_FOLDER = BASE_PATH / "data"
    IMPORTFILE_PATH = DATA_FOLDER / "Products_raw.csv"
    REJECTS_FILE_PATH = DATA_FOLDER / "rejected_products.csv"
    VALIDATED_FILE_PATH = DATA_FOLDER / "validated_products.csv"
    ANALYTICS_FILE_PATH = DATA_FOLDER / "analytics_summary.csv"
    PRICE_ANALYS_PATH = DATA_FOLDER / "price_analysis.csv"
    EXCEL_PATH = DATA_FOLDER / "finalreport.xlsx"

    if IMPORTFILE_PATH.exists():
        products_raw_df = pd.read_csv(IMPORTFILE_PATH, delimiter=";")
        print("==== DATA EXTRACTED ====")
    else:
        print(f"Did not find file at: {IMPORTFILE_PATH}")

    print("==== TRANSFORM DATA ====")

    # products_df = products_raw_df.copy()

    cleaned_df = cleaning(products_raw_df)

    print("==== FLAGG ERRORS ====")
    
    flagged_df = flagg(cleaned_df)

    print("==== LOAD rejected_products.csv ====")
    evaluate = Evaluate(flagged_df)

    rejected_df = evaluate.rejection()
    rejected_df.to_csv(REJECTS_FILE_PATH, index=False)

    print("==== LOAD validated_products.csv ====")
    validated_df = evaluate.validation()
    validated_df.to_csv(VALIDATED_FILE_PATH, index=False)

    print("==== LOAD analytics_summary.csv ====")
    analytics_summary_df = analytics_summary(validated_df, rejected_df)
    analytics_summary_df.to_csv(ANALYTICS_FILE_PATH, index=False)

    print("==== LOAD price analysis.csv ====")
    price_analysis_df = price_analysis(validated_df)
    price_analysis_df.to_csv(PRICE_ANALYS_PATH, index=False)
    
    print("==== LOAD finalreport.xlsx ====")
    with pd.ExcelWriter(EXCEL_PATH) as writer:
        analytics_summary_df.to_excel(writer, sheet_name="Analytics_summary", index=False)
        price_analysis_df.to_excel(writer, sheet_name="Price_analysis", index=False)
        validated_df.to_excel(writer, sheet_name="Validated", index=False)
        rejected_df.to_excel(writer, sheet_name="Rejected", index=False)
        
