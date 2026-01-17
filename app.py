import streamlit as st
import google.generativeai as genai

# Page Config
st.set_page_config(page_title="Carmen NHS Accounting AI", layout="wide", page_icon="📑")

# Custom Styling
st.markdown("""
    <style>
    .main {
        background-color: #f5f7f9;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #007bff;
        color: white;
    }
    </style>
    """, unsafe_allow_value=True)

st.title("📑 Carmen NHS Accounting Particulars Generator")
st.subheader("Official DepEd School Accounting Tool")

# 1. Secure API Configuration
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("❌ API Key Missing! Please add it to Streamlit Secrets.")
    st.stop()

# 2. Model Initialization (Using the stable 1.5 Flash)
try:
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"Model error: {e}")

# 3. User Interface
st.info("💡 **Instructions:** Enter the nature of the expense below. The AI will generate the professional particulars used in DepEd Accounting.")

user_input = st.text_input("Enter Transaction Details (e.g., Payment for Water Bill Nov 2025 or Loyalty Award for Juan Dela Cruz):")

if st.button("Generate All Particulars"):
    if user_input:
        try:
            with st.spinner('🖋️ Drafting professional particulars...'):
                # The Professional Prompt
                prompt = (
                    f"You are a Senior DepEd Accountant at Carmen National High School. "
                    f"Generate professional accounting particulars for the following transaction: {user_input}. "
                    "Provide 3 specific sections using formal DepEd terminology: "
                    "1. ORS (Obligation Request and Status): Format as 'To record obligation for...' "
                    "2. DV (Disbursement Voucher): Format as 'To record payment of...' "
                    "3. JEV (Journal Entry Voucher): Provide the brief Description/Explanation. "
                    "Use clear, concise, and official language."
                )
                
                response = model.generate_content(prompt)
                
                # Display Results in organized containers
                st.success("✅ Particulars Generated Successfully!")
                st.divider()
                
                # Show the output
                st.markdown(response.text)
                
                st.divider()
                st.caption("⚠️ **Note:** Please review the generated text against the latest COA and DepEd guidelines before printing.")

        except Exception as e:
            st.error("⚠️ Connection Error")
            st.info(f"Details: {e}")
            st.write("Tip: If you see a '404', wait 3 minutes for your API key to activate and refresh the page.")
    else:
        st.warning("⚠️ Please enter transaction details first.")

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center;'>Carmen National High School | Accounting Department</p>", unsafe_allow_value=True)
