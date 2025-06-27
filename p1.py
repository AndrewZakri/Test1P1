import streamlit as st
import folium
from folium import plugins
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from streamlit_folium import st_folium

# Load data - filtered for BOS
df = pd.read_csv("BOS_Jan_25.csv")
bos_routes = df[df['Origin'] == 'BOS'][['Origin', 'Dest', 'Dest_lat', 'Dest_long']].drop_duplicates()

st.title("Test 1, Problem 1")

st.write("Select one major airport from the U.S. East Coast (JFK, ATL, MIA, BOS, PHL, etc.). Map all the direct routes from the selected airport. Perform an Exploratory Data Analysis (EDA) to understand popular routes, airport connectivity, and operations performance.")

st.subheader("Boston Logan Airport (BOS)")

st.subheader("Direct Routes From Boston Logan Airport (BOS)")

# Create base map
m = folium.Map(location=[42.3656, -71.0096], zoom_start=4)

# Add lines for each direct route
for _, row in bos_routes.iterrows():
    folium.PolyLine(
        locations=[
            [42.3656, -71.0096],
            [row['Dest_lat'], row['Dest_long']]
        ],
        color="blue",
        weight=2,
        opacity=0.6
    ).add_to(m)

# Creat map for direct destinations from BOS
st_folium(m, width=725, height=500)

st.write("Direct Routes from Boston Logan Airport (BOS)")

st.write("An interactive map of all direct destinations from Boston Logan Airport (BOS). Direct routes are displayed in blue. Utilizing additional code, it was determined that BOS has direct connections to 63 airports. However, it should be noted that the dataset reflects flights occuring in January 2025 only. It is possible that connections in months not examined could be greater or fewer.")

