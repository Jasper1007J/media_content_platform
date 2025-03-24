import Youtube.main as youtube
import Kaggle.main as kaggle
import pandas as pd 

youtube_data = youtube.video_data

kaggle_data = kaggle.kaggle_data

merged_data = pd.concat([youtube_data, kaggle_data], ignore_index=False)

merged_data["Title_id"] = merged_data["Title"].factorize()[0]


merged_data.to_csv('./data_sets/merged_data.csv', index=False)

print(merged_data.head())


# Filling the null values
merged_data["Views"] = merged_data["Views"].transform(lambda x: x.fillna(x.mean()))
merged_data["Likes"] = merged_data["Likes"].transform(lambda x: x.fillna(x.mean()))
merged_data["Comments"] = merged_data["Comments"].transform(lambda x: x.fillna(x.mean()))

# Converting into INT
merged_data['Views'] = merged_data['Views'].fillna(0).astype(int)

merged_data['Likes'] = merged_data['Likes'].fillna(0).astype(int)

merged_data['Comments'] = merged_data['Comments'].fillna(0).astype(int)


merged_data = merged_data.drop_duplicates(inplace=True)

merged_data = merged_data[merged_data["Categories"]]