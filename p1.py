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

# Create dataframe
bos_df = df[df['Origin'] == 'BOS'].copy()
bos_df = bos_df[pd.to_numeric(bos_df['DepTime'], errors='coerce').notnull()]
bos_df['DepHour'] = bos_df['DepTime'].astype(int) // 100

# Group by hour of day
hourly_counts = bos_df.groupby('DepHour').size()

# Plot
fig, ax = plt.subplots(figsize=(10, 5))
hourly_counts.plot(kind='bar', color='skyblue', edgecolor='black', ax=ax)
ax.set_title("Flight Volume by Time of Day from BOS", fontsize=16)
ax.set_xlabel("Hour of Day (24-hour format)", fontsize=12)
ax.set_ylabel("Number of Flights", fontsize=12)
ax.set_xticks(range(0, 24))
ax.set_xticklabels([str(h).zfill(2) for h in range(0, 24)], rotation=0)
ax.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()

# Add plot to streamlit
st.pyplot(fig)

st.write("Flight volumne by time of day peaks at 7am and remains consistent high in the hours preceding and following. We can determine a drop off in flights between 11am and 2pm, with another increase between 3pm and 7pm. There is a substantial drop off in flights after 7pm, and very little to no activity in the overnight hours.")

# Create data frame
bos_df = df[df['Origin'] == 'BOS'].copy()

# Create a list of U.S. IATA airport codes
us_airports = ['ATL', 'ORD', 'LAX', 'JFK', 'DFW', 'MIA', 'DEN', 'SFO', 'CLT', 'SEA',
               'PHL', 'EWR', 'BOS', 'DCA', 'LGA', 'IAD', 'PHX', 'MSP', 'DTW', 'HNL',
               'MDW', 'MCO', 'TPA', 'BWI', 'SLC', 'SAN', 'CLE', 'PIT', 'STL', 'CVG',
               'RDU', 'AUS', 'BNA', 'SJC', 'SMF', 'IND', 'MKE', 'BUF', 'SAT', 'SDF',
               'ORF', 'PVD', 'RIC', 'ALB', 'SYR', 'MYR', 'SRQ', 'FLL', 'RSW', 'JAX',
               'MSY', 'CHS', 'GRR', 'PBI', 'TYS', 'AVL', 'HDN', 'EYW', 'PQI']

# Label flight domestic or international
bos_df['FlightType'] = bos_df['Dest'].apply(lambda x: 'Domestic' if x in us_airports else 'International')

# Calculate percentage
flight_type_counts = bos_df['FlightType'].value_counts(normalize=True) * 100

# Display result
fig, ax = plt.subplots()
flight_type_counts.plot(
    kind='pie',
    autopct='%1.1f%%',
    startangle=90,
    colors=['skyblue', 'lightcoral'],
    ax=ax
)
ax.set_title('Domestic vs. International Flights from BOS')
ax.set_ylabel('')
plt.tight_layout()

# Add plot to streamlit
st.pyplot(fig)

st.write("This pie chart reflects an overwhelming percentage of total flights classified as Domestic. Reviewing the direct route map, we can determine that there are only 2 destinations outside of the United States serviced by BOS. One in Puerto Rico and the other in the British Virgin Islands. Surprisingly, the number of International flights is low for an airport located in close proximity to the Atlantic Ocean. A possible explanation is that the demand for international travel in the New England area is low, either for business or leisure. It is also possible that neighboring airports, such as those in NYC are competing with BOS for international travel.")

# Filter flights originating from BOS
bos_df = df[df['Origin'] == 'BOS']

# Count number of flights by carrier
airline_counts = bos_df['Carrier'].value_counts().head(10)  # Top 10 airlines

# Optional: Map carrier codes to full airline names (partial example)
carrier_names = {
    'AA': 'American Airlines',
    'DL': 'Delta Air Lines',
    'UA': 'United Airlines',
    'B6': 'JetBlue Airways',
    'WN': 'Southwest Airlines',
    'NK': 'Spirit Airlines',
    'AS': 'Alaska Airlines',
    'YX': 'Republic Airways',
    'F9': 'Fontier Airlines',
    'MQ':  'Envoy Air'
}
airline_counts.index = [carrier_names.get(code, code) for code in airline_counts.index]

# Plot
fig, ax = plt.subplots(figsize=(10, 5))
airline_counts.plot(kind='barh', color='mediumseagreen', edgecolor='black', ax=ax)
ax.set_title("Top Airlines Operating from BOS – January 2025", fontsize=16)
ax.set_xlabel("Number of Flights", fontsize=12)
ax.set_ylabel("Airline", fontsize=12)
ax.invert_yaxis()  # Highest count at the top
ax.grid(axis='x', linestyle='--', alpha=0.7)
plt.tight_layout()

# Add plot to streamlit
st.pyplot(fig)

st.write("Referencing the bar chart for top airlines operating in BOS, we can see that there are 5 airlines with relatively high flight volumes, and the remaining airlines with much smaller volumes. JetBlue has just under 3000 flights, followed by Republic at 2500, Delta at 1800, American at 1100, and United at 900. The next closest is Spirit and Southwest with under 500 flights each. It could be argued that BOS is a hub for JetBlue, or at the very least an important airport in its network.")

# Delay performance

# Create dataframe
bos_df = df[df['Origin'] == 'BOS']

# Distribution of departure delays
fig, ax = plt.subplots(figsize=(10, 5))
sns.histplot(bos_df['DepDelay'].dropna(), bins=50, kde=True, ax=ax)
ax.set_title("Distribution of Departure Delays from BOS")
ax.set_xlabel("Departure Delay (minutes)")
ax.set_ylabel("Flight Count")

# Add plot to streamlit
st.pyplot(fig)

st.write("Reviewing the plot, we can determine that the peak is near zero minutes, which means that most flights depart ontime, or very close to ontime. The small number of negative values mean that some flights departed early. The distribution has a right-skewed tail, which means that while most flights are ontime or slightly delayed, there are some flights with significant delays. Cancelation rate is also very low at 2.37% of flights.")
