import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Carmen NHS AI", layout="wide")
st.title("📑 Carmen NHS Accounting AI")

# Securely load the API Key
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("API Key missing in Streamlit Secrets!")
    st.stop()

# Set up the Brain with a specific model path
system_behavior = """
You are a DepEd School Accountant for Carmen National High School. 
For every input, generate 3 clear sections:
1. ORS Particulars (Start with 'To obligate the...')
2. DV Particulars (Start with 'Payment of...' or 'Remittance of...')
3. JEV Description (Start with 'To record the...')
Use formal COA terminology and mention Carmen NHS.
"""

# Note the 'models/' prefix - this often fixes the 'NotFound' error
model = genai.GenerativeModel(
    model_name='models/gemini-1.5-flash',
    system_instruction=system_behavior
)

user_input = st.text_input("Describe the expense:")

if st.button("Generate Particulars"):
    if user_input:
        try:
            with st.spinner('Gemini is thinking...'):
                response = model.generate_content(user_input)
                st.markdown("### Generated Particulars")
                st.write(response.text)
        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.warning("Please enter an expense description first.")
