import requests
import pandas as pd
import sqlalchemy
from datetime import datetime, timedelta
from pandas_market_calendars import get_calendar
import os

load_dotenv()

DB_LOGIN = os.getenv("DB_PROD_LOGIN")
API_KEY = os.getenv("API_KEY")

engine = sqlalchemy.create_engine(DB_LOGIN)

calendar = get_calendar("NYSE")

date = (
    calendar.schedule(
        start_date=(datetime.today() - timedelta(days=10)), end_date=datetime.today()
    )
    .index.strftime("%Y-%m-%d")
    .values[-1]
)

all_assets_1 = requests(
    f"https://api.polygon.io/v3/reference/tickers?type=CS&market=stocks&active=true&order=asc&sort=ticker&limit=1000&apiKey={API_KEY}"
).json()
all_assets_2 = requests(f"{all_assets_1['next_url']}&apikey={API_KEY}").json()
all_assets_3 = requests(f"{all_assets_2['next_url']}&apikey={API_KEY}").json()
all_assets_4 = requests(f"{all_assets_3['next_url']}&apikey={API_KEY}").json()
all_assets_5 = requests(f"{all_assets_4['next_url']}&apikey={API_KEY}").json()
all_assets_6 = requests(f"{all_assets_5['next_url']}&apikey={API_KEY}").json()

asset_list = [
    all_assets_1,
    all_assets_2,
    all_assets_3,
    all_assets_4,
    all_assets_5,
    all_assets_6,
]
available_asset_list = []

for asset_data in asset_list:
    available_assets = pd.json_normalize(asset_data["results"])
    available_asset_list.append(available_assets)

total_available_assets = pd.concat(available_asset_list)
total_available_assets.to_sql("all_assets", con=engine, if_exists="replace")
