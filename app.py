import streamlit as st
import google.generativeai as genai
from num2words import num2words

st.set_page_config(page_title="Carmen NHS DV Generator", layout="wide")

def format_amount_in_words(amount):
    try:
        pesos = int(amount)
        centavos = int(round((amount - pesos) * 100))
        words = num2words(pesos, lang='en').replace('and', '').title()
        if centavos > 0: return f"{words} and {centavos}/100 Pesos Only"
        return f"{words} Pesos Only"
    except: return "_________________ Pesos Only"

# --- SIDEBAR ---
with st.sidebar:
    st.header("📋 Voucher Details")
    fund_cluster = st.text_input("Fund Cluster", "01")
    payee = st.text_input("Payee", value="GSIS")
    address = st.text_input("Address", value="Cabanatuan City")
    dv_no = st.text_input("DV No.", placeholder="2026-01-000")
    amount = st.number_input("Amount (PHP)", min_value=0.0, format="%.2f")
    dv_date = st.date_input("Date")

st.title("📑 Official DV Generator")
user_input = st.text_area("Transaction Details:", placeholder="e.g., GSIS January Premiums")

if st.button("Generate Complete Voucher"):
    if not user_input or amount <= 0:
        st.error("❌ Please enter both details and an amount.")
    else:
        try:
            # Verify API Key exists
            if "GEMINI_API_KEY" not in st.secrets:
                st.error("🔑 API Key not found in Streamlit Secrets!")
                st.stop()
                
            genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            with st.spinner('🖋️ Generating Particulars...'):
                prompt = f"Write a 1-paragraph DepEd particulars for {user_input} for Carmen National High School. Start with 'Payment of'."
                response = model.generate_content(prompt)
                p_text = response.text.replace("**", "").strip()
                amt_words = format_amount_in_words(amount)

            # --- RENDER VOUCHER ---
            # We use a container to ensure it stays in view
            with st.container():
                html_code = f"""
                <div style="background-color: white; color: black; padding: 20px; border: 2px solid black; font-family: serif; width: 750px; margin: auto;">
                    <h2 style="text-align: center;">DISBURSEMENT VOUCHER</h2>
                    <h4 style="text-align: center;">CARMEN NATIONAL HIGH SCHOOL</h4>
                    <hr>
                    <p><b>Payee:</b> {payee} <br> <b>Amount:</b> ₱ {amount:,.2f}</p>
                    <div style="border: 1px solid black; padding: 10px; height: 150px;">
                        <b>Particulars:</b><br>{p_text}
                    </div>
                    <p style="text-align: center; font-style: italic; font-weight: bold; margin-top: 10px;">{amt_words}</p>
                    <table style="width: 100%; border-top: 1px solid black; margin-top: 20px;">
                        <tr>
                            <td><b>Certified by:</b><br><br>JESUSA D. BOTE, CESE<br>Principal IV</td>
                            <td><b>Accounting:</b><br><br>GODFREY D. MANGULABNAN<br>Sr. Bookkeeper</td>
                        </tr>
                    </table>
                </div>
                """
                # This is the command that shows the voucher
                st.components.v1.html(html_code, height=600, scrolling=True)
                
                # FALLBACK: If the component above is blank, this text will still show
                st.info("💡 If the box above is blank, check your browser's 'Block Pop-ups' settings.")
                st.subheader("Generated Particulars (Copy/Paste):")
                st.write(p_text)

        except Exception as e:
            st.error(f"⚠️ An error occurred: {str(e)}")
