import streamlit as st
import pandas as pd
import pydeck as pdk

import matplotlib.pyplot as plt


st.title("📍 CSV Map Viewer")

# Upload CSV
uploaded_file = st.file_uploader(
    "Upload a CSV file with 'lat' and 'lon' columns", type="csv"
)

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # Check for required columns
    if "lat" in df.columns and "lon" in df.columns:
        st.success("CSV loaded successfully!")

        # Show data preview
        st.subheader("Data Preview")
        st.dataframe(df.head())

        # Map
        st.subheader("Map View")
        st.map(df[["lat", "lon"]])

        # Clustering
        # Parse date column
        df["DATE_RECORDED"] = pd.to_datetime(df["DATE_RECORDED"], errors="coerce")
        df = df.dropna(subset=["DATE_RECORDED"])

        # Time series plot
        st.subheader("📈 Pothole Reports Over Time")
        time_series = df["DATE_RECORDED"].dt.to_period("M").value_counts().sort_index()
        time_series.index = time_series.index.to_timestamp()
        fig, ax = plt.subplots()
        time_series.plot(ax=ax)
        ax.set_ylabel("Number of Reports")
        ax.set_xlabel("Date")
        ax.set_title("Monthly Pothole Reports")
        st.pyplot(fig)

    else:
        st.error("CSV must contain 'lat' and 'lon' columns.")
