import streamlit as st
import google.generativeai as genai
from num2words import num2words

# Page Configuration
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

# --- SIDEBAR INPUTS ---
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
                prompt = f"Write a professional 1-paragraph DepEd particular for {u_input} for Carmen NHS. Start with 'Payment of'."
                response = model.generate_content(prompt)
                p_text = response.text.replace("**", "").strip()
                amt_words = format_amount_in_words(f_amount)

                # --- FAIL-SAFE HTML ASSEMBLY ---
                # We build the HTML line-by-line to avoid SyntaxErrors
                html = '<div style="background-color: white; color: black; padding:
