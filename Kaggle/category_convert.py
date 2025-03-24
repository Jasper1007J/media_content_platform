def convert_categories(kaggle_data,):
        category_mapping = {
        "U.S. NEWS": "News & Politics",
        "WORLD NEWS": "News & Politics",
        "POLITICS": "News & Politics",
        "WEIRD NEWS":"News & Politics",
        "CRIME":"News & Politics",
        "COMEDY": "Entertainment",
        "MEDIA":"Entertainment",
        "ENTERTAINMENT": "Entertainment",
        "ARTS & CULTURE": "Entertainment",
        "HOME & LIVING":"People & Blogs",
        "WOMEN":"People & Blogs",
        "PARENTING": "People & Blogs",
        "EDUCATION": "Education",
        "STYLE & BEAUTY": "Howto & Style",
        "SPORTS": "Health & Sports",
        "HEALTHY LIVING": "Health & Sports",
        "WELLNESS": "Health & Sports",
        "FOOD & DRINK": "People & Blogs",
        "BUSINESS": "Business",
        "MONEY": "Business",
        "SCIENCE": "Science & Technology",
        "TRAVEL":"Travel & Events",
        "ENVIRONMENT": "Travel & Events",
        "TECHNOLOGY": "Science & Technology",
        "TECH": "Science & Technology"
    }

    # Apply the category mapping
        kaggle_data["Categories"] = kaggle_data["Categories"].map(category_mapping).fillna("Others")



    # remvoving the data with others category mapping 
        kaggle_data = kaggle_data[kaggle_data["Categories"] != "Others"]


        category_counts = kaggle_data["Categories"].value_counts()
        return kaggle_data


