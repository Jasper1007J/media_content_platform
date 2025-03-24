import streamlit as st
import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from dotenv import load_dotenv
import plotly.express as px
import os
import matplotlib.ticker as mtick

# Database Connection
load_dotenv()
@st.cache_resource
def get_connection():
    return mysql.connector.connect(
        host=os.getenv('HOSTNAME'),
        user=os.getenv("USERNAME"),
        password=os.getenv("PASSWORD"),
        database=os.getenv("DATABASE")
    )

# Fetch Data from MySQL
@st.cache_data(ttl=10000)
def fetch_data():
    conn = get_connection()
    query = """
        SELECT f.Title, f.Source, d.Date, d.Day, d.Month, d.Year, d.Week, 
               c.Categories, e.Views, e.Likes, e.Comments, e.Engagement_rate
        FROM fact_data f
        JOIN date d ON f.Date_id = d.Date_id
        JOIN category c ON f.Category_id = c.Category_id
        JOIN engagement e ON f.Engagement_id = e.Engagement_id
        ORDER BY d.Date DESC;
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Load Data
df = fetch_data()

# Sidebar Filters
st.sidebar.header("🔍 Filter the Data")
category_filter = st.sidebar.multiselect("📌 Select Category", df["Categories"].unique())
month_filter = st.sidebar.multiselect("📆 Select Month", df["Month"].unique())
search_query = st.sidebar.text_input("⌛ Search by Title")
date_range = st.sidebar.date_input("📅 Select Date Range", [])

# Apply Filters
if category_filter:
    df = df[df["Categories"].isin(category_filter)]
if month_filter:
    df = df[df["Month"].isin(month_filter)]
if search_query:
    df = df[df["Title"].str.contains(search_query, case=False, na=False)]
if len(date_range) == 2:
    df = df[(df["Date"] >= pd.to_datetime(date_range[0])) & (df["Date"] <= pd.to_datetime(date_range[1]))]

# Navbar for Page Selection
st.markdown("""
    <style>
        .css-18e3th9 { display: flex; justify-content: space-between;}
        .stButton>button { margin: 10px 10px;padding: 10px;background-color:#fefff2 ;border:none;transition: 0.3s}
        .stButton>button:hover { scale:1.1;color:black;background-color:#f7f7cb}
    </style>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
overview_btn = col1.button("🏠 Overview")
category_btn = col2.button("📊 Category Insights")
engagement_btn = col3.button("📈 Engagement Analysis")

# Set page based on button click
if "page" not in st.session_state:
    st.session_state.page = "Overview"

if overview_btn:
    st.session_state.page = "Overview"
elif category_btn:
    st.session_state.page = "Category Insights"
elif engagement_btn:
    st.session_state.page = "Engagement Analysis"

# Function to format y-axis values in Ks
def format_ks(value, _):
    return f"{int(value / 1000)}K"

# Overview Page
if st.session_state.page == "Overview":
    total_views = df["Views"].sum()
    total_likes = df["Likes"].sum()
    avg_views = df["Views"].mean()
    avg_likes = df["Likes"].mean()
    avg_engagement = df["Engagement_rate"].mean()
    
    col1, col2 = st.columns(2)
    col1.metric("👀 Total Views", f"{total_views:,}")
    col2.metric("❤️ Total Likes", f"{total_likes:,}")


    col1, col2, col3 = st.columns(3)
    col1.metric("👀 Avg. Views", f"{avg_views:,.2f}")
    col2.metric("❤️ Avg. Likes", f"{avg_likes:,.2f}")
    col3.metric("💬 Avg. Engagement Rate", f"{avg_engagement:.2f}%")
    
    st.subheader("💾 Data Preview")
    page_size = st.selectbox("📜 Records per Page", [5, 10, 20, 50, 100, 500, 1000, 10000], index=1)
    total_pages = (len(df) // page_size) + 1
    page_number = st.number_input("Page Number", min_value=1, max_value=total_pages, value=1)
    start_idx = (page_number - 1) * page_size
    end_idx = start_idx + page_size
    st.dataframe(df.iloc[start_idx:end_idx], use_container_width=True)

# Category Insights Page
elif st.session_state.page == "Category Insights":
    st.subheader("📊 Views & Likes Analysis")
    
    fig, ax = plt.subplots()
    st.header('BAR PLOT')
    st.text('Shows the total number of views,likes and comments for each category. Each bar represents a specific category, color-coded for easier differentiation.')
    st.info(' Helps to identify the most-watched content categories, providing insight into audience preferences.')
    sns.barplot(data=df, y="Categories", x="Views", ax=ax,palette='viridis')
    ax.xaxis.set_major_formatter(mtick.FuncFormatter(format_ks))
    plt.xticks(rotation=45)
    plt.title("Total Views per Category")
    st.pyplot(fig)
    
    st.info(' Highlights which categories receive the most positive reactions from users, allowing you to measure audience engagement.')
    fig, ax = plt.subplots()
    sns.barplot(data=df, y="Categories", x="Likes", ax=ax,palette = 'coolwarm')
    ax.xaxis.set_major_formatter(mtick.FuncFormatter(format_ks))
    plt.xticks(rotation=45)
    plt.title("Total Likes per Category")
    st.pyplot(fig)

    st.info('Tracks how often users engage via comments, a useful indicator of active participation versus passive viewing.')
    fig, ax = plt.subplots()
    sns.barplot(data=df, y="Categories", x="Comments", ax=ax,palette='Set3')
    ax.xaxis.set_major_formatter(mtick.FuncFormatter(format_ks))
    plt.xticks(rotation=45)
    plt.title("Total Commentss per Category")
    st.pyplot(fig)

    st.header('PARETO CHART')
    st.text('Highlights the categories contributing to the majority of views.')
    df_sorted = df.groupby("Categories")["Views"].sum().sort_values(ascending=False).reset_index()
    df_sorted["Cumulative_Percentage"] = df_sorted["Views"].cumsum() / df_sorted["Views"].sum() * 100
    fig_pareto = px.bar(df_sorted, x="Categories", y="Views", title="Pareto Analysis of Views",color_discrete_sequence=px.colors.sequential.Turbo)
    st.plotly_chart(fig_pareto, use_container_width=True) 

# Engagement Analysis Page
elif st.session_state.page == "Engagement Analysis":

    st.header('PIE CHART')
    st.text('Distributes engagement rates across categories.')
    st.info('Offers a proportional representation of engagement to identify which categories are mostly reacted by users.')
    fig_pie = px.pie(df, names="Categories", values="Engagement_rate", title="Engagement Distribution by Category")
    st.plotly_chart(fig_pie, use_container_width=True)

    st.header("BAR CHART")
    st.text('Total number of views across different days to find the audience behavior.')
    st.info('Helps to identify which days have higher audience activity, enabling strategic timing for new posts or campaigns.')
    fig_views_per_day = px.bar(df, x="Day", y="Views", color="Day", title="Views per Day")
    st.plotly_chart(fig_views_per_day, use_container_width=True)

    st.header('AREA CHART')
    st.text('Shows how views are distributed over time, categorized by color for each category.')
    st.info('Detects trends and seasonality in viewing patterns to aid in planning or content strategy.')
    fig_area = px.area(df, x="Date", y="Views", color="Categories",
                    title="📉 Views Distribution Over Time",range_y=[0, 5e6])
    st.plotly_chart(fig_area, use_container_width=True)
  

    st.header('LINE PLOT')
    st.info('Display how engagement rates fluctuate week by week over a specific time period.')
    fig_engagement_week = px.line(df, x="Week", y="Engagement_rate", color="Categories", title="Engagement Rate Trend by Week",range_y=(0,0.1))
    st.plotly_chart(fig_engagement_week, use_container_width=True)  

    st.header('TREEMAP')
    st.info('Shows how engagement   (likes, comments, etc.) is distributed across different categories.')
    fig_treemap = px.treemap(df, path=["Categories"], values="Engagement_rate", title="Engagement Breakdown by Categories")
    st.plotly_chart(fig_treemap, use_container_width=True)  

st.sidebar.markdown("---")
st.success("END OF THE PAGE")
