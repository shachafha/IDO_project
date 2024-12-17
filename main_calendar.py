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

    /* Responsive calendar grid */
    [data-testid="stColumns"] {
        display: grid !important;
        grid-template-columns: repeat(7, 1fr) !important;
        gap: 5px !important;
        width: 100% !important;
    }

    /* Ensure all column children maintain grid layout */
    [data-testid="stColumns"] > div {
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        width: 100% !important;
        margin: 0 !important;
        padding: 2px !important;
        box-sizing: border-box !important;
    }

    /* Calendar day buttons */
    .custom-button {
        width: 100% !important;
        aspect-ratio: 1 / 1 !important;
        min-height: 50px !important;
        max-height: 150px !important;
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

    /* Responsive text sizing */
    @media (max-width: 600px) {
        [data-testid="stColumns"] {
            grid-template-columns: repeat(7, 1fr) !important;
            gap: 3px !important;
        }

        .custom-button {
            font-size: 12px !important;
            min-height: 40px !important;
        }

        /* Center day names */
        [data-testid="stColumns"] > div > h3 {
            margin: 0 !important;
            font-size: 12px !important;
        }
    }

    @media (max-width: 400px) {
        .custom-button {
            font-size: 10px !important;
            min-height: 35px !important;
        }
    }

    /* Big font class */
    .big-font {
        font-size: 20px !important;
        text-align: center !important;
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
        if button_clickable and cols[col_index].button(button_text, key=date_str, type="primary"):
            # Store selected date in session state
            st.session_state['selected_date'] = date_str
            # Navigate to riddle page
            st.switch_page("pages/riddle_page.py")

        # Display button without functionality for past/future days
        if not button_clickable:
            cols[col_index].markdown(
                f'<button class="custom-button" style="background-color:{button_color};">{button_text}</button>',
                unsafe_allow_html=True
            )

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