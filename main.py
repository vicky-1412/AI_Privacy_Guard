import streamlit as st
import sqlite3
import hashlib
import re
from pypdf import PdfReader
import plotly.express as px
import pandas as pd

# --- CUSTOM CSS FOR DARK MODE LOOK ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #ff4b4b; color: white; }
    .stTextInput>div>div>input { background-color: #262730; color: white; }
    </style>
    """, unsafe_allow_html=True)

# --- DATABASE SETUP ---
conn = sqlite3.connect('users.db', check_same_thread=False)
c = conn.cursor()
c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT, password TEXT)')
c.execute('CREATE TABLE IF NOT EXISTS history(username TEXT, scan_type TEXT, count INTEGER, date TEXT)')
conn.commit()

def make_hashes(password): return hashlib.sha256(str.encode(password)).hexdigest()
def check_hashes(password, hashed_text): return make_hashes(password) == hashed_text

# --- APP UI ---
st.sidebar.title("🛡️ Privacy Pro AI")
menu = ["Login", "SignUp", "Dashboard"]
choice = st.sidebar.selectbox("Navigate", menu)

if choice == "SignUp":
    st.subheader("Create a New Account")
    new_user = st.text_input("Username")
    new_pwd = st.text_input("Password", type='password')
    if st.button("Create Account"):
        c.execute('INSERT INTO userstable(username, password) VALUES (?,?)', (new_user, make_hashes(new_pwd)))
        conn.commit()
        st.success("Account Created! Login panni mass kaatu macha.")

elif choice == "Login":
    st.subheader("Welcome Back!")
    username = st.text_input("User Name")
    password = st.text_input("Password", type='password')
    if st.button("Login"):
        c.execute('SELECT * FROM userstable WHERE username =?', (username,))
        data = c.fetchone()
        if data and check_hashes(password, data[1]):
            st.session_state['logged_in'] = True
            st.session_state['user'] = username
            st.rerun()

    if st.session_state.get('logged_in'):
        st.success(f"Logged in as {st.session_state['user']}")
        # --- SCANNER LOGIC ---
        input_text = st.text_area("Paste text or sensitive data here:")
        if st.button("Protect Now"):
            # Regex logic
            email_pattern = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
            matches = len(re.findall(email_pattern, input_text))
            protected = re.sub(email_pattern, "[EMAIL PROTECTED]", input_text)
            
            st.subheader("Protected Data:")
            st.code(protected)
            
            # Save stats
            from datetime import date
            c.execute('INSERT INTO history VALUES (?,?,?,?)', (st.session_state['user'], "Text Scan", matches, str(date.today())))
            conn.commit()
            st.balloons()

elif choice == "Dashboard":
    st.subheader("📊 Global Privacy Analytics")
    c.execute('SELECT scan_type, SUM(count) FROM history GROUP BY scan_type')
    db_data = c.fetchall()
    
    if db_data:
        df = pd.DataFrame(db_data, columns=['Type', 'Total Data Protected'])
        fig = px.bar(df, x='Type', y='Total Data Protected', color='Type', template="plotly_dark")
        st.plotly_chart(fig)
        
        # Performance Card
        st.metric(label="Total Leaks Blocked", value=df['Total Data Protected'].sum(), delta="Mass Improvement")
    else:
        st.warning("No data found! Login panni oru scan pannu macha.")