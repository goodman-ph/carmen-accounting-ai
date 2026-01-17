import streamlit as st
import google.generativeai as genai
from num2words import num2words

# Page Configuration for a professional look
st.set_page_config(page_title="Carmen NHS DV System", layout="centered")

# --- 1. AMOUNT IN WORDS LOGIC ---
def format_amount_in_words(amount):
    try:
        # Splits pesos and centavos for official COA format
        pesos = int(amount)
        centavos = int(round((amount - pesos) * 100))
        words = num2words(pesos, lang='en').replace('and', '').title()
        
        if centavos > 0:
            return f"{words} and {centavos}/100 Pesos Only"
        return f"{words} Pesos Only"
    except:
        return ""

# --- 2. MASTER AI RULES ---
OFFICIAL_TEMPLATE = """
You are the Senior School Accountant for Carmen National High School. 
Generate official particulars for a Disbursement Voucher.
Rule: Start with 'Payment of...' and include Carmen National High School. 
Be concise enough to fit in a standard DV Box.
"""

# --- 3. SIDEBAR DATA ENTRY (Header Data) ---
with st.sidebar:
    st.header("📋 Voucher Headers")
    payee = st.text_input("Payee", value="GSIS")
    address = st.text_input("Address", value="Cabanatuan City, Nueva Ecija")
    tin_no = st.text_input("TIN/Employee No.")
    dv_no = st.text_input("DV No.", placeholder="2026-01-000")
    amount = st.number_input("Amount (PHP)", min_value=0.0, format="%.2f")

# --- 4. MAIN INTERFACE ---
st.title("📑 Official DV Generator")
user_input = st.text_area("Transaction Details:", placeholder="e.g. remittance of employee premiums for Jan 2026")

if st.button("Generate Official Voucher"):
    if user_input and amount > 0:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        response = model.generate_content(f"{OFFICIAL_TEMPLATE}\n\nPROCESS: {user_input}")
        particulars_text = response.text
        words_amount = format_amount_in_words(amount)

        # --- 5. THE PRINTABLE TEMPLATE (HTML/CSS) ---
        # This section creates the boxes that look like your photo
        st.markdown(f"""
        <div style="border: 2px solid black; padding: 15px; background-color: white; color: black; font-family: serif;">
            <div style="text-align: center; font-weight: bold; border-bottom: 1px solid black; padding-bottom: 5px;">
                DISBURSEMENT VOUCHER
            </div>
            
            <table style="width: 100%; border-collapse: collapse;">
                <tr>
                    <td style="border: 1px solid black; padding: 5px; width: 70%;"><b>Payee:</b> {payee}</td>
                    <td style="border: 1px solid black; padding: 5px;"><b>Date:</b> {st.date_input("Date").strftime('%m/%d/%Y')}</td>
                </tr>
                <tr>
                    <td style="border: 1px solid black; padding: 5px;"><b>Address:</b> {address}</td>
                    <td style="border: 1px solid black; padding: 5px;"><b>DV No:</b> {dv_no}</td>
                </tr>
            </table>

            <table style="width: 100%; border-collapse: collapse; margin-top: 10px;">
                <tr style="text-align: center; font-weight: bold;">
                    <td style="border: 1px solid black; padding: 5px; width: 70%;">Particulars</td>
                    <td style="border: 1px solid black; padding: 5px;">Amount</td>
                </tr>
                <tr>
                    <td style="border: 1px solid black; padding: 10px; height: 150px; vertical-align: top;">
                        {particulars_text}
                    </td>
                    <td style="border: 1px solid black; text-align: right; padding: 10px; vertical-align: top; font-weight: bold;">
                        ₱ {amount:,.2f}
                    </td>
                </tr>
            </table>

            <div style="border: 1px solid black; padding: 10px; margin-top: 10px;">
                <b>A. Certified:</b> Expenses/Cash Advance necessary, lawful and incurred under my direct supervision.<br><br>
                <div style="text-align: center;">
                    <b>JESUSA D. BOTE, CESE</b><br>
                    School Principal IV
                </div>
            </div>

            <div style="border: 1px solid black; padding: 10px; margin-top: 10px; background-color: #f9f9f9;">
                <b>D. Approved for Payment:</b><br><br>
                <div style="text-align: center; font-style: italic; font-weight: bold;">
                    {words_amount}
                </div>
            </div>
        </div>
        """, unsafe_allow_value=True)
        
        st.info("💡 To print: Press **Ctrl + P** and set layout to 'Portrait'.")
    else:
        st.error("Please enter both Transaction Details and Amount.")
