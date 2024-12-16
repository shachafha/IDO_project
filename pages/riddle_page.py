import streamlit as st
import json
import random
from datetime import datetime
import base64

# Set page configuration
st.set_page_config(page_title="Daily Riddle", layout="wide")

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
</style>
""", unsafe_allow_html=True)

# Load riddles
with open('riddles.json', 'r') as f:
    riddles = json.load(f)


# Function to create balloon animation
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()


# Navigation buttons
st.markdown("""
<style>
.stButton>button {
    width: 200px;
    height: 50px;
    font-size: 16px;
}
</style>
""", unsafe_allow_html=True)

# Back to calendar button
if st.button("Back to Calendar", type="primary"):
    st.switch_page("main_calendar.py")

# Check if a date is selected
if 'selected_date' not in st.session_state:
    st.error("No date selected. Please go back to the calendar.")
    st.stop()

# Get the selected date's riddle
selected_date = st.session_state['selected_date']
riddle_data = riddles.get(selected_date)

if not riddle_data:
    st.error(f"No riddle found for {selected_date}")
    st.stop()

# Display the riddle
st.title(f"Riddle for {datetime.strptime(selected_date, '%Y-%m-%d').strftime('%B %d, %Y')}")
st.markdown(f"### {riddle_data['riddle']}")

# Input for answer
user_answer = st.text_input("Enter your answer:", key="riddle_answer")

# Submit button
if st.button("Submit Answer", type="primary"):
    # Normalize answers (lowercase, strip whitespace)
    correct_answer = riddle_data['answer'].lower().strip()
    user_answer_normalized = user_answer.lower().strip()

    if user_answer_normalized == correct_answer:
        # Correct answer
        st.success("You did it! 🎉")
        st.balloons()
    else:
        # Incorrect answer
        st.error("Oops! That's not quite right. Try again!")