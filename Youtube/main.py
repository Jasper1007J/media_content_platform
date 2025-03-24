

from googleapiclient.discovery import build
from dotenv import load_dotenv
import os
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
import channel_stats
import video_ids
import video_data
import category_extraction

#access the data from the dotenv file
load_dotenv()

# setting up the youtube API key to access the channels
API_KEY = os.getenv("API_KEY")
youtube = build('youtube', 'v3', developerKey=API_KEY)
# this creates a connection to youtube API v3


channel_ids = [" UCq-Fj5jknLsUf-MWSy4_brA", #Tseris
               "UCupvZG-5ko_eiXAupbDfxWw", #Cnn
               "UCvC4D8onUfXzvjTOM-dBfEA", #Marvel
               "UCMiJRAwDNSNzuYeN2uWa0pA", #Techchannel
               "UCYPvAwZP8pZhSMW8qs7cVCw", #India Today
               "UCb-xXZ7ltTvrh9C6DgB9H-Q", #Prasd Tech in telugu
               "UCBi2mrWuNuyYy4gbM6fU18Q", #ABC NEws
               "UCnQC_G5Xsjhp9fEJKuIcrSw", #Benshapiro
               "UCXuqSBlHAE6Xw-yeJA0Tunw", #LinusTech
               "UCsTcErHg8oDvUnTzoqsYeNw", #Unboxtheropy
               "UCOmcA3f_RrH6b9NmcNa4tdg", #CNET
               "UCOpcACMWblDls9Z6GERVi1A", #Screen Junkies
               "UCVtL1edhT8qqY-j2JIndMzg", #CineFix
               "UCLXo7UDZvByw2ixzpQCufnA", #Vox
               "UCvJJ_dzjViJCoLf5uKUTwoA", #CNBC
               "CoUxsWakJucWg46KW5RsvPw",  #Financial
               "UCX6b17PVsYBQ0ip5gyeme-Q", #CrashCourse
               "UC4a-Gbdw7vOaccHmFo40b9g", #Khan Academy
               "UCsooa4yRKGN_zEE8iknghZA", #Ted-ed
               "UCq2E1mIwUKMWzCA4liA_XGQ", #PickUpLimes
               "UCJ24N4O0bP7LGLBDvye7oCA", #Matt
               "UCSPYNpQ2fHv9HJ-q6MIMaPw", #Financialdiet
               "UCFKE7WVJfvaHW5q283SxchA", #Yoga with Adriene
              ]


# Calling the function to get the channel statistics 
channel_statistics = channel_stats.get_channel_stats(youtube, channel_ids)

# Storing the data in a pandas dataframe
channel_data = pd.DataFrame(channel_statistics)

# print(channel_data)


video_ids = video_ids.get_video_ids(youtube, channel_data)

video_data = pd.DataFrame(video_data.get_video_details(youtube, video_ids))
# print(video_data.head())

video_data["Category_id"] , video_data["Categories"] = category_extraction.category_extract(video_data,youtube)


change_date = []

for data in video_data['Published_date']:
    data = datetime.strptime(str(data), "%Y-%m-%dT%H:%M:%SZ").strftime('%Y-%m-%d')
    video_data['Published_date'] = data


video_data['Source'] = 'YoutubeAPI'
video_data["Title_id"] = video_data["Title"].factorize()[0] 

video_data.to_csv('./datasets/youtube_data.csv',index=False)

print(video_data.head())