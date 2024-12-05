# PLOTLY BUBBLE CHART-- TIME, DURATION, AND QUALITY RATING

import plotly.express as px
from utils import load_meditation_data
import pandas as pd

# Get the data
df = load_meditation_data()

# Convert session_time string to float hours
def time_to_float(time_str):
    if pd.isna(time_str):
        return None
    try:
        # Split the time string and take hours and minutes (ignore seconds)
        hours, minutes, _ = map(int, str(time_str).split(':'))
        return hours + minutes / 60
    except:
        print(f"Could not convert time: {time_str}")
        return None

# Apply the conversion
df['time_of_day'] = df['session_time'].apply(time_to_float)

# Create bubble chart
fig = px.scatter(
    df,
    x='duration_minutes',
    y='time_of_day',
    size='quality_rating',
    size_max=30,
    color='quality_rating',
    custom_data=['session_time', 'session_date', 'quality_rating', 'duration_minutes', 
                 df['nimittas'].map({True: 'Yes', False: 'No'})],  # Convert boolean to Yes/No here
    color_continuous_scale='viridis',
    title='Meditation Sessions: Duration vs Time of Day',
    labels={
        'duration_minutes': 'Duration (minutes)',
        'time_of_day': 'Time of Day',
        'quality_rating': 'Quality Rating'
    }
)

# Customize the hover template
fig.update_traces(
    hovertemplate="<br>".join([
        "Duration: %{customdata[3]} minutes",
        "Time: %{customdata[0]}",
        "Date: %{customdata[1]}",
        "Quality: %{customdata[2]}",
        "Nimittas: %{customdata[4]}",  # Now shows Yes/No
        "<extra></extra>"
    ])
)

# Update y-axis to show time in hour format
fig.update_layout(
    yaxis=dict(
        tickmode='array',
        ticktext=[f'{int(h):02d}:00' for h in range(24)],
        tickvals=list(range(24)),
        title='Time of Day',
        range=[8, 20]  # Limit y-axis to show 8 AM to 8 PM
    ),
    xaxis=dict(
        title='Duration (minutes)',
        range=[0, df['duration_minutes'].max() + 5]
    ),
    plot_bgcolor='white',
    hovermode='closest',
    height=800,
    width=1000
)

# Add gridlines
fig.update_xaxes(gridcolor='lightgrey', gridwidth=0.5)
fig.update_yaxes(gridcolor='lightgrey', gridwidth=0.5)

# Show the plot
fig.show()