# 7 SESSION ROLLING AVERAGES FOR DURATION AND QUALITY 

import matplotlib.pyplot as plt
import numpy as np
from utils import load_meditation_data
import pandas as pd

# Get the data
df = load_meditation_data()

# Calculate rolling averages for different metrics (duration and quality)
window_size = 7  # 7-day rolling average

# Create figure with multiple subplots
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
fig.suptitle('Meditation Trends (7-session Rolling Averages)')

# Plot 1: Duration Rolling Average
duration_rolling = df['duration_minutes'].rolling(window=window_size).mean()
ax1.plot(range(len(df)), df['duration_minutes'], 'o', alpha=0.3, label='Session Duration')
ax1.plot(range(len(df)), duration_rolling, 'r-', linewidth=2, label=f'{window_size}-session Rolling Average')
ax1.set_ylabel('Duration (minutes)')
ax1.set_title('Meditation Duration Trend')
ax1.legend()
ax1.grid(True, alpha=0.3)

# Plot 2: Quality Rating Rolling Average
quality_rolling = df['quality_rating'].rolling(window=window_size).mean()
ax2.plot(range(len(df)), df['quality_rating'], 'o', alpha=0.3, label='Session Quality')
ax2.plot(range(len(df)), quality_rolling, 'g-', linewidth=2, label=f'{window_size}-session Rolling Average')
ax2.set_ylabel('Quality Rating')
ax2.set_xlabel('Session Number')
ax2.set_title('Meditation Quality Trend')
ax2.legend()
ax2.grid(True, alpha=0.3)

# Adjust layout to prevent overlap
plt.tight_layout()
plt.show()

# Print some statistics
print("\nRolling Average Statistics:")
print(f"Recent average duration: {duration_rolling.iloc[-1]:.1f} minutes")
print(f"Recent average quality: {quality_rolling.iloc[-1]:.1f}/10")

# Only print 30-session trends if we have enough data
if len(df) >= 30:
    print(f"Duration trend (last 30 sessions): {(duration_rolling.iloc[-1] - duration_rolling.iloc[-30]):.1f} minutes")
    print(f"Quality trend (last 30 sessions): {(quality_rolling.iloc[-1] - quality_rolling.iloc[-30]):.1f} points")