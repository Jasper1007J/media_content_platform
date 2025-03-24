import pandas as pd
def category_extract(video_data,youtube):
    categories = video_data['Categories']

    category_data = []
    for i in categories:
        request = youtube.videoCategories().list(
        part = 'snippet',
        id = i
    )

        response = request.execute()
        
        for vid in response.get('items',[]):
            category_data.append(vid['snippet']['title'])
    categories_column = pd.DataFrame(category_data)

    return categories, categories_column