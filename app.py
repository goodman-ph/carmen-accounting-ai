import streamlit as st
import google.generativeai as genai
from num2words import num2words

# Page Setup
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

def get_voucher_html(fund, payee, addr, date, dv_no, amount, p_text, amt_words):
    # We use a simple f-string here for maximum stability
    return f"""
    <div style="background-color: white; color: black; padding: 20px; border: 2px solid black; font-family: serif; width: 700px; margin: auto; line-height: 1.2;">
        <div style="text-align: right; font-size: 10px; font-style: italic;">Appendix 32</div>
        <div style="text-align: center; border-bottom: 2px solid black; padding-bottom: 5px;">
            <div style="font-size: 11px;">Department of Education - Region III</div>
            <div style="font-weight: bold; font-size: 18px;">DISBURSEMENT VOUCHER</div>
            <div style="font-weight: bold; font-size: 14px;">CARMEN NATIONAL HIGH SCHOOL</div>
        </div>
        <table style="width: 100%; border-collapse: collapse; font-size: 11px; margin-top: 5px;">
            <tr>
                <td style="border: 1px solid black; padding: 5px; width: 70%;"><b>Fund Cluster:</b> {fund}</td>
                <td style="border: 1px solid black; padding: 5px;"><b>Date:</b> {date}<br><b>DV No:</b> {dv_no}</td>
            </tr>
            <tr>
                <td style="border: 1px solid black; padding: 5px;" colspan="2"><b>Payee:</b> {payee} | <b>Address:</b> {addr}</td>
            </tr>
        </table>
        <table style="width: 100%; border-collapse: collapse; font-size: 11px; margin-top: -1px;">
            <tr style="text-align: center; font-weight: bold;">
                <td style="border: 1px solid black; padding: 5px; width: 70%;">Particulars</td>
                <td style="border: 1px solid black; padding: 5px;">Amount</td>
            </tr>
            <tr>
                <td style="border: 1px solid black; padding: 10px; height: 160px; vertical-align: top;">{p_text}</td>
                <td style="border: 1px solid
