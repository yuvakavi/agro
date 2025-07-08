import streamlit as st

# Try normal import if running from agri_ai_app/
try:
    from utils.db import register_user, validate_login
except ModuleNotFoundError:
    # fallback if run directly from inside components folder (rare case)
    import sys
    import os
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    from utils.db import register_user, validate_login

def login_page():
    st.title("🔐 Login to AgroBot")

    name = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        user = validate_login(name, password)
        if user:
            st.success(f"Welcome back, {name}!")
            st.session_state.user = name
            st.session_state.page = "chatbot"
        else:
            st.error("Invalid credentials. Please try again or sign up.")

    st.info("Don't have an account?")
    if st.button("Go to Signup"):
        st.session_state.page = "signup"

def signup_page():
    st.title("📝 Signup for AgroBot")

    name = st.text_input("Create Username")
    password = st.text_input("Create Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")

    if st.button("Signup"):
        if password != confirm_password:
            st.error("Passwords do not match!")
        elif name.strip() == "" or password.strip() == "":
            st.error("Username and password cannot be empty.")
        else:
            register_user(name, password)
            st.success("Signup successful! Please login.")
            st.session_state.page = "login"

    st.info("Already have an account?")
    if st.button("Go to Login"):
        st.session_state.page = "login"











