import streamlit as st
import google.generativeai as genai
from num2words import num2words

# Page Configuration
st.set_page_config(page_title="Carmen NHS DV Generator", layout="centered")

# --- 1. BOX D: AMOUNT IN WORDS LOGIC ---
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

# --- 2. SIDEBAR DATA ENTRY ---
with st.sidebar:
    st.header("📋 Voucher Headers")
    fund_cluster = st.selectbox("Fund Cluster", ["01 - Regular Agency Fund", "07 - Trust Receipts"])
    payee = st.text_input("Payee", value="GSIS")
    address = st.text_input("Address", value="Cabanatuan City, Nueva Ecija")
    dv_no = st.text_input("DV No.", placeholder="2026-01-000")
    amount = st.number_input("Amount (PHP)", min_value=0.0, format="%.2f")
    dv_date = st.date_input("Date")

st.title("📑 Official DV Generator")
user_input = st.text_area("Transaction Details:", placeholder="e.g. remittance of employee premiums for Jan 2026")

if st.button("Generate Official Voucher"):
    if user_input and amount > 0:
        if "GEMINI_API_KEY" not in st.secrets:
            st.error("API Key missing in Secrets!")
            st.stop()
            
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        with st.spinner('🖋️ Drawing Official Template...'):
            # The AI prompt specifically for Carmen NHS
            prompt = f"Generate a formal DepEd accounting particular for Carmen National High School for: {user_input}. Start with 'Payment of...' and keep it concise."
            response = model.generate_content(prompt)
            particulars_text = response.text
            words_amount = format_amount_in_words(amount)

            # --- 3. THE "APPENDIX 32" HTML TEMPLATE ---
            # FIX: We ensure the triple quotes are opened and closed properly
            voucher_html = f"""
<div style="background-color: white; color: black; padding: 20px; border: 2px solid black; font-family: 'Times New Roman', serif; width: 100%; box-sizing: border-box;">
    <div style="text-align: right; font-size: 10px; font-style: italic;">Appendix 32</div>
    <div style="text-align: center; border-bottom: 1px solid black; padding-bottom: 5px; margin-bottom: 10px;">
        <div style="font-size: 11px;">Department of Education - Region III</div>
        <div style="font-weight: bold; font-size: 18px;">DISBURSEMENT VOUCHER</div>
        <div style="font-weight: bold
