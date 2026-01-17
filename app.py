import streamlit as st
import google.generativeai as genai
from num2words import num2words

# Basic Page Setup
st.set_page_config(page_title="Carmen NHS", layout="centered")

def format_words(amount):
    try:
        pesos = int(amount)
        words = num2words(pesos, lang='en').title()
        return f"{words} Pesos Only"
    except:
        return "Zero Pesos"

# Sidebar
with st.sidebar:
    st.header("📋 Voucher Details")
    v_payee = st.text_input("Payee", "GSIS")
    v_amount = st.number_input("Amount", min_value=0.0)
    v_date = st.date_input("Date")

st.title("📑 Carmen NHS DV Generator")
u_input = st.text_area("What is this payment for?")

if st.button("Generate Voucher"):
    if u_input and v_amount > 0:
        try:
            # Secure API Check
            if "GEMINI_API_KEY" not in st.secrets:
                st.error("Missing API Key in Secrets")
                st.stop()
            
            genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
            model = genai.GenerativeModel('gemini-2.0-flash')
            
            with st.spinner('Writing Particulars...'):
                prompt = f"Write a 1-paragraph DepEd particular for {u_input} at Carmen NHS. Start with 'Payment of'."
                response = model.generate_content(prompt)
                p_text = response.text.replace("*", "").strip()
                amt_in_words = format_words(v_amount)

            # --- THE VOUCHER DISPLAY ---
            # We use st.markdown for maximum stability. No HTML syntax errors possible.
            st.success("✅ Voucher Generated Successfully")
            
            st.markdown("---")
            st.markdown(f"### DISBURSEMENT VOUCHER")
            st.markdown(f"**CARMEN NATIONAL HIGH SCHOOL**")
            
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Payee:** {v_payee}")
                st.write(f"**Date:** {v_date}")
            with col2:
                st.write(f"**Amount:** ₱ {v_amount:,.2f}")
            
            st.info(f"**Particulars:**\n\n{p_text}")
            
            st.warning(f"**Amount in Words:**\n\n*{amt_in_words}*")
            
            st.markdown("---")
            st.markdown("**A. Certified:** Expenses necessary, lawful and incurred under my supervision.")
            st.write("**JESUSA D. BOTE, CESE** / *School Principal IV*")

        except Exception as e:
            st.error(f"Error: {str(e)}")
    else:
        st.warning("Please fill in the details.")
