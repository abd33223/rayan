import streamlit as st
import plotly.express as px
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
@st.cache  # This decorator will cache the dataset for faster loading
def load_data():
    dataset = pd.read_csv("Airline Dataset.csv")
    return dataset

airline = load_data()

# Display the missing rows, if any
missing_rows = airline.isnull().any(axis=1)
st.subheader("Rows with Missing Values")
st.write(airline[missing_rows])

# Drop rows with missing values
airline.dropna(inplace=True)

# Create a sidebar for selecting visualizations
st.sidebar.title("Select Visualization")
visualization_choice = st.sidebar.selectbox("Choose a Visualization", ["Histogram", "Sunburst Chart", "Animated Bubble Chart", "Box Plot", "Time Series Line Chart"])

# Visualize the data based on user choice
if visualization_choice == "Histogram":
    st.title("Histogram of Passenger Ages")
    plt.figure(figsize=(8, 6))
    sns.histplot(data=airline[:250], x='Age', bins=20, kde=True)
    plt.title('Histogram of Passenger Ages')
    plt.xlabel('Age')
    plt.ylabel('Frequency')
    st.pyplot()

elif visualization_choice == "Sunburst Chart":
    st.title("Top 10 Nationalities Among Passengers (First 500 Records)")
    top_nationalities = airline['Nationality'][:500].value_counts().head(10).reset_index()
    top_nationalities.columns = ['Nationality', 'Count']
    fig = px.sunburst(top_nationalities, path=['Nationality'], values='Count')
    st.plotly_chart(fig)

elif visualization_choice == "Animated Bubble Chart":
    st.title("Distribution of Flights on World Map (Animated Bubble Chart)")
    fig = px.scatter_geo(airline[:1000], locations='Country Name', locationmode='country names', color='Flight Status')
    st.plotly_chart(fig)

elif visualization_choice == "Box Plot":
    st.title("Box Plot of Passenger Ages by Continent")
    fig = px.box(airline.head(500), x='Continents', y='Age')
    st.plotly_chart(fig)

elif visualization_choice == "Time Series Line Chart":
    st.title("Number of Flights by Month (First 1000 Records)")
    airline['Departure Date'] = pd.to_datetime(airline['Departure Date'])
    flight_counts_by_month = airline[:1000].groupby(airline['Departure Date'].dt.to_period('M')).size().reset_index(name='Flight Count')
    flight_counts_by_month['Departure Date'] = flight_counts_by_month['Departure Date'].dt.strftime('%Y-%m')
    fig = px.line(flight_counts_by_month, x='Departure Date', y='Flight Count')
    st.plotly_chart(fig)
