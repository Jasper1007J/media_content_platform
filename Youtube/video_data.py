def get_video_details(youtube, video_ids):
    """
    Retrieves detailed statistics for a list of YouTube video IDs.

    Parameters:
    youtube (googleapiclient.discovery.Resource): An authenticated instance of the YouTube API.
    video_ids (list): A list of YouTube video IDs for which to retrieve statistics.

    Returns:
    list: A list of dictionaries, where each dictionary contains the following keys:
          - Title: The title of the video.
          - Published_date: The date and time when the video was published.
          - Views: The number of views on the video.
          - Likes: The number of likes on the video.
          - Categories: The category ID of the video.
          - Comments: The number of comments on the video.
    """
    all_video_stats = []

    for i in range(0, len(video_ids), 50):  # YouTube API allows max 50 videos per request
        request = youtube.videos().list(
            part="snippet,statistics",
            id=",".join(video_ids[i:i+50])
        )
        response = request.execute()

        for video in response.get("items", []):  # Prevent KeyError if 'items' is missing
            video_stats = dict(
                Title=video["snippet"]["title"],
                Published_date=video["snippet"]["publishedAt"],
                Views=video["statistics"].get("viewCount", 0),  # .get() to handle missing data
                Likes=video["statistics"].get("likeCount", 0),
                Categories = video["snippet"]["categoryId"],
                Comments=video["statistics"].get("commentCount", 0)  # Removed 'dislikeCount'
            )
            all_video_stats.append(video_stats)

    return all_video_stats
