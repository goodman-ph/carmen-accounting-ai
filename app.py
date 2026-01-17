import streamlit as st
import google.generativeai as genai
from num2words import num2words
import base64

st.set_page_config(page_title="Carmen NHS DV Generator", layout="centered")

def format_amount_in_words(amount):
    try:
        pesos = int(amount)
        centavos = int(round((amount - pesos) * 100))
        words = num2words(pesos, lang='en').replace('and', '').title()
        if centavos > 0:
            return words + " and " + str(centavos) + "/100 Pesos Only"
        return words + " Pesos Only"
    except:
        return "_________________ Pesos Only"

# SIDEBAR
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
                prompt = "Write a 1-paragraph DepEd accounting particular for " + str(u_input) + " at Carmen National High School. Start with 'Payment of'."
                response = model.generate_content(prompt)
                p_text = response.text.replace("**", "").replace('"', "'").strip()
                amt_words = format_amount_in_words(f_amount)

                # THE SAFE STRING METHOD: Each line is closed individually
                parts = [
                    'PGRpdiBzdHlsZT0iYmFja2dyb3VuZC1jb2xvcjogd2hpdGU7IGNvbG9yOiBibGFjazsgcGFkZGluZzogMjVweDsgYm9yZGVyOiAzcHggc29saWQgYmxhY2s7IGZvbnQtZmFtaWx5OiAnVGltZXMgTmV3IFJvbWFuJywgc2VyaWY7IHdpZHRoOiA2NTBweDsgbWFyZ2luOiBhdXRvOyBsaW5lLWhlaWdodDogMS4yOyI+PGRpdiBzdHlsZT0idGV4dC1hbGlnbjogcmlnaHQ7IGZvbnQtc2l6ZTogMTBweDsgZm9udC1zdHlsZTogaXRhbGljOyI+QXBwZW5kaXggMzI8L2Rpdj48ZGl2IHN0eWxlPSJ0
