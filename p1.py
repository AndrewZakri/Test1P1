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

# Most Popular Routes from BOS
top_routes = df[df['Origin'] == 'BOS'].groupby('Dest').size().sort_values(ascending=False).head(5)

# Create bar plot
fig, ax = plt.subplots()
top_routes.plot(kind='barh', ax=ax, color='skyblue')
ax.set_title('Top 5 Destinations from BOS')
ax.set_xlabel('Number of Flights')
ax.set_ylabel('Destination')

# Display in Streamlit
st.subheader("Most Popular Routes from BOS")
st.pyplot(fig)

st.write("The bar graph displays the top 5 destinations from BOS in January 2025. DCA (Ronald Reagan Washington Airport) has almost 800 direct flights in January. The next highest total is for LGA (LaGuardia Airport) with 550 flights. This would suggest that DCA is a key destination for an airline operating at BOS.")

# Daily trend analysis for January 2025

# Convert FlightDate to datetime and extract day of year
df['FlightDate'] = pd.to_datetime(df['FlightDate'])
df['Day'] = df['FlightDate'].dt.day_of_year

# Filter only BOS-origin flights
bos_df = df[df['Origin'] == 'BOS']

# Group by day of year to count number of flights per day
daily_counts = bos_df.groupby('Day').size()

# Plot daily trend
fig, ax = plt.subplots(figsize=(12, 6))
daily_counts.plot(kind='line', marker='o', linestyle='-', color='royalblue', ax=ax)
ax.set_title("Daily Flight Volume from BOS", fontsize=16)
ax.set_xlabel("Day of Year", fontsize=12)
ax.set_ylabel("Number of Flights", fontsize=12)
ax.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()

# Add plot to streamlit
st.pyplot(fig)

st.write("The daily flight volume out of BOS in January reflects a saw-toothed pattern. Observing the 3 lowest points, each around 260 flights, suggests a possible trend. These low points all occur on Saturday (11, 18 & 25). If we examine the days prior and after Saturday, we can determine that the total flights on those days are much higher. This could suggest a few possibilities. Passengers are arriving in BOS on Friday, possibly for a short stay/weekend getaway, and then depart on Sunday. Another possibility is that business travelers depart from BOS on Sunday or Monday, and then return Friday. Saturday would then have lower flight volume as the business travelers would be less active. This possibility becomes more reasonable when we examine the high points, which do coincide with Monday and Friday.")

# 7 day rolling average
fig, ax = plt.subplots(figsize=(12, 6))
daily_counts.rolling(window=7).mean().plot(ax=ax, color='darkorange', linewidth=2)
ax.set_title("7-Day Rolling Avg: Daily Flights from BOS", fontsize=16)
ax.set_xlabel("Day of Year", fontsize=12)
ax.set_ylabel("Avg Flights per Day", fontsize=12)
ax.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()

# Add plot to streamlit
st.pyplot(fig)

st.write("The 7 day rolling average of daily flights from BOS helps to smooth out the daily fluctuations. Whereas the daily flights volume line is saw-toothed, this rolling average is more consistent. We can also determine a peak in the first 10 days of the month, with a considerable decline between the 11th and 25th. Flights rebound towards the end of the month.")
