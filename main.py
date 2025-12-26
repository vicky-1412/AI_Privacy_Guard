import streamlit as st
import re
from pypdf import PdfReader

# Page Config
st.set_page_config(page_title="AI Privacy Pro", page_icon="🛡️")

st.title("🛡️ Pro Privacy Guard")
st.write("Macha, text-ah type pannu illa PDF file-ah upload pannu!")

def mask_private_info(text):
    # Patterns for Email, Phone, and Card
    email_pattern = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
    phone_pattern = r'\b\d{10}\b'
    card_pattern = r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b'

    text = re.sub(email_pattern, "[EMAIL PROTECTED]", text)
    text = re.sub(phone_pattern, "[PHONE HIDDEN]", text)
    text = re.sub(card_pattern, "[CARD HIDDEN]", text)
    return text

# Tabs for Text and PDF
tab1, tab2 = st.tabs(["📝 Text Scanner", "📄 PDF Scanner"])

with tab1:
    user_input = st.text_area("Paste text here:")
    if st.button("Protect Text"):
        st.success(mask_private_info(user_input))

with tab2:
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
    if uploaded_file is not None:
        reader = PdfReader(uploaded_file)
        full_text = ""
        for page in reader.pages:
            full_text += page.extract_text()
        
        st.info("PDF-la irunthu data-va AI read panniduchu. Protecting now...")
        st.write(mask_private_info(full_text))

st.sidebar.title("Settings")
st.sidebar.write("Project: AI Privacy Guard v2.0")

st.sidebar.write("Status: Active 🟢")
