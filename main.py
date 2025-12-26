import streamlit as st
import re
import pandas as pd
from io import BytesIO

# --- PAGE CONFIG ---
st.set_page_config(page_title="Privacy AI Legend", page_icon="🛡️", layout="wide")

# --- FUNCTIONS ---
def convert_to_excel(protected_text):
    df = pd.DataFrame([{"Original_Data": "User Input", "Protected_Result": protected_text}])
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='PrivacyReport')
    return output.getvalue()

def mask_data(text):
    email_pattern = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
    phone_pattern = r'\b\d{10}\b'
    text = re.sub(email_pattern, "[EMAIL HIDDEN]", text)
    text = re.sub(phone_pattern, "[PHONE HIDDEN]", text)
    return text

# --- UI DESIGN ---
st.title("🛡️ AI Privacy Legend v3.0")
st.markdown("### Protect your data and download professional reports (XL/Doc)")

user_input = st.text_area("Macha, un sensitive text-ah inga podu:", height=200, placeholder="Example: My email is [email protected] and phone is 9876543210")

if st.button("🚀 Secure & Generate Reports"):
    if user_input.strip() != "":
        protected = mask_data(user_input)
        
        # Result Display
        st.success("AI has successfully masked your data!")
        st.code(protected, language="text")
        
        st.divider()
        st.subheader("📥 Download Center")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Excel Logic
            excel_data = convert_to_excel(protected)
            st.download_button(
                label="📊 Download Excel Report",
                data=excel_data,
                file_name="Privacy_Report.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
            
        with col2:
            # Text/Doc Logic
            st.download_button(
                label="📝 Download Text Document",
                data=protected,
                file_name="Protected_Data.txt",
                mime="text/plain"
            )
        st.balloons()
    else:
        st.error("Empty-ah irukku macha! Ethavathu type pannu.")

st.sidebar.markdown("### App Features:")
st.sidebar.write("✅ Email Masking")
st.sidebar.write("✅ Phone Masking")
st.sidebar.write("✅ Excel/XL Export")
st.sidebar.write("✅ Doc/Text Export")