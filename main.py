from pathlib import Path
import pandas as pd
from utils import cleaning, flagg, Evaluate, analytics_summary, price_analysis

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

    # products_df = products_raw_df.copy()

    cleaned_df = cleaning(products_raw_df)

    print("====FLAGG ERRORS====")
    
    flagged_df = flagg(cleaned_df)

    print("====LOAD rejected_products.csv====")
    evaluate = Evaluate(flagged_df)

    rejected_df = evaluate.rejection()
    rejects_file_path = data_folder / "rejected_products.csv"
    rejected_df.to_csv(rejects_file_path, index=False)

    print("====LOAD validated_products.csv====")
    validated_df = evaluate.validation()
    validated_file_path = data_folder / "validated_products.csv"
    validated_df.to_csv(validated_file_path, index=False)

    print("====LOAD analytics_summary.csv====")
    analytics_summary_df = analytics_summary(validated_df, rejected_df)
    analytics_file_path = data_folder / "analytics_summary.csv"
    analytics_summary_df.to_csv(analytics_file_path, index=False)

    print("====LOAD price analysis.csv====")
    price_analysis_df = price_analysis(validated_df)
    price_analysis_path = data_folder / "price_analysis.csv"
    price_analysis_df.to_csv(price_analysis_path, index=False)
