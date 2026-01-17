import streamlit as st
import google.generativeai as genai

# This pulls your API key safely from Streamlit's Secret settings
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("API Key not found. Please add it to Streamlit Secrets.")

# Set up the AI "Brain"
system_behavior = """
You are a DepEd School Accountant for Carmen National High School. 
Generate 3 distinct boxes for every input:
1. ORS Particulars: Start with 'To obligate the...'
2. DV Particulars: Start with 'Payment of...' or 'Remittance of...'
3. JEV Description: Start with 'To record the...'
Use formal COA terminology. Mention Carmen NHS.
"""

model = genai.GenerativeModel('gemini-1.5-flash', system_instruction=system_behavior)

st.set_page_config(page_title="Carmen NHS AI", layout="wide")
st.title("📑 Carmen NHS Accounting AI")

user_input = st.text_input("Describe the expense (e.g., Fortune Life premiums Jan 2026):")

if st.button("Generate Particulars"):
    if user_input:
        response = model.generate_content(user_input)
        # Displaying the result
        st.write(response.text)
    else:
        st.warning("Please enter an expense first.")
