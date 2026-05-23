import streamlit as st
import google.generativeai as genai
import os
from PIL import Image

# ==========================================
# 1. CORE SYSTEM CONFIGURATION
# ==========================================
st.set_page_config(page_title="April OS", page_icon="⚡", layout="centered")

api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    st.error("Missing GEMINI_API_KEY. Please add it to your Streamlit Secrets.")
else:
    genai.configure(api_key=api_key)

# ==========================================
# 2. FUTURE UPGRADE MODULE SLOTS (MODULAR)
# ==========================================
def search_youtube_videos(query):
    """Placeholder module: Will fetch live links using YouTube API later"""
    return [
        f"📺 Search Result 1 for '{query}': https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
    ]

def generate_ai_image(prompt):
    """Placeholder module: Will connect to Google Imagen model later"""
    st.info(f"🎨 Image generator module triggered for: '{prompt}'")
    return None

# ==========================================
# 3. WAKE-WORD DETECTION ENGINE
# ==========================================
def parse_wake_word(user_text):
    clean_text = user_text.lower().strip(".,?! ")
    greetings = ["hey", "hi", "hello", "yo", "ok", "okay"]
    words = clean_text.split()
    
    if not words:
        return False, user_text
        
    starting_index = 0
    if words[0] in greetings and len(words) > 1:
        starting_index = 1
        
    if words[starting_index] == "april":
        # Reconstruction of remaining text without wake words
        raw_words = user_text.split()
        actual_prompt = " ".join(raw_words[starting_index + 1:])
        return True, actual_prompt.strip(",?! ")
        
    return False, user_text

# ==========================================
# 4. CHAT HISTORY INTERFACE
# ==========================================
st.markdown("### ⚡ April Core Interface")

if "history" not in st.session_state:
    st.session_state.history = []

for chat in st.session_state.history:
    with st.chat_message(chat['role']):
        st.markdown(chat['content'])

# ==========================================
# 5. INTELLIGENT ROUTER
# ==========================================
user_input = st.chat_input("Awaiting command...")

if user_input:
    is_triggered, clean_prompt = parse_wake_word(user_input)
    
    if is_triggered:
        # Show what user said instantly
        with st.chat_message("user"):
            st.markdown(user_input)
        st.session_state.history.append({"role": "user", "content": user_input})
        
        # Route to specific task modules based on keywords
        with st.chat_message("assistant"):
            with st.spinner("Processing..."):
                
                # ROUTE A: Video Search Request
                if "video" in clean_prompt.lower() or "youtube" in clean_prompt.lower():
                    links = search_youtube_videos(clean_prompt)
                    response_text = f"I found some video resources for you:\n\n" + "\n".join(links)
                
                # ROUTE B: Image Generation Request
                elif "generate an image" in clean_prompt.lower() or "draw" in clean_prompt.lower():
                    generate_ai_image(clean_prompt)
                    response_text = "I've initialized the image generation module shell. Full API hook coming next!"
                
                # ROUTE C: Standard Text/Thought Engine
                else:
                    try:
                        model = genai.GenerativeModel('gemini-pro')
                        response = model.generate_content(clean_prompt)
                        response_text = response.text
                    except Exception as e:
                        response_text = f"Error communicating with brain core: {str(e)}"
                
                st.markdown(response_text)
                st.session_state.history.append({"role": "assistant", "content": response_text})
    else:
        st.toast("System Idle. Say 'April' or 'Hey April' to wake me up.")
