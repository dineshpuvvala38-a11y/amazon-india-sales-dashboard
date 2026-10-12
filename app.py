from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(
    page_title="Amazon India Sales Dashboard",
    page_icon="📦",
    layout="wide",
)

st.title("📦 Amazon India Sales & Business Dashboard")
st.caption("Sales • Profitability • Products • Orders • Payments • Fulfilment • Geography")

DATA_PATH = Path(__file__).parent / "data" / "Amazon Sales Data India.xlsx"


@st.cache_data
def load_data():
    data = pd.read_excel(DATA_PATH)
    data["Order_Date"] = pd.to_datetime(data["Order_Date"], errors="coerce")
    text_cols = [
        "Category", "Product", "Payment_Method", "Fulfillment",
        "Order_Status", "Ship_State"
    ]
    for col in text_cols:
        data[col] = data[col].astype("string").str.strip()
    numeric_cols = [
        "Quantity", "Unit_Price_INR", "Discount_Pct",
        "Total_Sales_INR", "Profit_INR"
    ]
    for col in numeric_cols:
        data[col] = pd.to_numeric(data[col], errors="coerce").fillna(0)
    data = data.dropna(subset=["Order_Date", "Order_ID"])
    return data


df = load_data()
min_date = df["Order_Date"].min().date()
max_date = df["Order_Date"].max().date()

with st.sidebar:
    st.header("🔎 Dashboard Filters")
    date_range = st.date_input(
        "Order date range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
    )
    categories = st.multiselect(
        "Category",
        sorted(df["Category"].dropna().unique().tolist()),
        default=sorted(df["Category"].dropna().unique().tolist()),
    )
    states = st.multiselect(
        "Ship state",
        sorted(df["Ship_State"].dropna().unique().tolist()),
        default=sorted(df["Ship_State"].dropna().unique().tolist()),
    )
    statuses = st.multiselect(
        "Order status",
        sorted(df["Order_Status"].dropna().unique().tolist()),
        default=sorted(df["Order_Status"].dropna().unique().tolist()),
    )
    payments = st.multiselect(
        "Payment method",
        sorted(df["Payment_Method"].dropna().unique().tolist()),
        default=sorted(df["Payment_Method"].dropna().unique().tolist()),
    )
    fulfillments = st.multiselect(
        "Fulfilment method",
        sorted(df["Fulfillment"].dropna().unique().tolist()),
        default=sorted(df["Fulfillment"].dropna().unique().tolist()),
    )

if isinstance(date_range, (tuple, list)) and len(date_range) == 2:
    start_date, end_date = date_range
else:
    start_date, end_date = min_date, max_date

filtered = df[
    df["Order_Date"].dt.date.between(start_date, end_date)
    & df["Category"].isin(categories)
    & df["Ship_State"].isin(states)
    & df["Order_Status"].isin(statuses)
    & df["Payment_Method"].isin(payments)
    & df["Fulfillment"].isin(fulfillments)
].copy()

if filtered.empty:
    st.warning("No rows match the selected filters. Change the filters in the sidebar.")
    st.stop()

total_sales = filtered["Total_Sales_INR"].sum()
total_profit = filtered["Profit_INR"].sum()
total_orders = filtered["Order_ID"].nunique()
total_units = filtered["Quantity"].sum()
aov = total_sales / total_orders if total_orders else 0
profit_margin = (total_profit / total_sales * 100) if total_sales else 0
status_counts = filtered.groupby("Order_Status")["Order_ID"].nunique()
returned = int(status_counts.get("Returned", 0))
cancelled = int(status_counts.get("Cancelled", 0))
return_rate = returned / total_orders * 100 if total_orders else 0
cancellation_rate = cancelled / total_orders * 100 if total_orders else 0

def inr(value):
    return f"₹{value:,.0f}"

st.subheader("1. Overall Sales & Profit Performance")
k1, k2, k3, k4, k5, k6 = st.columns(6)
k1.metric("Total Sales", inr(total_sales))
k2.metric("Total Profit", inr(total_profit))
k3.metric("Total Orders", f"{total_orders:,}")
k4.metric("Units Sold", f"{total_units:,.0f}")
k5.metric("Average Order Value", inr(aov))
k6.metric("Profit Margin", f"{profit_margin:.2f}%")

