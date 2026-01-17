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
        
        with st.spinner('🖋️ Cleaning Particulars...'):
            prompt = (
                f"Act as a Senior School Accountant. Generate ONLY the official 'Particulars' text "
                f"for a Disbursement Voucher based on this: {user_input}. "
                f"RULES: 1. Start with 'Payment of...'. 2. One single paragraph. "
                f"3. No bullets or headers. 4. Mention Carmen National High School."
            )
            response = model.generate_content(prompt)
            p_text = response.text.replace("**", "").strip()
            amt_words = format_amount_in_words(amount)

            # BUILDING THE FULL TEMPLATE - FIXED ALL STRING LITERALS
            html_content = [
                '<div style="background-color: white; color: black; padding: 15px; border: 2px solid black; font-family: serif; width: 850px; margin: auto; line-height: 1.1;">',
                '<div style="text-align: right; font-size: 10px; font-style: italic;">Appendix 32</div>',
                '<div style="text-align: center; border-bottom: 1px solid black; padding-bottom: 5px; margin-bottom: 5px;">',
                '<div style="font-size: 11px;">Department of Education - Region III</div>',
                '<div style="font-weight: bold; font-size: 18px;">DISBURSEMENT VOUCHER</div>',
                '<div style="font-weight: bold; font-size: 14px;">CARMEN NATIONAL HIGH SCHOOL</div>',
                '</div>',
                '<table style="width: 100%; border-collapse: collapse; font-size: 11px; color: black;">',
                f'<tr><td style="border: 1px solid black; padding: 4px; width: 75%;"><b>Fund Cluster:</b> {fund_cluster}</td><td style="border: 1px solid black; padding: 4px;"><b>Date:</b> {dv_date} <br> <b>DV No:</b> {dv_no}</td></tr>',
                '<tr><td style="border: 1px solid black; padding: 4px;" colspan="2"><b>Mode of
