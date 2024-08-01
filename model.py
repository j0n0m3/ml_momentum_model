import pandas as pd
import sqlalchemy
import pmdarima as pmdarima
import os
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.model_selection import KFold, cross_validate

load_dotenv()

DB_LOGIN = os.getenv("DB_LOGIN")
API_KEY = os.getenv("API_KEY")


def Binarizer(value):
    if value > 0:
        return 1
    elif value <= 0:
        return 0


engine = sqlalchemy.create_engine(DB_LOGIN)
og_dataset = pd.read_sql("SELECT * FROM momentum_dataset", con=engine)
tickers = pd.read_sql("SELECT * FROM all_assets", con=engine)

dataset = og_dataset.copy().dropna().set_index("date")
dataset = og_dataset["ticker"].isin(tickers["ticker"].values)

# sample selection
dataset = dataset[dataset.index >= "2023-01-01"]

dataset = dataset.dop("index", axis=1)
dataset = pd.get_dummies(dataset)

target = "pct_change"

X_train = dataset.copy().drop(target, axis=1)
Y_train = dataset[target].values
Y_train_class = dataset[target].apply(Binarizer).values

k_folds = KFold(n_splits=5, shuffle=False)
rf_classification_scores = pd.DataFrame(
    cross_validate(
        estimator=RandomForestClassifier(),
        X=X_train,
        Y=Y_train_class,
        cv=k_folds,
        scoring=["accuracy", "precision", "recall", "f1", "roc_auc"],
    )
)
rf_regression_scores = pd.DataFrame(
    cross_validate(
        estimator=RandomForestRegressor(),
        X=X_train,
        Y=Y_train.ravel(),
        cv=k_folds,
        scoring=["neg_mean_absolute_error", "r2", "max_error"],
    )
)