monthly = (
    filtered.assign(Month=filtered["Order_Date"].dt.to_period("M").dt.to_timestamp())
    .groupby("Month", as_index=False)
    .agg(Sales=("Total_Sales_INR", "sum"), Profit=("Profit_INR", "sum"))
)
c1, c2 = st.columns(2)
with c1:
    fig = px.line(monthly, x="Month", y="Sales", markers=True, title="Monthly Sales Trend")
    fig.update_layout(yaxis_title="Sales (INR)", xaxis_title="")
    st.plotly_chart(fig, use_container_width=True)
with c2:
    fig = px.line(monthly, x="Month", y="Profit", markers=True, title="Monthly Profit Trend")
    fig.update_layout(yaxis_title="Profit (INR)", xaxis_title="")
    st.plotly_chart(fig, use_container_width=True)

st.divider()
st.subheader("2. Category & Product Performance")
category_perf = (
    filtered.groupby("Category", as_index=False)
    .agg(Sales=("Total_Sales_INR", "sum"),
         Profit=("Profit_INR", "sum"),
         Units=("Quantity", "sum"))
    .sort_values("Sales", ascending=False)
)
p1, p2 = st.columns(2)
with p1:
    fig = px.bar(category_perf, x="Category", y="Sales", title="Category-wise Sales", text_auto=".2s")
    fig.update_layout(xaxis_title="", yaxis_title="Sales (INR)")
    st.plotly_chart(fig, use_container_width=True)
with p2:
    fig = px.bar(category_perf, x="Category", y="Profit", title="Category-wise Profit", text_auto=".2s")
    fig.update_layout(xaxis_title="", yaxis_title="Profit (INR)")
    st.plotly_chart(fig, use_container_width=True)

fig = px.bar(
    category_perf, x="Category", y="Units",
    title="Category-wise Units Sold", text_auto=".2s"
)
fig.update_layout(xaxis_title="", yaxis_title="Units")
st.plotly_chart(fig, use_container_width=True)

top_products = (
    filtered.groupby("Product", as_index=False)
    .agg(Sales=("Total_Sales_INR", "sum"), Profit=("Profit_INR", "sum"),
         Units=("Quantity", "sum"))
    .sort_values("Sales", ascending=False)
    .head(10)
)
fig = px.bar(
    top_products.sort_values("Sales"),
    x="Sales", y="Product", orientation="h",
    title="Top 10 Products by Sales",
    hover_data=["Profit", "Units"],
    text_auto=".2s",
)
fig.update_layout(xaxis_title="Sales (INR)", yaxis_title="")
st.plotly_chart(fig, use_container_width=True)
st.dataframe(category_perf.style.format({"Sales": "₹{:,.2f}", "Profit": "₹{:,.2f}", "Units": "{:,.0f}"}),
             use_container_width=True, hide_index=True)

st.divider()
st.subheader("3. Order Status & Revenue at Risk")
s1, s2, s3, s4 = st.columns(4)
s1.metric("Delivered Orders", f"{int(status_counts.get('Delivered', 0)):,}")
s2.metric("Shipped Orders", f"{int(status_counts.get('Shipped', 0)):,}")
s3.metric("Returned Orders", f"{returned:,}", f"{return_rate:.2f}% of filtered orders")
s4.metric("Cancelled Orders", f"{cancelled:,}", f"{cancellation_rate:.2f}% of filtered orders")

status_perf = (
    filtered.groupby("Order_Status", as_index=False)
    .agg(Orders=("Order_ID", "nunique"), Sales_Value=("Total_Sales_INR", "sum"))
)
fig = px.pie(status_perf, names="Order_Status", values="Orders",
             title="Order Status Distribution", hole=0.45)
st.plotly_chart(fig, use_container_width=True)

