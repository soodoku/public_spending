## Kentucky Public Spending Data

The spending data (vendor details view which gives date of service, etc.) from 2007--2018 are from https://transparency.ky.gov/Pages/default.aspx

The [python script](kentucky_spending.py) iterates through the search results of `spending search`  to get spending data from 2007 to 2018 (1-12-2018) and creates `kentucky_spending.csv`. The CSV has the following columns `name (for instance, DEPT of CRIMINAL JUSTICE TRAINING, DAVID FARLEY, etc.), date_of_service, year, cabinet, department, classification, item_name, amount`

The data are posted at: http://dx.doi.org/10.7910/DVN/4W9ZN3

### Running the Script

```
pip install -r requirements.txt
python kentucky_spending.py
```