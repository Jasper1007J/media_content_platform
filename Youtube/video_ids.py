def get_video_ids(youtube,channel_data):
    video_ids = []

# Getting the video ids from the channel's upload playlist
    for channel_id in channel_data['playlist_id']:
        request = youtube.playlistItems().list(
                            part='snippet',
                            playlistId = channel_id,
                            maxResults = 50
                            )
        response = request.execute()
            
        for i in range(len(response['items'])):
            video_ids.append(response['items'][i]['snippet']['resourceId']['videoId']) #appending the video ids to the list
    
    return video_ids