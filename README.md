# Amazon India Sales & Business Dashboard

A GitHub-ready, interactive sales analytics dashboard built with **Python, Pandas, Streamlit, Plotly, and Excel**.

The dashboard follows the business requirements in `Amazon India Dashboard Sapphire IQ.pdf` and uses the supplied `Amazon Sales Data India.xlsx` dataset.

## Dashboard features

- KPI cards: total sales, total profit, orders, units sold, average order value, and profit margin.
- Monthly sales and profit trends.
- Category-wise sales, profit, and units sold.
- Top 10 products by sales.
- Delivered, shipped, returned, and cancelled order counts.
- Return rate and cancellation rate.
- Category-wise returns and cancellations.
- Sales and profit by payment method.
- Sales and profit by fulfilment method.
- State-wise sales, profit, and orders.
- Interactive filters for date, category, state, order status, payment method, and fulfilment.
- Filtered-data table and CSV download.

## Dataset

The project includes the supplied Excel dataset at:

`data/Amazon Sales Data India.xlsx`

The dataset contains 10,000 rows and 13 columns. Its order dates range from 2024-01-01 through 2026-08-30.

## Run locally

### 1. Install Python

Use Python 3.10 or newer. During installation on Windows, enable **Add Python to PATH** if available.

### 2. Open the project folder

Open a terminal or PowerShell inside this folder.

### 3. Create and activate a virtual environment (recommended)

**Windows PowerShell**
```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If `py` is not recognized, try:
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 4. Install dependencies
```powershell
python -m pip install -r requirements.txt
```

### 5. Start the dashboard
```powershell
python -m streamlit run app.py
```

Streamlit will print a local URL, usually `http://localhost:8501`. Open it in your browser.

## Upload to GitHub

1. Extract the ZIP file.
2. Create a new repository on GitHub, for example `amazon-india-sales-dashboard`.
3. Upload the extracted project files/folders, keeping the `data` folder intact.
4. Commit the files.
5. To run it on another computer, follow the local setup steps above.

Do not upload `.venv` or other environment folders. They are excluded by `.gitignore`.

## Deploy online (optional)

You can deploy this repository using Streamlit Community Cloud:
1. Push the project to GitHub.
2. Open Streamlit Community Cloud and connect your GitHub account.
3. Select the repository and `app.py` as the main file.
4. Deploy.

The Excel file is included in this repository, so keep the path and filename unchanged.

## KPI definitions

- **Total Sales:** sum of `Total_Sales_INR` for filtered rows.
- **Total Profit:** sum of `Profit_INR` for filtered rows.
- **Total Orders:** distinct `Order_ID` count.
- **Units Sold:** sum of `Quantity`.
- **Average Order Value:** total sales divided by distinct orders.
- **Profit Margin:** total profit divided by total sales, multiplied by 100.
- **Return Rate:** returned orders divided by filtered orders, multiplied by 100.
- **Cancellation Rate:** cancelled orders divided by filtered orders, multiplied by 100.

Rates use the current filter selection. If the order-status filter excludes Returned or Cancelled, the corresponding rate will be zero for that selection.

**Interpretation note:** the value associated with returned/cancelled rows is displayed as an indicative order value, not a confirmed financial loss.

## Project structure

```text
amazon-india-sales-dashboard/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── Amazon India Dashboard Sapphire IQ.pdf
└── data/
    └── Amazon Sales Data India.xlsx
```

## Technologies

- Python
- Pandas
- Streamlit
- Plotly
- Excel / XLSX

## Disclaimer

This is an educational portfolio project based on the supplied dataset. It is not affiliated with Amazon and does not use live Amazon systems or live sales data.
