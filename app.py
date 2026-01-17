import streamlit as st
import google.generativeai as genai
from num2words import num2words

st.set_page_config(page_title="Carmen NHS DV Generator", layout="centered")

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
            st.error("API Key missing!")
            st.stop()
        
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        with st.spinner('🖋️ Drawing...'):
            prompt = f"Generate a formal DepEd accounting particular for Carmen National High School: {user_input}. Start with 'Payment of...'"
            response = model.generate_content(prompt)
            p_text = response.text
            amt_words = format_amount_in_words(amount)

            # FAIL-SAFE METHOD: Building the HTML piece by piece to avoid SyntaxErrors
            html_parts = [
                '<div style="background-color: white; color: black; padding: 20px; border: 2px solid black; font-family: serif; width: 100%;">',
                '<div style="text-align: right; font-size: 10px; font-style: italic;">Appendix 32</div>',
                '<div style="text-align: center; border-bottom: 1px solid black; padding-bottom: 10px; margin-bottom: 10px;">',
                '<div style="font-size: 11px;">Department of Education - Region III</div>',
                '<div style="font-weight: bold; font-size: 18px;">DISBURSEMENT VOUCHER</div>',
                '<div style="font-weight: bold; font-size: 14px;">CARMEN NATIONAL HIGH SCHOOL</div>',
                '</div>',
                '<table style="width: 100%; border-collapse: collapse; font-size: 12px; color: black;">',
                f'<tr><td style="border: 1px solid black; padding: 5px;" colspan="2"><b>Fund Cluster:</b> {fund_cluster}</td>',
                f'<td style="border: 1px solid black; padding: 5px;"><b>Date:</b> {dv_date.strftime("%m/%d/%Y")}<br><b>DV No:</b> {dv_no}</td></tr>',
                '<tr><td style="border: 1px solid black; padding: 5px;" colspan="3"><b>Mode of Payment:</b> [ ] MDS Check &nbsp;&nbsp; [ ] Commercial Check &nbsp;&nbsp; [ ] ADA &nbsp;&nbsp; [ ] Others</td></tr>',
                f'<tr><td style="border: 1px solid black; padding: 5px;" colspan="3"><b>Payee:</b> {payee}<br><b>Address:</b> {address}</td></tr>',
                '<tr style="text-align: center; font-weight: bold; background-color: #f2f2f2;">',
                '<td style="border: 1px solid black; padding: 5px; width: 50%;">Particulars</td>',
                '<td style="border: 1px solid black; padding: 5px; width: 25%;">Responsibility Center</td>',
                '<td style="border: 1px solid black; padding: 5px; width: 25%;">Amount</td></tr>',
                f'<tr><td style="border: 1px solid black; padding: 10px; height: 180px; vertical-align: top;">{p_text}</td>',
                '<td style="border: 1px solid black;"></td>',
                f'<td style="border: 1px solid black; text-align: right; padding: 10px; vertical-align: top; font-weight: bold;">₱ {amount:,.2f}</td></tr>',
                '</table>',
                '<div style="border: 1px solid black; padding: 10px; font-size: 11px; margin-top: 5px;">',
                '<b>A. Certified:</b> Expenses/Cash Advance necessary, lawful and incurred under my direct supervision.<br><br>',
                '<div style="text-align: center;"><b>JESUSA D. BOTE, CESE</b><br>School Principal IV</div>',
                '</div>',
                '<div style="border: 1px solid black; padding: 10px; background-color: #f9f9f9; font-size: 11px; margin-top: 5px;">',
                f'<b>D. Approved for Payment:</b><br><br><div style="text-align: center; font-style: italic; font-weight: bold; font-size: 13px;">{amt_words}</div>',
                '</div>',
                '</div>'
            ]
            
            # Combine all parts into one clean string
            voucher_html = "".join(html_parts)
            
            st.components.v1.html(voucher_html, height=750, scrolling=True)
            st.success("✅ Voucher Generated Successfully!")
    else:
        st.warning("Please enter transaction details and an amount.")
