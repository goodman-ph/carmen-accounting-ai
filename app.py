import streamlit as st
import google.generativeai as genai
from num2words import num2words

# 1. Page Config
st.set_page_config(page_title="Carmen NHS DV Generator", layout="centered")

# 2. Amount Logic
def format_amount_in_words(amount):
    try:
        pesos = int(amount)
        centavos = int(round((amount - pesos) * 100))
        words = num2words(pesos, lang='en').replace('and', '').title()
        if centavos > 0:
            return words + " and " + str(centavos) + "/100 Pesos Only"
        return words + " Pesos Only"
    except:
        return "_________________ Pesos Only"

# 3. Sidebar Inputs
with st.sidebar:
    st.header("📋 Voucher Details")
    f_cluster = st.text_input("Fund Cluster", "01")
    f_payee = st.text_input("Payee", "GSIS")
    f_address = st.text_input("Address", "Cabanatuan City")
    f_dv_no = st.text_input("DV No.", placeholder="2026-01-000")
    f_amount = st.number_input("Amount (PHP)", min_value=0.0, format="%.2f")
    f_date = st.date_input("Date")

st.title("📑 Official DV Generator")
u_input = st.text_area("Transaction Details:", placeholder="e.g., GSIS January Premiums")

if st.button("Generate Complete Voucher"):
    if u_input and f_amount > 0:
        try:
            if "GEMINI_API_KEY" not in st.secrets:
                st.error("API Key missing in Secrets!")
                st.stop()
            
            genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
            model = genai.GenerativeModel('gemini-2.0-flash')
            
            with st.spinner('Generating...'):
                prompt = "Write a 1-paragraph DepEd accounting particular for " + u_input + " at Carmen National High School. Start with 'Payment of'."
                response = model.generate_content(prompt)
                p_text = response.text.replace("**", "").strip()
                amt_words = format_amount_in_words(f_amount)

                # 4. THE TEMPLATE (No f-strings used here to avoid SyntaxErrors)
                html_template = """
<div style="background-color: white; color: black; padding: 25px; border: 3px solid black; font-family: 'Times New Roman', serif; width: 700px; margin: auto; line-height: 1.2;">
    <div style="text-align: right; font-size: 10px; font-style: italic;">Appendix 32</div>
    <div style="text-align: center; border-bottom: 2px solid black; padding-bottom: 10px; margin-bottom: 10px;">
        <div style="font-size: 12px;">Department of Education - Region III</div>
        <div style="font-weight: bold; font-size: 20px;">DISBURSEMENT VOUCHER</div>
        <div style="font-weight: bold; font-size: 15px;">CARMEN NATIONAL HIGH SCHOOL</div>
    </div>
    <table style="width: 100%; border-collapse: collapse; font-size: 12px;">
        <tr>
            <td style="border: 1px solid black; padding: 8px;"><b>Fund Cluster:</b> [FUND]</td>
            <td style="border: 1px solid black; padding: 8px;"><b>Date:</b> [DATE]<br><b>DV No:</b> [DV_NO]</td>
        </tr>
        <tr>
            <td style="border: 1px solid black; padding: 8px;" colspan="2"><b>Payee:</b> [PAYEE] | <b>Address:</b> [ADDR]</td>
        </tr>
    </table>
    <table style="width: 100%; border-collapse: collapse; font-size: 12px; margin-top: -1px;">
        <tr style="text-align: center; font-weight: bold;">
            <td style="border: 1px solid black; padding: 5px; width: 70%;">Particulars</td>
            <td style="border: 1px solid black; padding: 5px;">Amount</td>
        </tr>
