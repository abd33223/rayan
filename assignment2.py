import streamlit as st
import pandas as pd
import plotly.express as px

# Load the airline dataset (assuming it's already loaded)
# If not, you can load it using pd.read_csv() as mentioned earlier
# airline = pd.read_csv("path/to/your/Airline Dataset.csv")

# Set the page title and favicon
st.set_page_config(
    page_title="Airline Data Visualization",
    page_icon="✈️",
    layout="wide",
)

# Add a header with a title and description
st.title("Airline Data Visualization")
st.markdown("Explore insights from the airline dataset with interactive visualizations.")


# Create a Streamlit app for the first visualization
st.header('Visualization 1: Top 10 Nationalities Among Passengers')
st.write("This sunburst chart explores the top 10 nationalities among passengers in the dataset.")

# Add a sidebar slider to select the number of records to consider
num_records_2 = st.slider("Number of Records for Sunburst Chart", min_value=1, max_value=len(airline), value=500)

# Calculate the top 10 nationalities and their counts based on the selected number of records
top_nationalities = airline['Nationality'][:num_records_2].value_counts().head(10).reset_index()
top_nationalities.columns = ['Nationality', 'Count']

# Display the sunburst chart using Plotly Express
fig = px.sunburst(top_nationalities, path=['Nationality'], values='Count')
fig.update_traces(textinfo='label+percent parent')

# Display the chart in the Streamlit app
st.plotly_chart(fig)

# Create a Streamlit app for the second visualization
st.header('Visualization 2: Distribution of Flights on World Map (Animated Bubble Chart)')
st.write("This animated bubble chart explores the distribution of flights on a world map.")

# Add a sidebar slider to select the number of records to consider
num_records_3 = st.slider("Number of Records for Bubble Chart", min_value=1, max_value=len(airline), value=1000)

# Create an animated bubble chart on a map with the selected number of records
fig = px.scatter_geo(airline[:num_records_3],  # Slice to select the specified number of records
                     locations='Country Name',
                     locationmode='country names',
                     color='Flight Status',
                     title='Distribution of Flights on World Map (Animated Bubble Chart)')

# Display the chart in the Streamlit app
st.plotly_chart(fig)

# Create a Streamlit app for the fourth visualization
st.header('Visualization 4: Number of Flights by Month (First 1000 Records)')
st.write("This time series line chart shows the number of flights by month.")

flight_counts_by_month = airline[:1000].groupby(airline['Departure Date'].dt.to_period('M')).size().reset_index(name='Flight Count')
flight_counts_by_month['Departure Date'] = flight_counts_by_month['Departure Date'].dt.strftime('%Y-%m')

# Specify an older version of Plotly that is compatible with Streamlit (e.g., version 4.14.3)
import plotly
plotly_version = "4.14.3"

# Check if the imported version of Plotly matches the specified version
if plotly.__version__ != plotly_version:
    st.warning(f"Warning: This app is designed for Plotly version {plotly_version}. You have version {plotly.__version__}. Some features may not work as expected.")

# Create a time series line chart to show the number of flights by month
fig = px.line(flight_counts_by_month, x='Departure Date', y='Flight Count',
              title='Number of Flights by Month (First 1000 Records)',
              labels={'Departure Date': 'Month', 'Flight Count': 'Flight Count'})

# Add interactivity: Use date range slider to select time periods
st.plotly_chart(fig)

