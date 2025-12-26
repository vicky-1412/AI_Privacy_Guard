import streamlit as st
import re
import pandas as pd
from io import BytesIO
from fpdf import FPDF
import google.generativeai as genai

# --- PAGE CONFIG ---
st.set_page_config(page_title="AI Privacy Legend", page_icon="🛡️")

# --- AI SETUP (Safe Secrets Method) ---
# Streamlit Cloud Settings -> Secrets-la GEMINI_KEY-ah save panni vechukko macha
try:
    genai.configure(api_key=st.secrets["GEMINI_KEY"])
    model = genai.GenerativeModel('gemini-pro')
except Exception as e:
    st.error("Secrets-la API Key set pannala pola macha! Check Streamlit Settings.")

# --- PDF GENERATOR FUNCTION ---
def create_pdf(text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="AI Privacy Guard - Protected Report", ln=1, align='C')
    pdf.ln(10)
    # Special character support fix
    safe_text = text.encode('latin-1', 'replace').decode('latin-1')
    pdf.multi_cell(0, 10, txt=safe_text)
    return pdf.output(dest='S').encode('latin-1')

# --- EXCEL GENERATOR FUNCTION ---
def convert_to_excel(protected_text):
    df = pd.DataFrame([{"Protected_Result": protected_text}])
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='PrivacyReport')
    return output.getvalue()

# --- MAIN UI ---
st.title("🛡️ Privacy Legend v4.0 (Full Support)")

user_input = st.text_area("Input text-ah podu macha:", height=150)

if st.button("🚀 Secure & Generate All Reports"):
    if user_input:
        # Simple masking (Email/Phone)
        protected = re.sub(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', "[EMAIL HIDDEN]", user_input)
        protected = re.sub(r'\b\d{10}\b', "[PHONE HIDDEN]", protected)
        
        st.subheader("Protected Result:")
        st.code(protected)
        
        st.divider()
        st.subheader("📥 Download Your Mass Reports")
        
        c1, c2, c3 = st.columns(3)
        
        with c1:
            pdf_data = create_pdf(protected)
            st.download_button(label="📄 Download PDF", data=pdf_data, file_name="Report.pdf", mime="application/pdf")
            
        with c2:
            xl_data = convert_to_excel(protected)
            st.download_button(label="📊 Download Excel", data=xl_data, file_name="Report.xlsx")
            
        with c3:
            st.download_button(label="📝 Download Doc", data=protected, file_name="Report.txt")
            
        st.balloons()
    else:
        st.warning("Text type panna thaan download panna mudiyum!")

# --- AI CHATBOT SECTION ---
st.divider() 
st.subheader("💬 AI Privacy Assistant")

with st.container():
    chat_input = st.text_input("Privacy pathi enna doubt macha?", placeholder="Ask me anything...")
    
    if st.button("Ask AI"):
        if chat_input:
            with st.spinner("AI yosikkuthu..."):
                try:
                    response = model.generate_content(f"You are a helpful privacy expert. Answer in simple terms: {chat_input}")
                    st.info(f"🤖 AI: {response.text}")
                except Exception as e:
                    st.error("API Key check pannu macha! Settings-la correct-ah kudu.")
        else:
            st.warning("Kelviya type pannu da!")