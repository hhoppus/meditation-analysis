# FEATURE IMPORTANCE BAR CHART 
# CONSIDERING HOW PREDICTIVE DURATION (MIN), NIMITTAS, AND SLEEP DEPR WERE IN DETERMINING MEDITATION QUALITY

import matplotlib.pyplot as plt
import pandas as pd
from sqlalchemy import create_engine
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import os
from dotenv import load_dotenv

load_dotenv()
engine = create_engine(f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}")
df = pd.read_sql_query("SELECT * FROM meditation_sessions", engine)

X = df[['duration_minutes', 'nimittas', 'sleep_depr']].copy()
X['nimittas'] = X['nimittas'].astype(int)
X['sleep_depr'] = X['sleep_depr'].astype(int)
y = df['quality_rating']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
rf_model = RandomForestRegressor(n_estimators=100, random_state=42)  # n_estimators=100trees
rf_model.fit(X_train, y_train)

plt.figure(figsize=(10, 6))
plt.bar(['Duration (min)', 'Nimittas', 'Sleep Depr'], rf_model.feature_importances_)
plt.title('Feature Importance in Predicting Meditation Quality')
plt.ylabel('Importance Score')
plt.tight_layout()
# plt.savefig('feature_importance.png')
plt.show()


# In this analysis 100 decision trees received randomized sets of data from the 80% of the data used for the training. 
# The selection of sessions given to each tree, known as bootstrapping, might include some sessions multiple times, 
# and some session 0 times.After the training period, 20% of the data set was used for testing, allowing the trees
# to use the features to predict the outcome. The importance value of each feature was determined by how effective 
# the feature was in allowing the decision tress to predict the quality rating. 
