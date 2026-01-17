import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Carmen NHS AI", layout="wide")
st.title("📑 Carmen NHS Accounting Particulars Generator")

if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("API Key missing! Add it to Streamlit Secrets.")
    st.stop()

# This list covers the most common names for the Flash model
# The app will try the first one, and move to the next if it hits a 404
model_names = ['gemini-1.5-flash', 'gemini-1.5-flash-latest', 'gemini-pro']

st.markdown("---")
user_input = st.text_input("Enter Expense Details:")

if st.button("Generate All Particulars"):
    if user_input:
        success = False
        for m_name in model_names:
            try:
                model = genai.GenerativeModel(m_name)
                prompt = f"As a DepEd Accountant for Carmen NHS, generate ORS, DV, and JEV particulars for: {user_input}. Format them clearly."
                
                with st.spinner(f'Trying model {m_name}...'):
                    response = model.generate_content(prompt)
                    st.success(f"Success using {m_name}!")
                    st.markdown(response.text)
                    success = True
                    break # Stop trying models once one works
            except Exception as e:
                continue # Try the next model in the list
        
        if not success:
            st.error("All models failed. Please check if your API Key is restricted to a specific region or project in Google AI Studio.")
    else:
        st.warning("Please type an expense description.")
