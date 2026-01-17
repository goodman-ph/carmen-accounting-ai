import streamlit as st
import google.generativeai as genai

# Helper function to convert number to words (Simplified for School Use)
def amount_to_words(number):
    from num2words import num2words
    try:
        words = num2words(number, lang='en')
        return words.replace('and', '').title() + " Pesos Only"
    except:
        return "_________________ Pesos Only"

# Page Config
st.set_page_config(page_title="Carmen NHS DV Generator", layout="wide")

# 1. Official Master Template
OFFICIAL_TEMPLATE = """
You are the Senior School Accountant for Carmen National High School. 
Generate uniform particulars following Philippine COA/DepEd standards:
RULES:
1. ORS: "To recognize obligation for [Expense Name] of [Payee]..."
2. DV: "Payment of [Expense Name] for [Payee] for the period [Date] per [Docs]..."
3. JEV: Provide Account Title | UACS Code | Debit | Credit.
4. MANDATORY: Include 'Carmen National High School'.
"""

# 2. Sidebar for Official Headers (Extract Data)
with st.sidebar:
    st.header("📋 Voucher Header Data")
    payee = st.text_input("Payee (e.g., GSIS or Name)")
    address = st.text_input("Address")
    tin_emp = st.text_input("TIN / Employee No.")
    dv_date = st.date_input("Date")
    dv_no = st.text_input("DV No.", placeholder="2026-01-001")
    amount = st.number_input("Amount (PHP)", min_value=0.0, format="%.2f")

# 3. Main Interface
st.title("📑 Carmen NHS Disbursement Voucher Tool")
user_input = st.text_area("Transaction Details (Purpose):", placeholder="e.g. Water bill for Jan 2026")

if st.button("Generate & Preview Voucher"):
    if user_input and amount > 0:
        # Configuration
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        # Process Particulars
        response = model.generate_content(f"{OFFICIAL_TEMPLATE}\n\nPROCESS: {user_input}")
        particulars = response.text
        
        # Display the Digital Form
        st.success("✅ Voucher Ready for Printing")
        
        with st.container(border=True):
            # Header Table
            st.markdown(f"**Payee:** {payee} | **Date:** {dv_date} | **DV No:** {dv_no}")
            st.markdown(f"**Address:** {address} | **TIN/Emp No:** {tin_emp}")
            st.divider()
            
            # Box A: Particulars
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write("**Particulars**")
                st.write(particulars)
            with col2:
                st.write("**Amount**")
                st.subheader(f"₱{amount:,.2f}")
            
            st.divider()
            
            # Box D: Approved for Payment (Amount in Words)
            st.write("**D. Approved for Payment**")
            amt_words = amount_to_words(amount)
            st.info(f"**{amt_words}**")
            
            # Signature Box
            st.write("**JESUSA D. BOTE, CESE**")
            st.caption("School Principal IV")
            
    else:
        st.warning("Please enter transaction details and an amount.")
