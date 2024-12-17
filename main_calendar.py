import streamlit as st
import calendar
from datetime import date, timedelta
import json

# Set page configuration
st.set_page_config(page_title="Riddle Calendar", layout="wide")

# Hide Streamlit default sidebar and add button styling
st.markdown("""
<style>
    [data-testid="stSidebar"][aria-expanded="true"] > div:first-child {
        visibility:hidden;
        width: 0px;
    }
    [data-testid="stSidebar"][aria-expanded="false"] > div:first-child {
        visibility:hidden;
    }

    /* Button styling */
    .calendar-button {
        width: 100%;
        height: 70px;  /* Adjust height */
        font-size: 16px;
        text-align: center;
        border: none;
        border-radius: 8px;
        cursor: pointer;
        transition: transform 0.2s;
    }
    .calendar-button:hover {
        transform: scale(1.05); /* Hover effect */
    }
    .current-day { background-color: #007bff; color: white; }
    .future-day { background-color: #d3d3d3; color: black; }
    .past-day { background-color: #28a745; color: white; }

    /* Center align titles */
    .day-title {
        text-align: center;
        font-weight: bold;
        font-size: 18px;
    }
</style>
""", unsafe_allow_html=True)

# Load riddles
with open('riddles.json', 'r') as f:
    riddles = json.load(f)

# Function to create the calendar
def create_calendar():
    # Set the start and end dates
    start_date = date(2024, 12, 9)
    end_date = date(2025, 1, 2)

    # Display calendar title
    st.markdown("<h1 style='text-align: center;'>30 DAYS TO 30</h1>", unsafe_allow_html=True)

    # Day names row
    day_names = list(calendar.day_abbr)
    day_cols = st.columns(7)  # Create 7 columns for day headers
    for i, day in enumerate(day_names):
        day_cols[i].markdown(f"<div class='day-title'>{day}</div>", unsafe_allow_html=True)

    # Initialize calendar grid
    current_date = start_date
    col_index = current_date.weekday()  # Start from the correct weekday
    cols = st.columns(7)  # Create 7 columns for dates

    # Loop through the date range
    while current_date <= end_date:
        date_str = current_date.strftime("%Y-%m-%d")

        # Determine button color class
        if current_date == date.today():
            button_class = "current-day"
        elif current_date > date.today():
            button_class = "future-day"
        else:
            button_class = "past-day"

        # Button content
        button_text = f"{current_date.day}<br>{current_date.strftime('%b')}"

        # Create a button (simulated with markdown)
        cols[col_index].markdown(
            f"<button class='calendar-button {button_class}'>{button_text}</button>",
            unsafe_allow_html=True
        )

        # Move to next column
        col_index += 1
        if col_index > 6:  # Reset to the first column after Sunday
            col_index = 0
            cols = st.columns(7)  # Create a new row of columns

        current_date += timedelta(days=1)

# Run the calendar
create_calendar()
