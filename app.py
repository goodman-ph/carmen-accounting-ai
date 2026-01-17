import streamlit as st
import google.generativeai as genai
from num2words import num2words

# Page Configuration
st.set_page_config(page_title="Carmen NHS DV System", layout="centered")

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
    payee = st.text_input("Payee", value="GSIS")
    address = st.text_input("Address", value="Cabanatuan City, Nueva Ecija")
    dv_no = st.text_input("DV No.", placeholder="2026-01-000")
    amount = st.number_input("Amount (PHP)", min_value=0.0, format="%.2f")
    dv_date = st.date_input("Date")

st.title("📑 Official DV Generator")
user_input = st.text_area("Transaction Details:", placeholder="e.g. remittance of employee premiums for Jan 2026")

if st.button("Generate Official Voucher"):
    if user_input and amount > 0:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        with st.spinner('🖋️ Drawing Official Template...'):
            # AI generating the Particulars text
            response = model.generate_content(f"Generate a professional DepEd accounting particular for: {user_input}. Start with 'Payment of...'")
            particulars_text = response.text
            words_amount = format_amount_in_words(amount)

            # --- 3. THE COMPLETE HTML TEMPLATE ---
            # We put everything inside one big HTML block
            voucher_html = f"""
            <div style="border: 2px solid black; padding: 20px; background-color: white; color: black; font-family: 'Times New Roman', serif; width: 700px; margin: auto;">
                <div style="text-align: center; border-bottom: 2px solid black; padding-bottom: 10px; margin-bottom: 10px;">
                    <div style="font-size: 12px;">Department of Education - Region III</div>
                    <div style="font-weight: bold; font-size: 20px;">DISBURSEMENT VOUCHER</div>
                    <div style="font-weight: bold; font-size: 14px;">CARMEN NATIONAL HIGH SCHOOL</div>
                </div>
                
                <table style="width: 100%; border-collapse: collapse; font-size: 13px;">
                    <tr>
                        <td style="border: 1px solid black; padding: 5px; width: 70%;"><b>Payee:</b> {payee}</td>
                        <td style="border: 1px solid black; padding: 5px;"><b>Date:</b> {dv_date.strftime('%m/%d/%Y')}</td>
                    </tr>
                    <tr>
                        <td style="border: 1px solid black; padding: 5px;"><b>Address:</b> {address}</td>
                        <td style="border: 1px solid black; padding: 5px;"><b>DV No:</b> {dv_no}</td>
                    </tr>
                </table>

                <table style="width: 100%; border-collapse: collapse; margin-top: 10px; font-size: 13px;">
                    <tr style="text-align: center; font-weight: bold; background-color: #f2f2f2;">
                        <td style="border: 1px solid black; padding: 5px; width: 75%;">Particulars</td>
                        <td style="border: 1px solid black; padding: 5px;">Amount</td>
                    </tr>
                    <tr>
                        <td style="border: 1px solid black; padding: 10px; height: 180px; vertical-align: top;">
                            {particulars_text}
                        </td>
                        <td style="border: 1px solid black; text-align: right; padding: 10px; vertical-align: top; font-weight: bold;">
                            ₱ {amount:,.2f}
                        </td>
                    </tr>
                </table>

                <div style="border: 1px solid black; padding: 10px; margin-top: 10px; font-size: 12px;">
                    <b>A. Certified:</b> Expenses/Cash Advance necessary, lawful and incurred under my direct supervision.<br><br><br>
                    <div style="text-align: center;">
                        <span style="text-decoration: underline; font-weight: bold;">JESUSA D. BOTE, CESE</span><br>
                        School Principal IV
                    </div>
                </div>

                <div style="border: 1px solid black; padding: 10px; margin-top: 10px; background-color: #f9f9f9; font-size: 12px;">
                    <b>D. Approved for Payment:</b><br><br>
                    <div style="text-align: center; font-style: italic; font-weight: bold; font-size: 14px;">
                        {words_amount}
                    </div>
                </div>
            </div>
            """

            # --- 4. THE FIX: USE HTML COMPONENT ---
            # This forces the browser to render the code as a visual form
            st.components.v1.html(voucher_html, height=800, scrolling=True)
            
            st.success("✅ Voucher Generated! You can now see the boxes and tables.")
