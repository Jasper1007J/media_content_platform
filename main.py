
from datetime import datetime 
import pandas as pd 
import numpy as np
import database.data_base_connection as db

youtube_data = pd.read_csv('./data_sets/youtube_data.csv')

kaggle_data = pd.read_csv('./data_sets/kaggle_data.csv')

merged_data = pd.concat([youtube_data, kaggle_data], ignore_index=False)

merged_data["Title_id"] = merged_data["Title"].factorize()[0]


print(merged_data.info())  # Check if it's None



# Filling the null values
# Convert columns to numeric, forcing errors='coerce' to handle non-numeric values
merged_data["Views"] = pd.to_numeric(merged_data["Views"], errors='coerce')
merged_data["Likes"] = pd.to_numeric(merged_data["Likes"], errors='coerce')
merged_data["Comments"] = pd.to_numeric(merged_data["Comments"], errors='coerce')

# Now fill NaN values with the mean
merged_data["Views"] = merged_data["Views"].fillna(merged_data["Views"].mean())
merged_data["Likes"] = merged_data["Likes"].fillna(merged_data["Likes"].mean())
merged_data["Comments"] = merged_data["Comments"].fillna(merged_data["Comments"].mean())

# Converting into INT
merged_data['Views'] = merged_data['Views'].fillna(0).astype(int)

merged_data['Likes'] = merged_data['Likes'].fillna(0).astype(int)

merged_data['Comments'] = merged_data['Comments'].fillna(0).astype(int)


merged_data.drop_duplicates(inplace=True)

merged_data = merged_data[merged_data["Categories"] != 'Others']

merged_data['Engagement_rate'] = (merged_data['Likes'] + merged_data['Comments']) / merged_data['Views']

merged_data['Date'] = pd.to_datetime(merged_data['Published_date'],errors= 'coerce')


merged_data['Week'] = merged_data['Date'].dt.day_name()


merged_data.to_csv('./data_sets/merged_data.csv', index=False)


dim_date = merged_data[['Date', 'Week']].drop_duplicates().reset_index(drop=True)
dim_date['Date_id'] = dim_date.index + 1  # Assign unique ID

# Extract day, month, and year
dim_date["Day"] = dim_date["Date"].dt.day
dim_date["Month"] = dim_date["Date"].dt.month
dim_date["Year"] = dim_date["Date"].dt.year

# Date table creation
dim_date = dim_date[["Date_id","Date","Year","Month","Day","Week"]]



# Engagement Table creation
dim_engagement = merged_data[['Views','Comments','Likes','Engagement_rate']].copy()
dim_engagement.loc[:, 'Engagement_id'] = range(1, len(dim_engagement) + 1)
dim_engagement = dim_engagement[['Engagement_id','Views','Likes','Comments','Engagement_rate']]

# Category Table Creation
dim_cat = merged_data[['Category_id', 'Categories']].drop_duplicates().reset_index(drop=True)


merged_data["Day"] = merged_data["Date"].dt.day
merged_data["Month"] = merged_data["Date"].dt.month
merged_data["Year"] = merged_data["Date"].dt.year


print(merged_data.isna().sum())
print(merged_data['Engagement_rate'].isna().sum())  # Count NaN values
print(merged_data['Engagement_rate'].isnull().sum())  # Alternative NaN check
print((merged_data['Engagement_rate'] == float('inf')).sum())  # Check for infinity
print((merged_data['Engagement_rate'] == float('-inf')).sum())  #

merged_data.dropna(subset = ['Engagement_rate'],inplace= True)
max_finite_value = merged_data[merged_data['Engagement_rate'] != float('inf')]['Engagement_rate'].max()
merged_data['Engagement_rate'].replace([float('inf'), float('-inf')], max_finite_value)

db.db_connect(merged_data)


