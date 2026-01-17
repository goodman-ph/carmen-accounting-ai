import streamlit as st
import google.generativeai as genai

# Page Config
st.set_page_config(page_title="Carmen NHS Accounting AI", layout="wide", page_icon="📑")

st.title("📑 Carmen NHS Accounting Particulars Generator")
st.subheader("Official DepEd School Accounting Tool")

# 1. Secure API Configuration
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("❌ API Key Missing! Please add it to Streamlit Secrets.")
    st.stop()

# 2. Model Initialization
try:
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"Model setup error: {e}")

# 3. User Interface
st.info("💡 **Instructions:** Enter the nature of the expense below to generate formal particulars.")

user_input = st.text_input("Enter Transaction Details (e.g., Payment for Water Bill Nov 2025):")

if st.button("Generate All Particulars"):
    if user_input:
        try:
            with st.spinner('🖋️ Drafting professional particulars...'):
                prompt = (
                    f"You are a Senior DepEd Accountant at Carmen National High School. "
                    f"Generate professional accounting particulars for: {user_input}. "
                    "Provide 3 specific sections: "
                    "1. ORS (Obligation Request and Status): 'To record obligation for...' "
                    "2. DV (Disbursement Voucher): 'To record payment of...' "
                    "3. JEV (Journal Entry Voucher): Brief Explanation."
                )
                
                response = model.generate_content(prompt)
                st.success("✅ Generated Successfully!")
                st.markdown("---")
                st.markdown(response.text)
                st.divider()
                st.caption("Review against COA guidelines before printing.")

        except Exception as e:
            st.error(f"⚠️ Connection Error: {e}")
    else:
        st.warning("⚠️ Please enter details first.")
