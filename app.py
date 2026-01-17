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
Format as a clean professional paragraph suitable for a standard DV box.
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
        # Secure API Check
        if "GEMINI_API_KEY" not in st.secrets:
            st.error("API Key missing in Secrets!")
            st.stop()
            
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        with st.spinner('🖋️ Rendering Official Template...'):
            response = model.generate_content(f"{OFFICIAL_TEMPLATE}\n\nPROCESS: {user_input}")
            particulars_text = response.text
            words_amount = format_amount_in_words(amount)

            # --- 5. THE PRINTABLE TEMPLATE (Fixed Rendering) ---
            # Using f-string to inject your data into a professional HTML grid
            voucher_html = f"""
            <div style="border: 2px solid black; padding: 25px; background-color: white; color: black; font-family: 'Times New Roman', serif; line-height: 1.2;">
                <div style="text-align: center; border-bottom: 2px solid black; padding-bottom: 10px; margin-bottom: 15px;">
                    <div style="font-size: 14px;">Department of Education - Region III</div>
                    <div style="font-weight: bold; font-size: 22px;">DISBURSEMENT VOUCHER</div>
                    <div style="font-size: 16px; font-weight: bold;">CARMEN NATIONAL HIGH SCHOOL</div>
                </div>
                
                <table style="width: 100%; border-collapse: collapse; color: black;">
                    <tr>
                        <td style="border: 1px solid black; padding: 10px; width: 70%;"><b>Payee:</b> {payee}</td>
                        <td style="border: 1px solid black; padding: 10px;"><b>Date:</b> {dv_date.strftime('%m/%d/%Y')}</td>
                    </tr>
                    <tr>
                        <td style="border: 1px solid black; padding: 10px;"><b>Address:</b> {address}</td>
                        <td style="border: 1px solid black; padding: 10px;"><b>DV No:</b> {dv_no}</td>
                    </tr>
                </table>

                <table style="width: 100%; border-collapse: collapse; margin-top: 15px; color: black;">
                    <tr style="text-align: center; font-weight: bold; background-color: #f2f2f2;">
                        <td style="border: 1px solid black; padding: 10px; width: 75%;">Particulars</td>
                        <td style="border: 1px solid black; padding: 10px;">Amount</td>
                    </tr>
                    <tr>
                        <td style="border: 1px solid black; padding: 20px; height: 220px; vertical-align: top; font-size: 15px;">
                            {particulars_text}
                        </td>
                        <td style="border: 1px solid black; text-align: right; padding: 20px; vertical-align: top; font-weight: bold; font-size: 20px;">
                            ₱ {amount:,.2f}
                        </td>
                    </tr>
                </table>

                <div style="border: 1px solid black; padding: 15px; margin-top: 15px; color: black;">
                    <div style="font-size: 13px;"><b>A. Certified:</b> Expenses/Cash Advance necessary, lawful and incurred under my direct supervision.</div>
                    <br><br>
                    <div style="text-align: center;">
                        <span style="text-decoration: underline; font-weight: bold; font-size: 16px;">JESUSA D. BOTE, CESE</span><br>
                        <span style="font-size: 14px;">School Principal IV</span>
                    </div>
                </div>

                <div style="border: 1px solid black; padding: 15px; margin-top: 15px; background-color: #f9f9f9; color: black; border-left: 10px solid #ddd;">
                    <div style="font-size: 13px;"><b>D. Approved for Payment:</b></div>
                    <div style="text-align: center; font-style: italic; font-weight: bold; font-size: 18px; padding: 15px;">
                        {words_amount}
                    </div>
                </div>
            </div>
            """
            
            # CRITICAL: This is what turns the code into the actual template
            st.markdown(voucher_html, unsafe_allow_html=True)
            
            st.success("✅ Voucher Rendered! Press Ctrl+P to print.")
    else:
        st.error("Please enter details and an amount.")
