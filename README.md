# Momentum Model

This project implements a momentum-based trading model. The model fetches/processes financial data, builds datasets, and applies machine learning techniques to predict momentum.

## Files Description
- **ticker_list.py**: Scans and retrieves tickers
- **ohlcv_builder.py**: Fetches/processes OHLCV data
- **momentum_features.py**: Builds momentum dataset
- **model.py**: Implements machine learning models to predict momentum

## Setup and Usage

1. **Clone Repository**
   ```bash
   git clone https://github.com/your-username/your-repo-name.git
   cd your-repo-name
2. **Install Dependencies**
- With env:
   ```bash
   pip install -r requirements.txt
- Without env:
   ```bash
   pip install requests pandas numpy sqlalchemy matplotlib pandas-market-calendars pmdarima scikit-learn python-dotenv
3. **Configuration**
- Create .env in main directory
   ```bash
   API_KEY = "your_polygon_api_key"
   DB_LOGIN = "mysql+mysqlconnector://username:password@hostname:port/database"
4. **Run Scripts**
   ```bash
   python ticker_list.py
   python ohlcv_builder.py
   python momentum_features.py
   python model.py