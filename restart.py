from pathlib import Path

def restart_workspace():
    base_path = Path(__file__).parent
    data_folder = base_path / "data"

    files_to_remove = [
        "analytics_summary.csv",
        "price_analysis.csv",
        "rejected_products.csv",
        "validated_products.csv",
        "finalreport.xlsx"
    ]

    print("==== CLEANING WORKSPACE ====")
    
    deleted_count = 0
    
    for file_name in files_to_remove:
        file_path = data_folder / file_name
        
        if file_path.exists():
            try:
                file_path.unlink()
                print(f"Removed: {file_name}")
                deleted_count += 1
            except Exception as e:
                print(f"Error removing {file_name}: {e}")
        else:
            print(f"Skipped: {file_name} (not found)")

    print(f"==== DONE: {deleted_count} files removed ====")

if __name__ == "__main__":
    restart_workspace()