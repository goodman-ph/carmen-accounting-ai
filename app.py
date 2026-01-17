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
    fund_cluster = st.text_input("Fund Cluster", "01")
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
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        with st.spinner('🖋️ Finalizing Official Template...'):
            response = model.generate_content(f"Formal DepEd DV particulars for: {user_input}")
            p_text = response.text
            amt_words = format_amount_in_words(amount)

            # BUILDING THE FULL TEMPLATE (BOX A to BOX E)
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
                '<tr><td style="border: 1px solid black; padding: 4px;" colspan="2"><b>Mode of Payment:</b> [ ] MDS Check &nbsp; [ ] Commercial Check &nbsp; [ ] ADA &nbsp; [ ] Others</td></tr>',
                f'<tr><td style="border: 1px solid black; padding: 4px;"><b>Payee:</b> {payee}</td><td style="border: 1px solid black; padding: 4px;"><b>TIN/Emp No:</b> {tin_no}</td></tr>',
                f'<tr><td style="border: 1px solid black; padding: 4px;" colspan="2"><b>Address:</b> {address}</td></tr>',
                '</table>',
                '<table style="width: 100%; border-collapse: collapse; font-size: 11px; color: black; margin-top: -1px;">',
                '<tr style="text-align: center; font-weight: bold;"><td style="border: 1px solid black; width: 50%;">Particulars</td><td style="border: 1px solid black; width: 20%;">Responsibility Center</td><td style="border: 1px solid black;">Amount</td></tr>',
                f'<tr><td style="border: 1px solid black; padding: 8px; height: 120px; vertical-align: top;">{p_text}</td><td style="border: 1px solid black;"></td><td style="border: 1px solid black; text-align: right; padding: 8px; font-weight: bold;">₱ {amount:,.2f}</td></tr>',
                '</table>',
                '<div style="border: 1px solid black; padding: 5px; font-size: 10px; margin-top: -1px;"><b>A. Certified:</b> Expenses/Cash Advance necessary, lawful and incurred under my direct supervision.<br><br><div style="text-align: center;"><b>JESUSA D. BOTE, CESE</b><br>School Principal IV</div></div>',
                '<div style="border: 1px solid black; padding: 5px; font-size: 10px; margin-top: -1px;"><b>B. Accounting Entry:</b><br><table style="width: 100%; border-collapse: collapse; text-align: center; margin-top: 5px;"><tr><td style="border: 1px solid black;">Account Title</td><td style="border: 1px solid black;">UACS Code</td><td style="border: 1px solid black;">Debit</td><td style="border: 1px solid black;">Credit</td></tr><tr><td style="border: 1px solid black; height: 30px;"></td><td style="border: 1px solid black;"></td><td style="border: 1px solid black;"></td><td style="border: 1px solid black;"></td></tr></table></div>',
                '<table style="width: 100%; border-collapse: collapse; font-size: 10px; margin-top: -1px;"><tr>',
                '<td style="border: 1px solid black; width: 50%; padding: 5px; vertical-align: top;"><b>C. Certified:</b><br>[ ] Cash Available<br>[ ] Subject to Authority to Debit Account<br>[ ] Supporting documents complete<br><br><b>GODFREY D. MANGULABNAN</b><br>Sr. Bookkeeper</td>',
                f'<td style="border: 1px solid black; padding: 5px; vertical-align: top;"><b>D. Approved for Payment:</b><br><br><div style="text-align: center; font-style: italic; font-weight: bold;">{amt_words}</div><br><div style="text-align: center;"><b>JESUSA D. BOTE, CESE</b><br>School Principal IV</div></td>',
                '</tr></table>',
                '<div style="border: 1px solid black; padding: 5px; font-size: 10px; margin-top: -1px;"><b>E. Receipt of Payment:</b><br><table style="width: 100%; font-size: 10px;"><tr><td>Check/ADA No: ___________</td><td>Date: ___________</td><td>Bank: ___________</td></tr><tr><td>Signature: ___________</td><td>Date: ___________</td><td>Printed Name: ___________</td></tr></table></div>',
                '</div>'
            ]
            
            st.components.v1.html("".join(html_content), height=900, scrolling=True)
            st.success("✅ Full Voucher Generated!")
    else:
        st.warning("Please enter details and an amount.")
