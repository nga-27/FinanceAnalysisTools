# FinanceAnalysisTools
Analysis software for analyzing one's finances and portfolio management.

## Type of Finance Files
`.xlsx` and `.csv` currently supported

## How to Use:
1. Copy and save `config_example.json` as `config.json`. Fill out appropriately.
2. Copy and save `SimplifiedFinances_example.xlsx` as `SimplifiedFinances.xlsx`, fill out, and enter title into `config.json`.
3. Run `python app.py`.
4. View output folder for created content. (Currently outputs `finances_output.xlsx`)

## Supported Tasks / Features (ver. added)
* "Tabular Stats" (0.0.1) - Gains/Losses, YTD Return, Total Return

## Miscellaneous
### SimplifiedFinances.xlsx

A workbook with spreadsheets to organize financial accounting of funds. Frequency of indexes is up to user, with fixed intervals not required.
This is meant to be interactive - this software is primarily meant to derive content and insights from this spreadsheet. The user can group
their funds into any number of groups desired (e.g. "HSA", "401k", "Stocks", "Cash", etc.). Each "total" column should be the sum of that particular
grouping. The "Grand Total" column should be the sum of the grouped columns.

Tabs on this spreadsheet required are "Amount", "Qty", and "Contributions" - order does not matter, but they must be present.
