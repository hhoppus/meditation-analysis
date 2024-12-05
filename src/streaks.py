# SCATTERPLOT SHOWING RELATIONSHIP BETWEEN STREAK LENGTH AND QUALITY RATING

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from utils import load_meditation_data
from scipy import stats  

def calculate_streaks(df):
    # Convert session_date to datetime
    df['session_date'] = pd.to_datetime(df['session_date'])
    
    date_range = pd.date_range(start=df['session_date'].min(), end=df['session_date'].max(), freq='D')
    all_dates = pd.DataFrame({'session_date': date_range})
    
    meditation_days = df['session_date'].dt.date.unique()
    all_dates['meditated'] = all_dates['session_date'].dt.date.isin(meditation_days)
    
    streaks = []
    current_streak = 0
    
    for meditated in all_dates['meditated']:
        if meditated:
            current_streak += 1
        else:
            current_streak = 0
        streaks.append(current_streak)
    
    all_dates['streak'] = streaks
    df['streak'] = df['session_date'].map(all_dates.set_index('session_date')['streak'])
    
    df['week'] = df['session_date'].dt.isocalendar().week
    df['year'] = df['session_date'].dt.year
    weekly_sessions = df.groupby(['year', 'week']).size().reset_index(name='sessions_per_week')
    df = df.merge(weekly_sessions, on=['year', 'week'])
    
    return df

def plot_streak_quality(df):
    plt.figure(figsize=(10, 6))
    plt.scatter(df['streak'], df['quality_rating'])
    
    plt.xlabel('Streak Length (consecutive days)')
    plt.ylabel('Quality Rating')
    
    correlation, p_value = stats.pearsonr(df['streak'], df['quality_rating'])
    
    z = np.polyfit(df['streak'], df['quality_rating'], 1)
    p = np.poly1d(z)
    plt.plot(df['streak'], p(df['streak']), "r--")
    
    plt.title(f'Meditation Quality vs Streak Length (r = {correlation:.3f}, p = {p_value:.3f})')
    plt.show()

def get_meditation_streaks():
    df = load_meditation_data()
    return calculate_streaks(df)

if __name__ == "__main__":
    df_with_streaks = get_meditation_streaks()
    plot_streak_quality(df_with_streaks)




