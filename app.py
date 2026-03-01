import streamlit as st
import pandas as pd
import numpy as np

# Page config
st.set_page_config(page_title="Superstore Dashboard", layout="wide")

# Load Data
@st.cache_data
def load_data():
    # return pd.read_csv("dataset/cleaned_superstore.csv")
    return pd.read_csv("dataset/processed/cleaned_superstore_data.csv")

df = load_data()

st.title("📊 Superstore Sales Dashboard")
st.markdown("Interactive Sales & Profit Analysis")

# KPIs
# total_sales = df["Sales"].sum()
# total_profit = df["Profit"].sum()
# total_orders = df["Order ID"].nunique()
# total_customers = df["Customer ID"].nunique()

# col1, col2, col3, col4 = st.columns(4)

# col1.metric("Total Sales", f"${total_sales:,.0f}")
# col2.metric("Total Profit", f"${total_profit:,.0f}")
# col3.metric("Total Orders", total_orders)
# col4.metric("Total Customers", total_customers)

# st.divider()
# Apply filter first
st.sidebar.header("Filter Options")

region = st.sidebar.selectbox("Select Region", ["All"] + list(df["Region"].unique()))

filtered_df = df.copy()

if region != "All":
    filtered_df = df[df["Region"] == region]

# KPIs based on filtered data
total_sales = filtered_df["Sales"].sum()
total_profit = filtered_df["Profit"].sum()
total_orders = filtered_df["Order ID"].nunique()
total_customers = filtered_df["Customer ID"].nunique()

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Sales", f"${total_sales:,.0f}")
col2.metric("Total Profit", f"${total_profit:,.0f}")
col3.metric("Total Orders", total_orders)
col4.metric("Total Customers", total_customers)

#monthly sales
st.subheader("Monthly Sales Trend")

filtered_df["Order Date"] = pd.to_datetime(filtered_df["Order Date"])
monthly_sales = (
    filtered_df
    .groupby(filtered_df["Order Date"].dt.to_period("M"))["Sales"]
    .sum()
)

st.line_chart(monthly_sales)

#add profit margin KPI
profit_margin = (total_profit / total_sales) * 100 if total_sales != 0 else 0

st.metric("Profit Margin (%)", f"{profit_margin:.2f}%")

#improve chart
col1, col2 = st.columns(2)

with col1:
    st.subheader("Sales by Category")
    category_sales = filtered_df.groupby("Category")["Sales"].sum()
    st.bar_chart(category_sales)

with col2:
    st.subheader("Profit by Region")
    region_profit = filtered_df.groupby("Region")["Profit"].sum()
    st.bar_chart(region_profit)


#add top 10 products
st.subheader("Top 10 Products by Sales")

top_products = (
    filtered_df.groupby("Product Name")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

st.bar_chart(top_products)

