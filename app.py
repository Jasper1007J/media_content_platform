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
@st.cache_data
def fetch_data():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    
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

# Streamlit UI Configuration
# st.set_page_config(page_title=" Jasper's Media Dashboard", layout="wide")

# Sidebar Filters
st.sidebar.header("🔍 Filter the Data")
category_filter = st.sidebar.multiselect("📌 Select Category", df["Categories"].unique())
month_filter = st.sidebar.multiselect("📆 Select Month", df["Month"].unique())

# Search Bar
search_query = st.sidebar.text_input("⌛ Search by Title")

# Date Range Filter
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

# 📌 **Key Metrics**
total_views = df["Views"].sum()
total_likes = df["Likes"].sum()
avg_engagement = df["Engagement_rate"].mean()

st.markdown("### 🧭 **Media Content Analytics Dashboard**")
col1, col2, col3 = st.columns(3)

col1.metric("👀 Total Views", f"{total_views:,}")
col2.metric("❤️ Total Likes", f"{total_likes:,}")
col3.metric("💬 Avg. Engagement Rate", f"{avg_engagement:.2f}%")

st.divider()

# 📄 **Data Preview**
st.subheader("💾 Data Preview")
st.dataframe(df, use_container_width=True)

# 📊 **Visualizations**
st.subheader("📊 Insights & Analytics")



# 📊 Views by Category
fig1 = px.bar(df, x="Categories", y="Views", color="Categories", title="Total Views per Category")
st.plotly_chart(fig1, use_container_width=True)


fig2 = px.bar(df, x="Categories", y="Likes", color="Categories", title="Total Likes per Category")
st.plotly_chart(fig2, use_container_width=True)



fig3 = px.bar(df, x="Categories", y="Comments", color="Categories", title="Total Comments per Category")
st.plotly_chart(fig3, use_container_width=True)

fig_pie = px.pie(df, names="Categories", values="Engagement_rate", title="Engagement Distribution by Category")
st.plotly_chart(fig_pie, use_container_width=True)


fig_line = px.line(df, x="Date", y="Engagement_rate", color="Categories", markers=True,
                   title="Monthly Engagement Rate Trends")
st.plotly_chart(fig_line, use_container_width=True)


# 📈 Engagement Rate Trend
fig4 = px.line(df, x="Date", y="Engagement_rate", markers=True,
               title="📈 Engagement Rate Over Time", template="plotly_white")
st.plotly_chart(fig4, use_container_width=True)

st.divider()

# 📊 **Additional Visualizations**
st.subheader("🔍 Advanced Insights")



# 📌 Likes vs Comments Scatter Plot
fig3 = px.scatter(df, x="Likes", y="Comments", color="Categories", size="Views",
                  title="📌 Likes vs Comments (Bubble Chart)", template="seaborn")
st.plotly_chart(fig3, use_container_width=True)

# 📉 Views Distribution Over Time
fig4 = px.area(df, x="Date", y="Views", color="Categories",
               title="📉 Views Distribution Over Time", template="plotly_white")
st.plotly_chart(fig4, use_container_width=True)

st.sidebar.markdown("---")

st.success("✅ Data Loaded Successfully!")
