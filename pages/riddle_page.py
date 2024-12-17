import streamlit as st
import json
from datetime import datetime

# Set page configuration
st.set_page_config(page_title="חידת היום", layout="wide")

# Hide Streamlit default sidebar and set RTL styling
st.markdown("""
<style>
    [data-testid="stSidebar"][aria-expanded="true"] > div:first-child {
        visibility:hidden;
        width: 0px;
    }
    [data-testid="stSidebar"][aria-expanded="false"] > div:first-child {
        visibility:hidden;
    }
    /* RTL styling */
    .rtl {
        direction: rtl;
        text-align: right;
        font-family: Arial, sans-serif;
    }
    /* Right-align buttons */
    .stButton>button {
        width: 200px;
        height: 50px;
        font-size: 16px;
        background-color: #A7C7E7 !important;
        color: black;
        float: right;
        border: none; 
        margin: 10px 0;
    }
    /* Right-align input box label */
    label[data-testid="stLabel"] {
        text-align: right;
        display: block;
        font-size: 18px;
        font-weight: bold;
        direction: rtl;
    }
    /* Align content spacing */
    .block-container {
        direction: rtl;
    }
</style>
""", unsafe_allow_html=True)

# Load riddles
with open('riddles.json', 'r') as f:
    riddles = json.load(f)

# Function to get query parameters from the URL
def get_query_param(param):
    query_string = st.query_params
    return query_string.get(param, None)

# Back to calendar button aligned to the right
st.markdown("<div style='text-align: right;'>", unsafe_allow_html=True)
if st.button("חזרה ללוח", type="primary"):
    st.switch_page("main_calendar.py")
st.markdown("</div>", unsafe_allow_html=True)

# Extract the selected date from query parameters
selected_date = get_query_param("date")

if not selected_date:
    st.error("לא נבחר תאריך. חזור ללוח.")
    st.stop()

# Validate the date format
try:
    datetime.strptime(selected_date, '%Y-%m-%d')
except ValueError:
    st.error("פורמט תאריך לא תקין. חזור ללוח.")
    st.stop()

# Get the selected date's riddle
riddle_data = riddles.get(selected_date)

if not riddle_data:
    st.error(f"לא נמצאה חידה עבור {selected_date}")
    st.stop()

# Display the riddle in RTL
st.markdown(f"<h1 class='rtl'>חידת היום - {datetime.strptime(selected_date, '%Y-%m-%d').strftime('%d/%m/%Y')}</h1>", unsafe_allow_html=True)
st.markdown(f"<div class='rtl'><h3>{riddle_data['riddle']}</h3></div>", unsafe_allow_html=True)

# Input for answer with aligned label
user_answer = st.text_input("כתוב את תשובתך כאן:", key="riddle_answer", label_visibility="visible")

# Submit button aligned to the right
st.markdown("<div style='text-align: right;'>", unsafe_allow_html=True)
if st.button("שלח תשובה", type="primary"):
    # Normalize answers (lowercase, strip whitespace)
    correct_answer = riddle_data['answer'].lower().strip()
    user_answer_normalized = user_answer.lower().strip()

    # Check answer
    if user_answer_normalized == correct_answer:
        st.success("כל הכבוד! 🎉")
        st.balloons()
    else:
        st.error("טעות. נסה שוב!")
st.markdown("</div>", unsafe_allow_html=True)
