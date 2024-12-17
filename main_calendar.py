import streamlit as st
import calendar
from datetime import date, timedelta
import json
import base64

# Function to convert an image file to base64 encoding
def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Function to set the background using base64 encoded image
def set_background(png_file):
    bin_str = get_base64(png_file)
    page_bg_img = f'''
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{bin_str}");
        background-size: cover;
        background-attachment: local;
    }}
    </style>
    '''
    st.markdown(page_bg_img, unsafe_allow_html=True)

# Set the background image (update the file path as needed)
set_background('image_back.jpeg')

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
    day_names = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']

    # Create a list to represent the calendar (rows and columns)
    calendar_table = []

    # Add day names header
    calendar_table.append(day_names)

    # Current date tracker
    current_date = start_date
    col_index = start_date.weekday()  # Start position based on the weekday

    # Create the calendar grid with buttons for each day
    row = [""] * 7  # Initialize an empty row for the first week

    while current_date <= end_date:
        if col_index < 7:
            date_str = current_date.strftime("%Y-%m-%d")
            has_riddle = date_str in riddles

            # Determine button color based on the date's status
            if current_date == date.today():
                button_color = "#A7C7E7"  # Pastel blue
                button_clickable = True
                button_text = f"{current_date.day}\n{current_date.strftime('%b')}"
                button_html = f"""
                <a href='/riddle_page?date={date_str}' target='_self'>
                    <button style='background-color:{button_color}; width: 100%; height: 60px; font-size: 15px; color: black; border: none; border-radius: 12px;'>
                        {button_text}
                    </button>
                </a>
                """
            elif current_date > date.today():
                button_color = "#D1D1D1"  # Pastel gray
                button_clickable = False
                button_text = f"{current_date.day}\n{current_date.strftime('%b')}"
                button_html = f"""
                <button style='background-color:{button_color}; width: 100%; height: 60px; font-size: 15px; color: black; border: none; border-radius: 12px;' disabled>
                    {button_text}
                </button>
                """
            else:
                button_color = "#A8E6CF"  # Pastel green
                button_clickable = False
                button_text = f"{current_date.day}\n{current_date.strftime('%b')}"
                button_html = f"""
                <button style='background-color:{button_color}; width: 100%; height: 60px; font-size: 15px;color: black; border: none; border-radius: 12px;' disabled>
                    {button_text}
                </button>
                """

            # Add the button HTML to the calendar grid
            row[col_index] = button_html

            # Move to next date
            current_date += timedelta(days=1)
            col_index += 1
        else:
            # Add the row to the calendar table and reset
            calendar_table.append(row)
            row = [""] * 7
            col_index = 0

    # If there's any remaining row (not yet added), add it
    if any(row):
        calendar_table.append(row)

    # Create a markdown table representation of the calendar
    table_html = "<table style='width: 50%; border-collapse: collapse; margin: auto;'>"
    for row in calendar_table:
        table_html += "<tr>"
        for day in row:
            table_html += f"<td style='text-align: center; padding: 1px; border: none;'>{day}</td>"
        table_html += "</tr>"
    table_html += "</table>"

    st.markdown(table_html, unsafe_allow_html=True)

# Run the calendar
create_calendar()
