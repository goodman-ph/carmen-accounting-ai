import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Carmen NHS AI", layout="wide")
st.title("📑 Carmen NHS Accounting AI")

# Secure API Configuration
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("Missing API Key! Please go to Streamlit Settings > Secrets.")
    st.stop()

# We use the most basic model ID to avoid the 404 error
# This version is highly compatible with new API keys
try:
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
except Exception as e:
    st.error(f"Model setup failed: {e}")

st.info("System Instruction: Acting as DepEd Accountant for Carmen NHS.")

user_input = st.text_input("Enter Expense Details (e.g. Loyalty Award for Ador Dionisio):")

if st.button("Generate Particulars"):
    if user_input:
        try:
            # Simple, direct prompt
            response = model.generate_content(
                f"As a DepEd School Accountant, write the ORS, DV, and JEV particulars for: {user_input} at Carmen National High School."
            )
            
            # Divide the output into columns for better viewing
            st.success("Results Generated!")
            st.markdown("---")
            st.markdown(response.text)
            
        except Exception as e:
            st.error("⚠️ Connection Error")
            st.write(f"Server Message: {e}")
            st.info("If you see '404', your API Key is still propagating. Please wait 3-5 minutes and try again.")
    else:
        st.warning("Please type something first.")
