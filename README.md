# Lab - Data Ingestion, manipulation & workflow
In this Lab the task was to load a csv file into a Pandas DataFrame and clean the data. Then we would reject data that was impossible and flag data that was uncertain. Then we would export the data in csv format.

If you want to know more about the lab. Here is the PDF.
[Lab_instructions (PDF)](./img/Data_Platform_Lab_1.pdf)

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

3. Run program:
    ```bash
    py main.py
    ```
## Transformation
Transformation is when we take the data and clean up obvious errors, reject what you can't use, and flag what we think we need more information about. Since all columns start as strings, we start with some string cleaning.

### String cleaning
String cleaning is good for replacing characters you know are wrong, such as / to - in dates or if you've slipped a kr into the price column. It's also just for handling whitespaces where you know they shouldn't be.

I cleaned the data by
- Removing whitespaces
- Replace 2 or mor whitespaces whith 1 space
- Change format to Upper, Lower or Title
- Changing typeformat on Date and Price

### Data Type Conversion
After string cleaning, I do a Data Type Conversion on price (to Number) and date (to Date). This will replace values ​​that cannot be replaced with Not Available (N/A)

### Identify problems
After that, I flag all the flaws.
- Missing id
- Missing name
- Missing price
- Missing currency
- Missing create_date
- Negative price
- Too low price
- Too high price

### Flagging or Rejecting
This was a difficult trade-off because I didn't have a Stakeholder to consult with. It meant that you still had to assume certain conditions. The idea is that anything that makes it impossible to use the data or identify it is rejected, while the rest is flagged as wanting clarification, but you can count on it.

I rejected these
- Missing id: Without id we can't identify the row.
- Missing price: Without price we can't calculate it.
- Negative price: A price can't be negative and should therefore be rejected
- Missing currency: Missing currency means we don't know how much it will be. It varies a lot between different currencies

I kept these, but flagged them up to see if they were correct.
- Missing name: As long as we have an id on the row, we should be able to get this out. It is not critical as most things will be calculated on price. However, it could be misleading if you want to know the average for e.g. a jacket.
- Missing create_date: As long as we have an id on the row, we should be able to get this out. It is not critical as most things will be calculated on price. However, it could be misleading if you want to know the average for e.g. June.
- Too low price: I thought it was worth flagging up everything that has a price of 0-5 SEK to see if this is really true.
- Too high price: I thought it was worth flagging up everything that has a price of 10,000 SEK or more to see if this is really true.

I also made att codestucture
| Code | Reason | Type |
|:-------:|:-------:|--------|
| 10 | Validated | OK |
| 21-24 | Warnings | Flagged |
| 31-34 | Critical Errors | Rejected |


## The reports
- [analytics_summary.csv](./img/analytics_summary.csv)
In this one, I choose to include both flagged and unflagged data to see how they differed from each other.

- [price_analysis.csv](./img/price_analysis.csv)
In this case, I used Rank to sort out relevant values. To calculate the most deviating price, I used the difference between the median and the price to run Rank against.

- [rejected_products.csv](./img/rejected_products.csv)
- [validated_products.csv](./img/validated_products.csv)
- [finalreport.xlsx](./img/finalreport.xlsx)
In the assignment we were only supposed to produce rejected_products.csv, but since I had validated as well and since I am a fan of Excel, I also made a validated_products.csv and an Excel that puts everything together into a file with a sheet for each csv.

## Work process
This project follows the ETL (Extract, Transform, Load) workflow:
- Extract: Loading raw data from CSV using Pandas.
- Transform: String cleaning, type conversion, and flagging/rejecting data based on quality rules.
- Load: Exporting processed data back to CSV and Excel formats.

I worked in a [Jupyter Notebook](sandbox.ipynb) to test that everything works as it should. In this you can also see the flow and some comments about each part.
Then I moved the code to main.py and saw that it worked there. To keep my code DRY, I used utils.py to hold my functions.
I coded everything myself, but have had discussions in my study group with Anja Scherwall and Felix Kjellberg. I used [Pandas docs][1] for explanations of methods and functions. Google Gemini helped me with troubleshooting when I got stuck.

[1]: https://pandas.pydata.org/docs/reference/frame.html