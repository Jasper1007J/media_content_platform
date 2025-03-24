import streamlit as st
import mysql.connector
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Database Connection
@st.cache_resource
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Jasper@1007",
        database="media_content"
    )

# Fetch Data from MySQL
@st.cache_data(ttl=1000)
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

# Overview Page with Pagination
if st.session_state.page == "Overview":
    total_views = df["Views"].sum()
    total_likes = df["Likes"].sum()
    avg_engagement = df["Engagement_rate"].mean()
    
    col1, col2, col3 = st.columns(3)
    col1.metric("👀 Total Views", f"{total_views:,}")
    col2.metric("❤️ Total Likes", f"{total_likes:,}")
    col3.metric("💬 Avg. Engagement Rate", f"{avg_engagement:.2f}%")
    
    st.subheader("💾 Data Preview")
    page_size = st.selectbox("📜 Records per Page", [5, 10, 20, 50,100], index=1)
    total_pages = (len(df) // page_size) + 1
    page_number = st.number_input("Page Number", min_value=1, max_value=total_pages, value=1)
    start_idx = (page_number - 1) * page_size
    end_idx = start_idx + page_size
    st.dataframe(df.iloc[start_idx:end_idx], use_container_width=True)
    

# Category Insights Page
elif st.session_state.page == "Category Insights":
    st.subheader("📊 Views & Likes Analysis")
    
    fig1 = px.bar(df, x="Categories", y="Views", color="Categories", title="Total Views per Category")
    st.plotly_chart(fig1, use_container_width=True)
    st.info("The bar graph visualizes the total views for each category")
    
    fig2 = px.bar(df, x="Categories", y="Likes", color="Categories", title="Total Likes per Category")
    st.plotly_chart(fig2, use_container_width=True)
    st.info("The bar graph visualizes the total likes for each category")
    
    fig3 = px.bar(df, x="Categories", y="Comments", color="Categories", title="Total Comments per Category")
    st.plotly_chart(fig3, use_container_width=True)
    st.info("The bar graph visualizes the total comments for each category")

# Engagement Analysis Page
elif st.session_state.page == "Engagement Analysis":
    st.subheader("📈 Engagement Trends")

    fig,ax = plt.subplots()
    sns.countplot(data = df, x = "Week",palette='pastel',alpha=1)
    ax.set_xlabel("Week Of the Day")
    ax.set_ylabel("Count")
    ax.set_title("Total No of the Days News uploaded"   )
    st.pyplot(fig, use_container_width=True)

    fig_pie = px.pie(df, names="Categories", values="Engagement_rate", title="Engagement Distribution by Category")
    st.plotly_chart(fig_pie, use_container_width=True)
    
    fig_line = px.line(df, x="Date", y="Engagement_rate", color="Categories", markers=True,
                       title="Monthly Engagement Rate Trends")
    st.plotly_chart(fig_line, use_container_width=True)
    
    fig_scatter = px.scatter(df, x="Likes", y="Comments", color="Categories", size="Views",
                             title="📌 Likes vs Comments (Bubble Chart)")
    st.plotly_chart(fig_scatter, use_container_width=True)


    fig_area = px.area(df, x="Date", y="Views", color="Categories",
                       title="📉 Views Distribution Over Time",range_y=[0, 6e6])
    st.plotly_chart(fig_area, use_container_width=True)

st.sidebar.markdown("---")
st.success("END OF THE PAGE")
