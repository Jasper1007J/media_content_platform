

def get_channel_stats(youtube, channel_ids):
    """
    This function retrieves channel statistics from the YouTube API.

    Parameters:
    youtube (googleapiclient.discovery.Resource): An authenticated instance of the YouTube API.
    channel_ids (list): A list of YouTube channel IDs for which to retrieve statistics.
    Returns:
    list: A list of dictionaries, where each dictionary contains the following keys:
          - Channel_name: The name of the YouTube channel.
          - Subscribers: The number of subscribers to the channel.
          - Views: The total number of views on the channel.
          - Total_videos: The total number of videos uploaded to the channel.
          - playlist_id: The ID of the channel's upload playlist.
    """
    all_data = []
    request = youtube.channels().list(
                part='snippet,contentDetails,statistics',
                id=','.join(channel_ids))
    response = request.execute() 

    for i in range(len(response['items'])):
        data = dict(Channel_name = response['items'][i]['snippet']['title'],
                    Subscribers = response['items'][i]['statistics']['subscriberCount'],
                    Views = response['items'][i]['statistics']['viewCount'],
                    Total_videos = response['items'][i]['statistics']['videoCount'],
                    playlist_id = response['items'][i]['contentDetails']['relatedPlaylists']['uploads'])
        all_data.append(data)

    return all_data


