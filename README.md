# Lab - Data Ingestion, manipulation & workflow
In this Lab the task was to load a csv file into a Pandas DataFrame and clean the data. Then we would reject data that was impossible and flag data that was uncertain. Then we would export the data in csv format. The files we would get were
- [analytics_summary.csv](./data/analytics_summary.csv)
- [price_analysis.csv](./data/price_analysis.csv)
- [rejected_products.csv](./data/rejected_products.csv)

Apart from these, I also created
- [validated_products.csv](./data/validated_products.csv)

Since I am something of an excel fan, I couldn't help but create an excel file that contained all these reports as
- [finalreport.xlsx](./data/finalreport.xlsx)finalreport.xlsx

## Installation
1. Clone the repo
    ```bash
    git clone https://github.com/RikardOledal/DataPlatform_DE25_LAB1_Rikard_Oledal.git
    ```

2. Install dependencies:
    With uv:
    ```bash
    uv sync
    ```
3. Remove created files:
    ```bash
    py restart.py
    ```

4. Run program:
    ```bash
    py main.py
    ```
## Transformation


Flagg
tekniskt giltig
misstänkt lågt värde
kan vara korrekt (kampanj, fel, bulk)

Reject
obligatoriskt fält saknas (currency)
datan kan inte användas alls
Omöjliga värden
Ingen identitet

Reject
missing_id 
missing_price
non_positive_price
missing_currency

Flagg
missing_name
to_high_price
missing_create_date