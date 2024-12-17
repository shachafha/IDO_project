import streamlit as st
import calendar
from datetime import date, timedelta
import json
import locale

# Set page configuration
st.set_page_config(page_title="Riddle Calendar", layout="wide")

# Mobile-responsive CSS
st.markdown("""
<style>
    /* Hide Streamlit default sidebar */
    [data-testid="stSidebar"][aria-expanded="true"] > div:first-child {
        visibility: hidden;
        width: 0px;
    }
    [data-testid="stSidebar"][aria-expanded="false"] > div:first-child {
        visibility: hidden;
    }

    /* Calendar day buttons */
    .custom-button {
        width: 100% !important;
        height: 80px !important;
        font-size: 14px !important;
        display: flex !important;
        flex-direction: column !important;
        justify-content: center !important;
        align-items: center !important;
        background-color: #007bff !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 5px !important;
        white-space: normal !important;
        word-wrap: break-word !important;
        text-align: center !important;
    }

    /* Day name headers */
    .day-header {
        text-align: center !important;
        font-size: 14px !important;
        font-weight: bold !important;
        padding: 5px !important;
    }

    /* Responsive text sizing */
    @media (max-width: 600px) {
        .custom-button {
            height: 60px !important;
            font-size: 12px !important;
        }

        .day-header {
            font-size: 12px !important;
        }
    }

    @media (max-width: 400px) {
        .custom-button {
            height: 50px !important;
            font-size: 10px !important;
        }
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
    st.markdown(f"<h1 style='text-align: center;'>30 DAYS TO 30</h1>", unsafe_allow_html=True)

    # Day names (abbreviated)
    day_names = list(calendar.day_abbr)

    # Create day name headers with equal width
    day_cols = st.columns(7)
    for i, day in enumerate(day_names):
        day_cols[i].markdown(f'<div class="day-header">{day}</div>', unsafe_allow_html=True)

    # Current date tracker
    current_date = start_date

    # Fill initial empty spaces
    start_weekday = start_date.weekday()

    # Track week rows
    while current_date <= end_date:
        # Create a row of columns for the week
        week_cols = st.columns(7)

        # Fill empty spaces for the first week
        if current_date == start_date:
            for i in range(start_weekday):
                week_cols[i].write("")

        # Create buttons for each day of the week
        for col_index in range(7):
            # Skip if we've already processed all dates
            if current_date > end_date:
                break

            # Check if date has a riddle
            date_str = current_date.strftime("%Y-%m-%d")

            # Determine button color based on the date's status
            if current_date == date.today():
                button_color = "#007bff"  # Blue for today
                button_clickable = True
            elif current_date > date.today():
                button_color = "#d3d3d3"  # Lighter gray for future days
                button_clickable = False
            else:
                button_color = "#28a745"  # Green for past days
                button_clickable = False

            # Create button with day and month
            button_text = f"{current_date.day}\n{current_date.strftime('%b')}"

            # Display button
            if button_clickable and week_cols[col_index].button(button_text, key=date_str, type="primary"):
                # Store selected date in session state
                st.session_state['selected_date'] = date_str
                # Navigate to riddle page
                st.switch_page("pages/riddle_page.py")

            # Display button without functionality for past/future days
            if not button_clickable:
                week_cols[col_index].markdown(
                    f'<button class="custom-button" style="background-color:{button_color};">{button_text}</button>',
                    unsafe_allow_html=True
                )

            # Move to next date
            current_date += timedelta(days=1)

            # If we've reached the end of week or end of dates, break
            if col_index == 6 or current_date > end_date:
                break


# Run the calendar
create_calendar()