import streamlit as st
import google.generativeai as genai
from num2words import num2words

st.set_page_config(page_title="Carmen NHS DV Generator", layout="centered")

def format_amount_in_words(amount):
    try:
        pesos = int(amount)
        centavos = int(round((amount - pesos) * 100))
        words = num2words(pesos, lang='en').replace('and', '').title()
        if centavos > 0: return f"{words} and {centavos}/100 Pesos Only"
        return f"{words} Pesos Only"
    except: return "_________________ Pesos Only"

# --- SIDEBAR ---
with st.sidebar:
    st.header("📋 Voucher Details")
    fund_cluster = st.text_input("Fund Cluster", "01")
    payee = st.text_input("Payee", value="GSIS")
    address = st.text_input("Address", value="Cabanatuan City")
    dv_no = st.text_input("DV No.", placeholder="2026-01-000")
    amount = st.number_input("Amount (PHP)", min_value=0.0, format="%.2f")
    dv_date = st.date_input("Date")

st.title("📑 Official DV Generator")
user_input = st.text_area("Transaction Details:", placeholder="e.g., GSIS January Premiums")

if st.button("Generate Complete Voucher"):
    if not user_input or amount <= 0:
        st.error("❌ Please enter both details and an amount.")
    else:
        try:
            if "GEMINI_API_KEY" not in st.secrets:
                st.error("🔑 API Key not found in Streamlit Secrets!")
                st.stop()
                
            genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
            
            # Updated to gemini-2.0-flash for better compatibility
            model = genai.GenerativeModel('gemini-2.0-flash')
            
            with st.spinner('🖋️ Generating Particulars...'):
                prompt = f"Write a 1-paragraph DepEd particulars for {user_input} for Carmen National High School. Start with 'Payment of'."
                response = model.generate_content(prompt)
                p_text = response.text.replace("**", "").strip()
                amt_words = format_amount_in_words(amount)

            # --- THE FULL VOUCHER HTML ---
            # We use a single string to avoid syntax errors
            voucher_html = f"""
            <div style="background-color: white; color: black; padding: 25px; border: 2px solid black; font-family: 'Times New Roman', serif; width: 700px; margin: auto; line-height: 1.2;">
                <div style="text-align: right; font-size: 10px; font-style: italic;">Appendix 32</div>
                <div style="text-align: center; border-bottom: 2px solid black; padding-bottom: 5px;">
                    <div style="font-size: 12px;">Department of Education - Region III</div>
                    <div style="font-weight: bold; font-size: 18px;">DISBURSEMENT VOUCHER</div>
                    <div style="font-weight: bold; font-size: 14px;">CARMEN NATIONAL HIGH SCHOOL</div>
                </div>

                <table style="width: 100%; border-collapse: collapse; font-size: 11px; margin-top: 5px;">
                    <tr>
                        <td style="border: 1px solid black; padding: 5px; width: 70%;"><b>Fund Cluster:</b> {fund_cluster}</td>
                        <td style="border: 1px solid black; padding: 5px;"><b>Date:</b> {dv_date}<br><b>DV No:</b> {dv_no}
