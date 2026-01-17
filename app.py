import streamlit as st
import google.generativeai as genai
from num2words import num2words
import base64

# 1. Page Config
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

# 2. Sidebar Inputs
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
                prompt = "Write a 1-paragraph DepEd accounting particular for " + u_input + " at Carmen National High School. Start with 'Payment of'."
                response = model.generate_content(prompt)
                p_text = response.text.replace("**", "").replace('"', "'").strip()
                amt_words = format_amount_in_words(f_amount)

                # 3. BASE64 ENCODED TEMPLATE (Prevents Python Syntax Errors)
                # This is a standard HTML template converted to a string Python can't break.
                template_raw = (
                    'PGRpdiBzdHlsZT0iYmFja2dyb3VuZC1jb2xvcjogd2hpdGU7IGNvbG9yOiBibGFjazsgcGFkZGluZzogMjVweDsgYm9yZGVyOiAzcHggc'
                    '29saWQgYmxhY2s7IGZvbnQtZmFtaWx5OiAnVGltZXMgTmV3IFJvbWFuJywgc2VyaWY7IHdpZHRoOiA2NTBweDsgbWFyZ2luOiBhdXRv'
                    'OyBsaW5lLWhlaWdodDogMS4yOyI+PGRpdiBzdHlsZT0idGV4dC1hbGlnbjogcmlnaHQ7IGZvbnQtc2l6ZTogMTBweDsgZm9udC1zdHl'
                    'sZTogaXRhbGljOyI+QXBwZW5kaXggMzI8L2Rpdj48ZGl2IHN0eWxlPSJ0ZXh0LWFsaWduOiBjZW50ZXI7IGJvcmRlci1ib3R0b206ID'
                    'JweCBzb2xpZ  YmxhY2s7IHBhZGRpbmctYm90dG9tOiAxMHB4OyBtYXJnaW4tYm90dG9tOiAxMHB4OyI+PGRpdiBzdHlsZT0iZm9udC1'
                    'zaXplOiAxMnB4OyI+RGVwYXJ0bWVudCBvZiBFZHVjYXRpb24gLSBSZWdpb24gSUlJPC9kaXY+PGRpdiBzdHlsZT0iZm9udC13ZWlnaHQ'
                    '6IGJvbGQ7IGZvbnQtc2l6ZTogMjBweDsiPkRJU0JVUlNFTUVOVCBWT1VDSEVSPC9kaXY+PGRpdiBzdHlsZT0iZm9udC13ZWlnaHQ6IGJ'
                    'vbGQ7IGZvbnQtc2l6ZTogMTVweDsiPkNBUk1FTiBOQVRJT05BTCBISUdIIFNDSE9PTDwvZGl2PjwvZGl2Pjx0YWJsZSBzdHlsZT0id2l'
                    'kdGg6IDEwMCU7IGJvcmRlci1jb2xsYXBzZTogY29sbGFwc2U7IGZvbnQtc2l6ZTogMTJweDsiPjx0cj48dGQgc3R5bGU9ImJvcmRlcjog'
                    'MXB4IHNvbGlkIGJsYWNrOyBwYWRkaW5nOiA4cHg7Ij48Yj5GdW5kIENsdXN0ZXI6PC9iPiBbRlVORF08L3RkPjx0ZCBzdHlsZT0iYm9y'
                    'ZGVyOiAxcHggc29saWQgYmxhY2s7IHBhZGRpbmc6IDhweDsiPjxiPkRhdGU6PC9iPiBbREFURV08YnI+PGI+RFYgTm86PC9iPiBbRFZf'
                    'Tk9dPC90ZD48L3RyPjx0cj48dGQgc3R5bGU9ImJvcmRlcjogMXB4IHNvbGlkIGJsYWNrOyBwYWRkaW5nOiA4cHg7IiBjb2xzcGFuPSIy'
                    'Ij48Yj5QYXllZTo8L2I+IFtQQVlFRV0gfCA8Yj5BZGRyZXNzOjwvYj4gW0FERFJdPC90ZD48L3RyPjwvdGFibGU+PHRhYmxlIHN0eWxl'
                    'PSJ3aWR0aDogMTAwJTsgYm9yZGVyLWNvbGxhcHNlOiBjb2xsYXBzZTsgZm9udC1zaXplOiAxMnB4OyBtYXJnaW4tdG9wOiAtMXB4OyI+'
                    'PHRyIHN0eWxlPSJ0ZXh0LWFsaWduOiBjZW50ZXI7IGZvbnQtd2VpZ2h0OiBib2xkOyI+PHRkIHN0eWxlPSJvcmRlcjogMXB4IHNvbGlk'
                    'IGJsYWNrOyBwYWRkaW5nOiA1cHg7IHdpZHRoOiA3MCU7Ij5QYXJ0aWN1bGFyczwvdGQ+PHRkIHN0eWxlPSJib3JkZXI6IDFweCBzb2xp'
                    'ZCBibGFjazsgcGFkZGluZzogNXB4OyI+QW1vdW50PC90ZD48L3RyPjx0cj48dGQgc3R5bGU9ImJvcmRlcjogMXB4IHNvbGlkIGJsYWNr'
                    'OyBwYWRkaW5nOiAxNXB4OyBoZWlnaHQ6IDE4MHB4OyB2ZXJ0aWNhbC1hbGlnbjogdG9wOyB0ZXh0
