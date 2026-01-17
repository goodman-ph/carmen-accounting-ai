import streamlit as st
import google.generativeai as genai
from num2words import num2words

st.set_page_config(page_title="Carmen NHS DV Generator", layout="wide")

def format_amount_in_words(amount):
    try:
        pesos = int(amount)
        centavos = int(round((amount - pesos) * 100))
        words = num2words(pesos, lang='en').replace('and', '').title()
        if centavos > 0:
            return f"{words} and {centavos}/100 Pesos Only"
        return f"{words} Pesos Only"
    except:
        return "_________________ Pesos Only"

# --- SIDEBAR INPUTS ---
with st.sidebar:
    st.header("📋 Voucher Details")
    fund_cluster = st.text_input("Fund Cluster", "01 - Regular Agency Fund")
    payee = st.text_input("Payee", value="GSIS")
    address = st.text_input("Address", value="Cabanatuan City, Nueva Ecija")
    tin_no = st.text_input("TIN/Employee No.")
    dv_no = st.text_input("DV No.", placeholder="2026-01-000")
    amount = st.number_input("Amount (PHP)", min_value=0.0, format="%.2f")
    dv_date = st.date_input("Date")

st.title("📑 Full Official DV Generator")
user_input = st.text_area("Transaction Details:", placeholder="e.g., remittance of premiums for Jan 2026")

if st.button("Generate Complete Voucher"):
    if user_input and amount > 0:
        if "GEMINI_API_KEY" not in st.secrets:
            st.error("API Key missing in Secrets!")
            st.stop()
            
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        with st.spinner('🖋️ Processing...'):
            prompt = (
                f"Act as a Senior School Accountant. Generate ONLY the official 'Particulars' text "
                f"for a Disbursement Voucher based on this: {user_input}. "
                f"RULES: 1. Start with 'Payment of...'. 2. One single paragraph. "
                f"3. No bullets. 4. Mention Carmen National High School."
            )
            response = model.generate_content(prompt)
            p_text = response.text.replace("**", "").strip()
            amt_words = format_amount_in_words(amount)

            # --- FAIL-SAFE HTML CONSTRUCTION ---
            # We use a list and join it to prevent "unterminated string" errors.
