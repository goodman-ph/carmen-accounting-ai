import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Carmen NHS AI", layout="wide")
st.title("📑 Carmen NHS Accounting Particulars Generator")

# 1. API Key Setup
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("API Key missing! Go to Streamlit Settings > Secrets and add GEMINI_API_KEY.")
    st.stop()

# 2. Updated Model Name (This fixes the 404 error)
# Using 'gemini-1.5-flash' without the 'models/' prefix is now the standard for the latest SDK
model = genai.GenerativeModel('gemini-1.5-flash')

st.markdown("---")
user_input = st.text_input("Enter Expense Details:", placeholder="Ex: Loyalty award for Ador Dionisio 15 years")

if st.button("Generate All Particulars"):
    if user_input:
        try:
            # We explicitly ask for a specific format to make splitting easier
            prompt = f"""
            Act as a DepEd Accountant. For the expense '{user_input}', generate:
            PARTICULAR1: [Draft the ORS Box B particulars here]
            PARTICULAR2: [Draft the DV Particulars here]
            PARTICULAR3: [Draft the JEV Description here]
            Ensure Carmen National High School is mentioned. Use COA standards.
            """
            
            with st.spinner('Processing...'):
                response = model.generate_content(prompt)
                full_text = response.text
                
                # Create 3 columns for the 3 boxes
                col1, col2, col3 = st.columns(3)
                
                # Logic to display text (even if splitting fails)
                with col1:
                    st.info("### ORS Box B")
                    st.write(full_text.split("PARTICULAR2")[0].replace("PARTICULAR1:", "").strip())
                
                with col2:
                    st.success("### DV Particulars")
                    if "PARTICULAR2" in full_text:
                        st.write(full_text.split("PARTICULAR2")[1].split("PARTICULAR3")[0].replace(":", "").strip())
                
                with col3:
                    st.warning("### JEV Description")
                    if "PARTICULAR3" in full_text:
                        st.write(full_text.split("PARTICULAR3")[1].replace(":", "").strip())

        except Exception as e:
            st.error(f"Error: {e}. Try checking your API Key in Google AI Studio.")
    else:
        st.warning("Please type an expense description.")

st.markdown("---")
st.caption("Admin Tool for Carmen National High School | 2026")
