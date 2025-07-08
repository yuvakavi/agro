import streamlit as st
from components.login import login_page, signup_page
from components.chatbot import chatbot_home
from components.usecases import (
    crop_recommendation_ui,
    advisor_ui,
    market_price_ui,
    disease_detection_ui
)

# === Page Config ===
st.set_page_config(page_title="AgroBot", layout="centered")

# === Session State Initialization ===
if "page" not in st.session_state:
    st.session_state.page = "home"
if "user" not in st.session_state:
    st.session_state.user = None
if "language" not in st.session_state:
    st.session_state.language = "English"

# === Home Page (Only logo centered, rest normal layout)
def show_logo_page():
    # Center the logo using columns
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image("assets/logo.png", width=140)

    # Keep rest of content left-aligned/default
    st.markdown("## Welcome to AgroBot 🌾")

    st.session_state.language = st.selectbox(
        "🌐 Choose Language / மொழி தேர்வு",
        ["English", "Tamil"]
    )

    st.write("### Please Login or Signup to Continue")
    tab = st.radio("Select", ["🔐 Login", "📝 Signup"], horizontal=True)

    if tab == "🔐 Login":
        if st.button("➡ Go to Login", use_container_width=True):
            st.session_state.page = "login"
    else:
        if st.button("➡ Go to Signup", use_container_width=True):
            st.session_state.page = "signup"

# === Use Case Wrappers with Back Button ===
def wrapped_crop_ui():
    crop_recommendation_ui()
    if st.button("🔙 Back to Chatbot"):
        st.session_state.page = "dashboard"

def wrapped_market_ui():
    market_price_ui()
    if st.button("🔙 Back to Chatbot"):
        st.session_state.page = "dashboard"

def wrapped_disease_ui():
    disease_detection_ui()
    if st.button("🔙 Back to Chatbot"):
        st.session_state.page = "dashboard"

def wrapped_advisor_ui():
    advisor_ui()
    if st.button("🔙 Back to Chatbot"):
        st.session_state.page = "dashboard"

# === Router ===
def route():
    page = st.session_state.page
    if page == "home":
        show_logo_page()
    elif page == "login":
        login_page()
    elif page == "signup":
        signup_page()
    elif page == "dashboard":
        chatbot_home()
    elif page == "crop_recommend":
        wrapped_crop_ui()
    elif page == "market_price":
        wrapped_market_ui()
    elif page == "disease_detect":
        wrapped_disease_ui()
    elif page == "chatbot":
        wrapped_advisor_ui()

# === Launch ===
route()














