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
    # Using the stable 2.5-flash for the best 2026 performance
    model = genai.GenerativeModel('gemini-2.5-flash')
except Exception as e:
    st.error(f"Model setup error: {e}")

# 3. Official Master Template (LOCKED RULES)
OFFICIAL_TEMPLATE = """
You are the Senior School Accountant for Carmen National High School. 
Generate uniform particulars following these Philippine COA/DepEd standards:

RULES:
1. ORS (Obligation Request): 
   - Start with: "To recognize obligation for [Expense Name] of [Payee]..."
   - Mention the year and PPA/Activity if provided.

2. DV (Disbursement Voucher): 
   - Start with: "Payment of [Expense Name] for [Payee] for the period [Date] per [Supporting Docs]..."
   - Do NOT say "To record payment"; start directly with "Payment of..."

3. JEV (Journal Entry Voucher):
   - Description: "To record [Transaction Name] for the month of [Month]..."
   - Provide the Table: Account Title | UACS Code | Debit | Credit.

4. MANDATORY: 
   - Always include the name "Carmen National High School".
   - Use UACS codes: Water (5020401000), Electricity (5020402000), Internet (5020503000).
"""

# 4. User Interface
st.info("💡 **Instructions:** Enter transaction details to generate uniform official particulars.")

user_input = st.text_input("Enter Details (e.g., Water bill Jan 2026, Bill #123, 1,500 pesos):")

if st.button("Generate Official Particulars"):
    if user_input:
        try:
            with st.spinner('🖋️ Drafting uniform particulars...'):
                # Combine the rules with the user's input
                final_prompt = f"{OFFICIAL_TEMPLATE}\n\nTRANSACTION TO PROCESS: {user_input}"
                
                response = model.generate_content(final_prompt)
                
                st.success("✅ Uniformed Particulars Generated!")
                st.divider()
                st.markdown(response.text)
                
        except Exception as e:
            st.error(f"⚠️ Connection Error: {e}")
    else:
        st.warning("⚠️ Please enter details first.")

# Footer
st.markdown("---")
st.caption("Note: This is an AI-assisted drafting tool for Carmen NHS. Verify against latest COA/DepEd guidelines.")
