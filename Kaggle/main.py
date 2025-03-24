from kaggle.api.kaggle_api_extended import KaggleApi
import pandas as pd
import Kaggle.category_convert as category_convert
import Kaggle.category_id  as category_id
api = KaggleApi()
api.authenticate()

api.dataset_download_files('rmisra/news-category-dataset', path='./sources', unzip=True)


# Load data into a pandas DataFrame
kaggle_data = pd.read_json('News_Category_Dataset_v3.json',lines=True)


kaggle_data.to_csv('./data_sets/kaggle_data.csv',index=False)

kaggle_data = pd.read_csv('./data_sets/kaggle_data.csv')


#Data Cleaning
kaggle_data.dropna(subset = ['headline','short_description','authors'],inplace= True)

kaggle_data = kaggle_data.drop(columns = ['link','short_description','authors'])


kaggle_data.rename(columns={"headline":"Title","date":"Published_date","category":"Categories"},inplace=True)


kaggle_data['Source'] = 'KaggleAPI'
kaggle_data["Title_id"] = kaggle_data["Title"].factorize()[0] 





kaggle_data = category_convert.convert_categories(kaggle_data)

kaggle_data = category_id.get_category_id(kaggle_data)

kaggle_data.to_csv('./data_sets/kaggle_data.csv',index=False)








