import streamlit as st
import re
import pandas as pd
from io import BytesIO
from fpdf import FPDF

# --- PDF GENERATOR FUNCTION ---
def create_pdf(text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="AI Privacy Guard - Protected Report", ln=1, align='C')
    pdf.ln(10)
    # Text-ah PDF-la ezhuthu
    pdf.multi_cell(0, 10, txt=text)
    return pdf.output(dest='S').encode('latin-1')

# --- EXCEL GENERATOR FUNCTION ---
def convert_to_excel(protected_text):
    df = pd.DataFrame([{"Protected_Result": protected_text}])
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='PrivacyReport')
    return output.getvalue()

# --- MAIN UI ---
st.title("🛡️ Privacy Legend v4.0 (PDF Support)")

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
        
        # 3 Columns for 3 Buttons
        c1, c2, c3 = st.columns(3)
        
        with c1:
            # PDF Download
            pdf_data = create_pdf(protected)
            st.download_button(label="📄 Download PDF", data=pdf_data, file_name="Report.pdf", mime="application/pdf")
            
        with c2:
            # XL Download
            xl_data = convert_to_excel(protected)
            st.download_button(label="📊 Download Excel", data=xl_data, file_name="Report.xlsx")
            
        with c3:
            # Doc Download
            st.download_button(label="📝 Download Doc", data=protected, file_name="Report.txt")
            
        st.balloons()
    else:
        st.warning("Text type panna thaan download panna mudiyum!")