#  Media Content Analytics Platform

A data visualization and analytics platform for media content insights using **Streamlit**, **MySQL**, **Matplotlib** and **Plotly**.

## 🚀 Features

- Interactive dashboard to analyze media engagement metrics
- Filters for categories and months
- Visualizations for views, engagement rates, and interactions
- MySQL database integration

## 📁 Project Structure

```
MEDIA_CONTENT_PLATFORM/
│── data_sets/               # Raw datasets (CSV files)
│── database_tables/         # Predefined table structures (CSV files)
|── Kaggle/                  # Processing the data from Kaggle Dataset
│── sources/                 # Data source files
|── Youtube/                 # Processing data from Youtube API
│── med_env/                 # Virtual environment (optional)
│── .env                     # Environment variables (hidden)
│── .env_sample              # Sample environment file
│── .gitignore               # Git ignore file
│── app.py                   # Streamlit app script
│── data_extraction.ipynb    # Data extraction & preprocessing notebook
│── LICENSE                  # License file
│── README.md                # Project documentation
```

## 🛠️ Installation

1️⃣ **Clone the repository**

```sh
git clone https://github.com/Jasper1007J/media-content-platform.git
cd media-content-platform
```

2️⃣ **Create a virtual environment (optional but recommended)**

```sh
python -m venv med_env
source med_env/bin/activate   # On macOS/Linux
med_env\Scripts\activate      # On Windows
```

3️⃣ **Install dependencies**

```sh
pip install -r requirements.txt
```

## 📊 Usage

Run the Streamlit application:

```sh
streamlit run app.py
```

## 🗄️ Database Setup
```sh
1️⃣ Start MySQL Server and create the `youtube` database.
2️⃣ Import the predefined tables from `database_tables/`.
3️⃣ Update `.env` file with database credentials.
```

## 🖼️ Dashboard Visuals

- **Engagement Metrics per Category** 📊
- **Engagement Rate Trends** 📈


## 📜 License

This project is licensed under the MIT License.

---
⭐ **Developed by Namala Jasper**
