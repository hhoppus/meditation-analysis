# Run in terminal: 
# streamlit run streamlit_dashboard.py

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils import load_meditation_data
from datetime import datetime

def extract_hour(time_str):
    """Convert session time string to hour, with error handling."""
    if pd.isna(time_str):
        return None
    try:
        return datetime.strptime(str(time_str), '%H:%M:%S').hour
    except ValueError:
        try:
            return datetime.strptime(str(time_str), '%H:%M').hour
        except ValueError:
            st.warning(f"Could not parse time: {time_str}")
            return None

def main():
    st.set_page_config(page_title="Meditation Tracker", layout="wide")
    st.title("Meditation Practice Dashboard")

    # Load data with error handling
    try:
        df = load_meditation_data()
        if df.empty:
            st.error("No meditation data available. Please check your database connection.")
            return
    except Exception as e:
        st.error(f"Failed to load meditation data: {str(e)}")
        return

    try:
        df['session_date'] = pd.to_datetime(df['session_date'])
    except Exception as e:
        st.error("Error processing dates in meditation data. Please check data format.")
        return

    # Sidebar filters
    st.sidebar.header("Filters")
    try:
        date_range = st.sidebar.date_input(
            "Date Range",
            [df['session_date'].min(), df['session_date'].max()]
        )
    except Exception as e:
        st.sidebar.error("Error setting date range. Using all available dates.")
        date_range = [df['session_date'].min(), df['session_date'].max()]

    # Filter data
    try:
        mask = (df['session_date'].dt.date >= date_range[0]) & (df['session_date'].dt.date <= date_range[1])
        filtered_df = df.loc[mask]
        
        if filtered_df.empty:
            st.warning("No data available for selected date range.")
            return
    except Exception as e:
        st.error("Error filtering data by date range.")
        return

    # Layout with columns
    col1, col2 = st.columns(2)

    with col1:
        try:
            # Quality vs Duration Scatter
            fig_scatter = px.scatter(
                filtered_df,
                x='duration_minutes',
                y='quality_rating',
                trendline="ols",
                title="Meditation Duration vs Quality"
            )
            st.plotly_chart(fig_scatter)
        except Exception as e:
            st.error("Error creating duration vs quality plot.")

        try:
            # Time of Day Analysis
            filtered_df['hour'] = filtered_df['session_time'].apply(extract_hour)
            time_quality = filtered_df.groupby('hour')['quality_rating'].mean().reset_index()
            fig_time = px.line(
                time_quality,
                x='hour',
                y='quality_rating',
                title="Average Quality by Time of Day"
            )
            st.plotly_chart(fig_time)
        except Exception as e:
            st.error("Error creating time of day analysis plot.")

    with col2:
        try:
            # Box Plot for Nimittas
            fig_box = go.Figure()
            fig_box.add_trace(go.Box(
                y=filtered_df[filtered_df['nimittas'] == False]['duration_minutes'],
                name="No Nimittas"
            ))
            fig_box.add_trace(go.Box(
                y=filtered_df[filtered_df['nimittas'] == True]['duration_minutes'],
                name="With Nimittas"
            ))
            fig_box.update_layout(title="Duration Distribution by Nimittas")
            st.plotly_chart(fig_box)
        except Exception as e:
            st.error("Error creating nimittas distribution plot.")

        try:
            # Recent Sessions Table
            st.subheader("Recent Sessions")
            recent = filtered_df.sort_values('session_date', ascending=False).head(5)
            st.dataframe(recent[['session_date', 'session_time', 'duration_minutes', 'quality_rating', 'nimittas']])
        except Exception as e:
            st.error("Error displaying recent sessions table.")

    # Summary Statistics
    st.header("Summary Statistics")
    try:
        col3, col4, col5 = st.columns(3)
        with col3:
            st.metric("Average Duration", f"{filtered_df['duration_minutes'].mean():.1f} min")
        with col4:
            st.metric("Average Quality", f"{filtered_df['quality_rating'].mean():.1f}/10")
        with col5:
            st.metric("Total Sessions", len(filtered_df))
    except Exception as e:
        st.error("Error calculating summary statistics.")

if __name__ == "__main__":
    main()