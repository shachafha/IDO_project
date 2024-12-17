import streamlit as st
import calendar
from datetime import date, timedelta
import json
import locale

# Set page configuration
st.set_page_config(page_title="Riddle Calendar", layout="wide")

# Hide Streamlit default sidebar
st.markdown("""
<style>
    [data-testid="stSidebar"][aria-expanded="true"] > div:first-child {
        visibility:hidden;
        width: 0px;
    }
    [data-testid="stSidebar"][aria-expanded="false"] > div:first-child {
        visibility:hidden;
    }
    .big-font {
        font-size:20px !important;
        text-align: center;
    }
    .stButton>button {
        width: 100%;
        height: 150px;
        font-size: 20px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        background-color: #007bff !important;
        border: none;  /* Remove the border */
        border-radius: 12px;  /* Add rounded corners */
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

    # Display current month and year
    st.markdown(f"<h1 style='text-align: center;'>30 DAYS TO 30</h2>", unsafe_allow_html=True)

    # Create columns for calendar
    cols = st.columns(7)

    # Current date tracker
    current_date = start_date

    # Day names (abbreviated)
    day_names = list(calendar.day_abbr)

    # Display day names
    for i, day in enumerate(day_names):
        cols[i].markdown(f"<h3 style='text-align: center;'>{day}</h3>", unsafe_allow_html=True)

    # Reset columns
    cols = st.columns(7)

    # Fill initial empty spaces
    start_weekday = start_date.weekday()
    for i in range(start_weekday):
        cols[i].write("")

    # Track column index
    col_index = start_weekday

    # Create buttons for each date
    while current_date <= end_date:
        # Check if date has a riddle
        date_str = current_date.strftime("%Y-%m-%d")
        has_riddle = date_str in riddles

        # Determine button color based on the date's status
        if current_date == date.today():
            button_color = "#007bff"  # Blue for today
            button_clickable = True  # Optional, based on your requirement
        elif current_date > date.today():
            button_color = "#d3d3d3"  # Lighter gray for future days
            button_clickable = False  # Future days should not be clickable
        else:
            button_color = "#28a745"  # Green for past days
            button_clickable = False  # Past days are also not clickable

        # Create button with day and month
        button_text = f"{current_date.day}\n{current_date.strftime('%b')}"

        # Display button
        if button_clickable and cols[col_index].button(button_text, key=date_str, type="primary"):
            # Store selected date in session state
            st.session_state['selected_date'] = date_str
            # Navigate to riddle page
            st.switch_page("pages/riddle_page.py")

        # Display button without functionality for past/future days
        if not button_clickable:
            cols[col_index].markdown(
                f"<button style='background-color:{button_color}; width: 100%; height: 150px; font-size: 20px; text-align: center; border: none; border-radius: 12px;'>{button_text}</button>",
                unsafe_allow_html=True)

        # Move to next column
        col_index += 1

        # Start new row if end of week
        if col_index > 6:
            col_index = 0
            cols = st.columns(7)

        # Move to next date
        current_date += timedelta(days=1)


# Run the calendar
create_calendar()
