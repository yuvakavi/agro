import streamlit as st

def chatbot_home():
    st.markdown("### 🤖 Welcome to AgroBot Chat")

    # 🌐 Language selection
    lang = st.selectbox("🌍 Select Language / மொழியை தேர்ந்தெடுக்கவும்", ["English", "தமிழ்"], key="language")
    st.session_state['lang'] = lang  # Store selected language

    st.markdown("#### Please select a service below:" if lang == "English" else "தயவுசெய்து சேவையைத் தேர்ந்தெடுக்கவும்:")

    # 🟩 Vertical button layout
    st.button("🌾 Crop Recommendation" if lang == "English" else "🌾 பயிர் பரிந்துரை", 
              key="crop", use_container_width=True, on_click=lambda: setattr(st.session_state, 'page', 'crop_recommend'))

    st.button("📈 Market Price Analysis" if lang == "English" else "📈 சந்தை விலை பகுப்பாய்வு", 
              key="market", use_container_width=True, on_click=lambda: setattr(st.session_state, 'page', 'market_price'))

    st.button("🦠 Disease Detection & Treatment" if lang == "English" else "🦠 நோய் கண்டறிதலும் சிகிச்சையும்", 
              key="disease", use_container_width=True, on_click=lambda: setattr(st.session_state, 'page', 'disease_detect'))

    st.button("🧠 Crop Advisory Chatbot" if lang == "English" else "🧠 பயிர் ஆலோசனை", 
              key="advisory", use_container_width=True, on_click=lambda: setattr(st.session_state, 'page', 'chatbot'))

    st.markdown("---")

    st.button("🔙 Back to Dashboard" if lang == "English" else "🔙 டாஷ்போர்டுக்கு திரும்பு", 
              use_container_width=True, on_click=lambda: setattr(st.session_state, 'page', 'dashboard'))


