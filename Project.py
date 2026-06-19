import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Page Configuration
st.set_page_config(page_title="Company Financial Dashboard", layout="wide")
st.title("📊 Company Financial Performance Dashboard")
st.markdown("Real-time analysis of company revenue, expenses, and key financial metrics.")

# 2. Sample Dataset (Fallback automatically if excel not created yet)
@st.cache_data
def load_data():
    data = {
        "Month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
        "Revenue": [50000, 60000, 55000, 70000, 85000, 90000],
        "Expenses": [35000, 38000, 40000, 42000, 45000, 48000],
        "Net_Profit": [15000, 22000, 15000, 28000, 40000, 42000],
        "CAC": [120, 115, 130, 110, 105, 100],
        "ROI": [15, 18, 12, 22, 25, 28]
    }
    return pd.DataFrame(data)

df = load_data()

# 3. Sidebar Filters
st.sidebar.header("Filter Options")
selected_months = st.sidebar.multiselect("Select Months:", options=df["Month"].unique(), default=df["Month"].unique())

# Filter data based on selection
filtered_df = df[df["Month"].isin(selected_months)]

# 4. Top KPI Metrics
total_revenue = filtered_df["Revenue"].sum()
total_expenses = filtered_df["Expenses"].sum()
total_profit = filtered_df["Net_Profit"].sum()

col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="Total Revenue ($)", value=f"{total_revenue:,}")
with col2:
    st.metric(label="Total Expenses ($)", value=f"{total_expenses:,}")
with col3:
    st.metric(label="Net Profit ($)", value=f"{total_profit:,}")

st.markdown("---")

# 5. Charts and Visualizations
chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.subheader("Revenue vs Expenses Trend")
    fig_trend = px.line(filtered_df, x="Month", y=["Revenue", "Expenses"], markers=True)
    st.plotly_chart(fig_trend, use_container_width=True)

with chart_col2:
    st.subheader("Net Profit Breakdown")
    fig_profit = px.bar(filtered_df, x="Month", y="Net_Profit", text_auto='.2s', color="Net_Profit")
    st.plotly_chart(fig_profit, use_container_width=True)

# 6. Data Table View
st.markdown("---")
st.subheader("Raw Financial Data View")
st.dataframe(filtered_df, use_container_width=True)


df.to_excel("financial_data.xlsx", index=False)

