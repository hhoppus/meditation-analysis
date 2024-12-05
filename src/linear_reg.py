# LINEAR REGRESSION WITH RANDOM FOREST USED FOR FEATURE IMPORTANCE CHART

import pandas as pd
from sqlalchemy import create_engine
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create SQLAlchemy engine
engine = create_engine(f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}")

# Load data using SQLAlchemy
df = pd.read_sql_query("SELECT * FROM meditation_sessions", engine)

# Rest of the analysis code remains the same
X = df[['duration_minutes', 'nimittas', 'sleep_depr']].copy()
X['nimittas'] = X['nimittas'].astype(int)
X['sleep_depr'] = X['sleep_depr'].astype(int)
y = df['quality_rating']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

lr_model = LinearRegression()
lr_model.fit(X_train, y_train)
lr_pred = lr_model.predict(X_test)
lr_r2 = r2_score(y_test, lr_pred)

rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)
rf_pred = rf_model.predict(X_test)
rf_r2 = r2_score(y_test, rf_pred)

feature_importance = pd.DataFrame({
    'feature': X.columns,
    'importance': rf_model.feature_importances_
}).sort_values('importance', ascending=False)

print("\nModel Performance (R² scores):")
print(f"Linear Regression: {lr_r2:.3f}")
print(f"Random Forest: {rf_r2:.3f}")
print("\nFeature Importance:")
print(feature_importance)