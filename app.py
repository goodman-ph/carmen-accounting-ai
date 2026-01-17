import streamlit as st
import google.generativeai as genai
from num2words import num2words

# Page Settings
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
        return ""

# --- 2. MASTER PROMPT ---
OFFICIAL_TEMPLATE = "Generate a concise accounting particular for a DepEd Disbursement Voucher. Start with 'Payment of...' and mention Carmen National High School."

# --- 3. INPUT FIELDS (Voucher Headers) ---
with st.sidebar:
    st.header("Voucher Details")
    payee = st.text_input("Payee", value="GSIS")
    address = st.text_input("Address", value="Cabanatuan City")
    tin_no = st.text_input("TIN/Employee No.")
    dv_no = st.text_input("DV No.")
    amount = st.number_input("Amount (PHP)", min_value=0.0, format="%.2f")
    dv_date = st.date_input("Date")

# --- 4. MAIN INTERFACE ---
st.title("📑 Official DV Generator")
user_input = st.text_area("Purpose/Details:")

if st.button("Generate Official Voucher"):
    if user_input and amount > 0:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        response = model.generate_content(f"{OFFICIAL_TEMPLATE}\n\nDetails: {user_input}")
        particulars_text = response.text
        words_amount = format_amount_in_words(amount)

        # --- 5. THE RENDERED TEMPLATE ---
        # This is the part that turns "code" into a "form"
        st.markdown(f"""
        <div style="background-color: white; color: black; padding: 30px; border: 2px solid black; font-family: 'Arial', sans-serif;">
            
            <div style="text-align: center; border-bottom: 2px solid black; padding-bottom: 10px;">
                <div style="font-size: 12px;">Department of Education - Region III</div>
                <div style="font-weight: bold; font-size: 18px;">DISBURSEMENT VOUCHER</div>
                <div style="font-size: 14px;">CARMEN NATIONAL HIGH SCHOOL</div>
            </div>

            <table style="width: 100%; border-collapse: collapse; margin-top: 10px;">
                <tr>
                    <td style="border: 1px solid black; padding: 5px; width: 60%;"><b>Payee:</b> {payee}</td>
                    <td style="border: 1px solid black; padding: 5px;"><b>Date:</b> {dv_date.strftime('%m/%d/%Y')}</td>
                </tr>
                <tr>
                    <td style="border: 1px solid black; padding: 5px;"><b>Address:</b> {address}</td>
                    <td style="border: 1px solid black; padding: 5px;"><b>DV No:</b> {dv_no}</td>
                </tr>
            </table>

            <table style="width: 100%; border-collapse: collapse; margin-top: 10px;">
                <tr style="text-align: center; font-weight: bold; background-color: #eeeeee;">
                    <td style="border: 1px solid black; padding: 5px; width: 75%;">Particulars</td>
                    <td style="border: 1px solid black; padding: 5px;">Amount</td>
                </tr>
                <tr>
                    <td style="border: 1px solid black; padding: 15px; height: 150px; vertical-align: top;">
                        {particulars_text}
                    </td>
                    <td style="border: 1px solid black; text-align: right; padding: 15px; vertical-align: top; font-weight: bold; font-size: 18px;">
                        ₱ {amount:,.2f}
                    </td>
                </tr>
            </table>

            <div style="border: 1px solid black; padding: 10px; margin-top: 10px;">
                <div style="font-size: 12px;"><b>A. Certified:</b> Expenses/Cash Advance necessary, lawful and incurred under my direct supervision.</div>
                <br>
                <div style="text-align: center;">
                    <b style="text-decoration: underline;">JESUSA D. BOTE, CESE</b><br>
                    <span>School Principal IV</span>
                </div>
            </div>

            <div style="border: 1px solid black; padding: 10px; margin-top: 10px; background-color: #fcfcfc;">
                <div style="font-size: 12px;"><b>D. Approved for Payment:</b></div>
                <div style="text-align: center; font-style: italic; font-weight: bold; padding: 10px;">
                    {words_amount}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True) # THIS LINE IS CRITICAL

        st.success("✅ Voucher Generated! Use Ctrl+P to print this page.")
