import streamlit as st
import mysql.connector
import pandas as pd
import plotly.express as px

# Database Connection
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Jasper@1007",
        database="youtube"
    )

# Fetch Data from MySQL
def fetch_data():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # Query fact_data with joins
    query = """
        SELECT f.Title, f.Source, d.Date, d.Day, d.Month, d.Year, d.Week, 
               c.Categories, e.Views, e.Likes, e.Comments, e.Engagement_rate
        FROM fact_data f
        JOIN date d ON f.Date_id = d.Date_id
        JOIN category c ON f.Category_id = c.Category_id
        JOIN engagement e ON f.Engagement_id = e.Engagement_id
        ORDER BY d.Date DESC;
    """
    
    cursor.execute(query)
    data = cursor.fetchall()
    conn.close()
    
    return pd.DataFrame(data)

# Load Data
df = fetch_data()

# 🎨 Streamlit UI
st.set_page_config(page_title="YouTube Data Dashboard", layout="wide")
st.title("📊 YouTube Data Analytics Dashboard")

# Sidebar Filters
st.sidebar.header("🔍 Filter Data")
category_filter = st.sidebar.multiselect("Select Category", df["Categories"].unique())
month_filter = st.sidebar.multiselect("Select Month", df["Month"].unique())

# Apply Filters
if category_filter:
    df = df[df["Categories"].isin(category_filter)]
if month_filter:
    df = df[df["Month"].isin(month_filter)]

# Display Data
st.subheader("📄 Data Preview")
st.dataframe(df)

# 📊 Visualization 1: Views by Category
fig1 = px.bar(df, x="Categories", y="Views", color="Categories", title="Total Views per Category")
st.plotly_chart(fig1, use_container_width=True)

# 📈 Visualization 2: Engagement Rate Over Time
fig2 = px.line(df, x="Date", y="Engagement_rate", title="Engagement Rate Trend")
st.plotly_chart(fig2, use_container_width=True)

# 📌 Visualization 3: Likes vs Comments Scatter Plot
fig3 = px.scatter(df, x="Likes", y="Comments", color="Categories", size="Views",
                  title="Likes vs Comments (Bubble Chart)")
st.plotly_chart(fig3, use_container_width=True)

st.sidebar.markdown("---")
st.sidebar.write("📌 Built with ❤️ using Streamlit")

