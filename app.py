import streamlit as st
import google.generativeai as genai
from num2words import num2words

# Page Configuration
st.set_page_config(page_title="Carmen NHS DV System", layout="centered")

# --- 1. OFFICIAL AMOUNT IN WORDS (Box D Format) ---
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

# --- 2. MASTER AI RULES ---
OFFICIAL_TEMPLATE = """
You are the Senior School Accountant for Carmen National High School. 
Generate official particulars for a Disbursement Voucher.
Rule: Start with 'Payment of...' and include Carmen National High School. 
Format as a clean professional paragraph.
"""

# --- 3. SIDEBAR DATA ENTRY ---
with st.sidebar:
    st.header("📋 Voucher Headers")
    payee = st.text_input("Payee", value="GSIS")
    address = st.text_input("Address", value="Cabanatuan City, Nueva Ecija")
    tin_no = st.text_input("TIN/Employee No.")
    dv_no = st.text_input("DV No.", placeholder="2026-01-000")
    amount = st.number_input("Amount (PHP)", min_value=0.0, format="%.2f")
    dv_date = st.date_input("Date")

# --- 4. MAIN INTERFACE ---
st.title("📑 Official DV Generator")
user_input = st.text_area("Transaction Details:", placeholder="e.g. remittance of employee premiums for Jan 2026")

if st.button("Generate Official Voucher"):
    if user_input and amount > 0:
        # Check for API Key
        if "GEMINI_API_KEY" not in st.secrets:
            st.error("API Key missing in Secrets!")
            st.stop()
            
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        with st.spinner('Building Voucher...'):
            response = model.generate_content(f"{OFFICIAL_TEMPLATE}\n\nPROCESS: {user_input}")
            particulars_text = response.text
            words_amount = format_amount_in_words(amount)

            # --- 5. THE PRINTABLE TEMPLATE (Fixed unsafe_allow_html) ---
            st.markdown(f"""
            <div style="border: 2px solid black; padding: 20px; background-color: white; color: black; font-family: 'Times New Roman', serif;">
                <div style="text-align: center; font-weight: bold; font-size: 20px; border-bottom: 2px solid black; padding-bottom: 10px; margin-bottom: 10px;">
                    DISBURSEMENT VOUCHER
                </div>
                
                <table style="width: 100%; border-collapse: collapse; color: black;">
                    <tr>
                        <td style="border: 1px solid black; padding: 8px; width: 70%;"><b>Payee:</b> {payee}</td>
                        <td style="border: 1px solid black; padding: 8px;"><b>Date:</b> {dv_date.strftime('%m/%d/%Y')}</td>
                    </tr>
                    <tr>
                        <td style="border: 1px solid black; padding: 8px;"><b>Address:</b> {address}</td>
                        <td style="border: 1px solid black; padding: 8px;"><b>DV No:</b> {dv_no}</td>
                    </tr>
                </table>

                <table style="width: 100%; border-collapse: collapse; margin-top: 10px; color: black;">
                    <tr style="text-align: center; font-weight: bold; background-color: #f2f2f2;">
                        <td style="border: 1px solid black; padding: 8px; width: 75%;">Particulars</td>
                        <td style="border: 1px solid black; padding: 8px;">Amount</td>
                    </tr>
                    <tr>
                        <td style="border: 1px solid black; padding: 15px; height: 180px; vertical-align: top; line-height: 1.5;">
                            {particulars_text}
                        </td>
                        <td style="border: 1px solid black; text-align: right; padding: 15px; vertical-align: top; font-weight: bold; font-size: 18px;">
                            ₱ {amount:,.2f}
                        </td>
                    </tr>
                </table>

                <div style="border: 1px solid black; padding: 15px; margin-top: 10px; color: black;">
                    <b>A. Certified:</b> Expenses/Cash Advance necessary, lawful and incurred under my direct supervision.<br><br><br>
                    <div style="text-align: center;">
                        <span style="text-decoration: underline; font-weight: bold;">JESUSA D. BOTE, CESE</span><br>
                        School Principal IV
                    </div>
                </div>

                <div style="border: 1px solid black; padding: 15px; margin-top: 10px; background-color: #f9f9f9; color: black;">
                    <b>D. Approved for Payment:</b><br><br>
                    <div style="text-align: center; font-style: italic; font-weight: bold; font-size: 16px;">
                        {words_amount}
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.success("✅ Form Generated! Press Ctrl+P to Print.")
    else:
        st.error("Please enter both Transaction Details and a valid Amount.")
