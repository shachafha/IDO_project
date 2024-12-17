import streamlit as st
import calendar
from datetime import date, timedelta
import json

# Set page configuration
st.set_page_config(page_title="Riddle Calendar", layout="wide")

# Custom CSS for improved responsiveness
st.markdown("""
<style>
    /* Hide Streamlit default sidebar */
    [data-testid="stSidebar"][aria-expanded="true"] > div:first-child {
        visibility:hidden;
        width: 0px;
    }
    [data-testid="stSidebar"][aria-expanded="false"] > div:first-child {
        visibility:hidden;
    }

    /* Day headers */
    .day-header {
        text-align: center;
        font-weight: bold;
        margin-bottom: 10px;
    }

    /* Button styling */
    .calendar-button {
        width: 100% !important;
        height: 100px !important;
        font-size: 20px !important;
        display: flex !important;
        flex-direction: column !important;
        justify-content: center !important;
        align-items: center !important;
        border: none !important;
        border-radius: 12px !important;
        margin-bottom: 10px !important;
    }

    /* Ensure consistent layout */
    [data-testid="column"] {
        width: 100% !important;
        max-width: 100% !important;
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

    # Day names (full for better readability)
    day_names = list(calendar.day_name)

    # Display day name headers
    day_header_row = st.columns(7)
    for i, day in enumerate(day_names):
        day_header_row[i].markdown(f"<div class='day-header'>{day}</div>", unsafe_allow_html=True)

    # Current date tracker
    current_date = start_date

    # Track week progress
    week_days = []

    while current_date <= end_date:
        # Check if date has a riddle
        date_str = current_date.strftime("%Y-%m-%d")
        has_riddle = date_str in riddles

        # Determine button color and clickability
        if current_date == date.today():
            button_color = "#007bff"  # Blue for today
            button_clickable = True
        elif current_date > date.today():
            button_color = "#d3d3d3"  # Lighter gray for future days
            button_clickable = False
        else:
            button_color = "#28a745"  # Green for past days
            button_clickable = False

        # Create button text
        button_text = f"{current_date.day}\n{current_date.strftime('%b')}"

        # Collect dates for the current week
        week_days.append({
            'date': current_date,
            'date_str': date_str,
            'button_color': button_color,
            'button_clickable': button_clickable,
            'button_text': button_text
        })

        # If we've collected 7 days or reached the end date, render the week
        if len(week_days) == 7 or current_date == end_date:
            # Create columns for the week
            week_cols = st.columns(7)

            # Populate columns with buttons
            for i, day_info in enumerate(week_days):
                col = week_cols[i]

                # Display clickable or non-clickable button
                if day_info['button_clickable']:
                    if col.button(day_info['button_text'], key=day_info['date_str'], type="primary"):
                        # Store selected date in session state
                        st.session_state['selected_date'] = day_info['date_str']
                        # Navigate to riddle page
                        st.switch_page("pages/riddle_page.py")
                else:
                    # Display non-interactive button for past/future days
                    col.markdown(
                        f"<button style='background-color:{day_info['button_color']}; width: 100%; height: 100px; font-size: 20px; text-align: center; border: none; border-radius: 12px;'>{day_info['button_text']}</button>",
                        unsafe_allow_html=True
                    )

            # Reset week days
            week_days = []

        # Move to next date
        current_date += timedelta(days=1)


# Run the calendar
create_calendar()