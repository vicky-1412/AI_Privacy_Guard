import streamlit as st
import re
from pypdf import PdfReader

# --- PAGE CONFIG ---
st.set_page_config(page_title="AI Privacy Pro", page_icon="🔐")

# --- LOGIN LOGIC ---
def login():
    st.title("🔐 Secure Login")
    user = st.text_input("Username")
    pwd = st.text_input("Password", type="password")
    
    # Inga nee unakku pudicha username & password vechukko macha
    if st.button("Login"):
        if user == "macha" and pwd == "Strong@123": # Strong Password Example
            st.session_state["logged_in"] = True
            st.rerun()
        else:
            st.error("Invalid Username or Password! Correct-ah podu macha.")

# --- MAIN APP FUNCTION ---
def main_app():
    st.title("🛡️ Pro Privacy Guard")
    st.sidebar.success("Welcome Macha! You are logged in. ✅")
    
    if st.sidebar.button("Logout"):
        st.session_state["logged_in"] = False
        st.rerun()

    # Masking Logic
    def mask_private_info(text):
        email_pattern = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
        phone_pattern = r'\b\d{10}\b'
        card_pattern = r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b'
        text = re.sub(email_pattern, "[EMAIL PROTECTED]", text)
        text = re.sub(phone_pattern, "[PHONE HIDDEN]", text)
        text = re.sub(card_pattern, "[CARD HIDDEN]", text)
        return text

    tab1, tab2 = st.tabs(["📝 Text Scanner", "📄 PDF Scanner"])
    with tab1:
        user_input = st.text_area("Paste text here:")
        if st.button("Protect Text"):
            st.success(mask_private_info(user_input))
    with tab2:
        uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
        if uploaded_file:
            reader = PdfReader(uploaded_file)
            full_text = "".join([p.extract_text() for p in reader.pages])
            st.write(mask_private_info(full_text))

# --- APP FLOW ---
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if not st.session_state["logged_in"]:
    login()
else:
    main_app()