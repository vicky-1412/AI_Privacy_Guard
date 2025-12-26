import streamlit as st
import re
import pandas as pd
from io import BytesIO

# --- DOWNLOAD HELPERS ---
def convert_df(df):
    # Excel format-ku matha
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name='Sheet1')
    writer.close()
    return output.getvalue()

# --- MAIN APP ---
# (Munnadi panna Login/Database logic-ah apdiye vechukko macha, 
# Scanner section-la mattum intha download logic-ah add pannu)

if st.session_state.get('logged_in'):
    st.subheader("🚀 Pro Data Exporter")
    input_text = st.text_area("Scan and Download panna text-ah podu:")
    
    if st.button("Secure & Generate Reports"):
        # Regex Scan
        email_pattern = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
        protected_text = re.sub(email_pattern, "[EMAIL PROTECTED]", input_text)
        
        st.success("Data Protected!")
        st.code(protected_text)
        
        # Reports Data
        report_data = {'Original Text': [input_text], 'Protected Text': [protected_text]}
        df = pd.DataFrame(report_data)
        
        st.divider()
        st.write("### ⬇️ Download Your Reports")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # XL Download
            xl_data = convert_df(df)
            st.download_button(label="📥 Download Excel", data=xl_data, file_name="Privacy_Report.xlsx")
            
        with col2:
            # TXT (Document) Download
            st.download_button(label="📝 Download Doc (Txt)", data=protected_text, file_name="Privacy_Report.txt")
            
        with col3:
            # Simple CSV Download
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(label="📊 Download CSV", data=csv, file_name="Privacy_Report.csv")

        st.balloons()