loss_status = filtered[filtered["Order_Status"].isin(["Returned", "Cancelled"])]
if not loss_status.empty:
    loss_category = (
        loss_status.groupby(["Category", "Order_Status"], as_index=False)
        .agg(Orders=("Order_ID", "nunique"), Sales_Value=("Total_Sales_INR", "sum"))
    )
    fig = px.bar(
        loss_category, x="Category", y="Orders", color="Order_Status",
        barmode="group", title="Category-wise Returns & Cancellations"
    )
    fig.update_layout(xaxis_title="", yaxis_title="Orders")
    st.plotly_chart(fig, use_container_width=True)
    at_risk = loss_status["Total_Sales_INR"].sum()
    st.info(
        f"Sales value associated with returned/cancelled rows: {inr(at_risk)}. "
        "This is the recorded order value for those statuses, not a verified accounting loss."
    )
else:
    st.info("No returned or cancelled rows match the current filters.")

st.divider()
st.subheader("4. Payment, Fulfilment & Geographic Performance")
pay_perf = (
    filtered.groupby("Payment_Method", as_index=False)
    .agg(Sales=("Total_Sales_INR", "sum"), Profit=("Profit_INR", "sum"))
)
p1, p2 = st.columns(2)
with p1:
    fig = px.bar(pay_perf, x="Payment_Method", y="Sales", title="Sales by Payment Method", text_auto=".2s")
    fig.update_layout(xaxis_title="", yaxis_title="Sales (INR)")
    st.plotly_chart(fig, use_container_width=True)
with p2:
    fig = px.bar(pay_perf, x="Payment_Method", y="Profit", title="Profit by Payment Method", text_auto=".2s")
    fig.update_layout(xaxis_title="", yaxis_title="Profit (INR)")
    st.plotly_chart(fig, use_container_width=True)

ful_perf = (
    filtered.groupby("Fulfillment", as_index=False)
    .agg(Sales=("Total_Sales_INR", "sum"), Profit=("Profit_INR", "sum"))
)
f1, f2 = st.columns(2)
with f1:
    fig = px.bar(ful_perf, x="Fulfillment", y="Sales", title="Sales by Fulfilment Method", text_auto=".2s")
    fig.update_layout(xaxis_title="", yaxis_title="Sales (INR)")
    st.plotly_chart(fig, use_container_width=True)
with f2:
    fig = px.bar(ful_perf, x="Fulfillment", y="Profit", title="Profit by Fulfilment Method", text_auto=".2s")
    fig.update_layout(xaxis_title="", yaxis_title="Profit (INR)")
    st.plotly_chart(fig, use_container_width=True)

state_perf = (
    filtered.groupby("Ship_State", as_index=False)
    .agg(Sales=("Total_Sales_INR", "sum"), Profit=("Profit_INR", "sum"),
         Orders=("Order_ID", "nunique"))
    .sort_values("Sales", ascending=False)
)
g1, g2 = st.columns(2)
with g1:
    fig = px.bar(state_perf.head(15).sort_values("Sales"), x="Sales", y="Ship_State",
                 orientation="h", title="Top 15 States by Sales", text_auto=".2s")
    fig.update_layout(xaxis_title="Sales (INR)", yaxis_title="")
    st.plotly_chart(fig, use_container_width=True)
with g2:
    fig = px.bar(state_perf.head(15).sort_values("Profit"), x="Profit", y="Ship_State",
                 orientation="h", title="Top 15 States by Profit", text_auto=".2s")
    fig.update_layout(xaxis_title="Profit (INR)", yaxis_title="")
    st.plotly_chart(fig, use_container_width=True)

fig = px.bar(state_perf.head(15).sort_values("Orders"), x="Orders", y="Ship_State",
             orientation="h", title="Top 15 States by Orders", text_auto=".2s")
fig.update_layout(xaxis_title="Orders", yaxis_title="")
st.plotly_chart(fig, use_container_width=True)

with st.expander("View filtered order data"):
    st.dataframe(filtered.sort_values("Order_Date", ascending=False),
                 use_container_width=True, hide_index=True)
    csv = filtered.to_csv(index=False).encode("utf-8")
    st.download_button("Download filtered data as CSV", csv,
                       file_name="amazon_india_filtered_sales.csv", mime="text/csv")

st.caption(
    "Data source: supplied Amazon Sales Data India.xlsx. "
    "This is a portfolio/educational dashboard and is not affiliated with Amazon."
)
