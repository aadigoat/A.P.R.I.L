import streamlit as st
import google.generativeai as genai
import os

# ==========================================
# 1. CORE SYSTEM CONFIGURATION
# ==========================================
st.set_page_config(page_title="April OS", page_icon="⚡", layout="centered")

api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    st.error("Missing GEMINI_API_KEY. Please add it to your Streamlit Secrets.")
else:
    genai.configure(api_key=api_key)

# Initialize persistent session states
if "history" not in st.session_state:
    st.session_state.history = []
if "latest_response" not in st.session_state:
    st.session_state.latest_response = "Awaiting command... Say 'April' to wake me up."
# New state tracker for voice commands
if "voice_muted" not in st.session_state:
    st.session_state.voice_muted = False

# ==========================================
# 2. INTERFACE & LAYOUT MANAGEMENT
# ==========================================
with st.sidebar:
    st.markdown("### ⚙️ System Status")
    status_color = "🔴 Muted" if st.session_state.voice_muted else "🔊 Active"
    st.markdown(f"**Voice Mode:** {status_color}")
    st.divider()
    st.markdown("*April OS v1.2 — Voice Commands Enabled*")

st.markdown("## ⚡ April Core Interface")

# Dedicated section showing her latest text transmission
st.markdown("### 📢 Latest Transmission")
st.info(st.session_state.latest_response)
st.divider()

# ==========================================
# 3. FUTURE UPGRADE MODULE SLOTS
# ==========================================
def search_youtube_videos(query):
    return [f"📺 Video Result for '{query}': https://www.youtube.com/results?search_query={query.replace(' ', '+')}"]

def generate_ai_image(prompt):
    st.info(f"🎨 Image generator triggered for: '{prompt}'")
    return None

# ==========================================
# 4. WAKE-WORD & VOICE COMMAND DETECTION
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
        raw_words = user_text.split()
        actual_prompt = " ".join(raw_words[starting_index + 1:])
        return True, actual_prompt.strip(",?! ")
        
    return False, user_text

# ==========================================
# 5. CHAT LOG DISPLAY
# ==========================================
st.markdown("#### 💬 Session Logs")
for chat in st.session_state.history:
    with st.chat_message(chat['role']):
        st.markdown(chat['content'])

# ==========================================
# 6. INTELLIGENT ROUTER & VOICE RUNTIME
# ==========================================
user_input = st.chat_input("Awaiting command...")

if user_input:
    is_triggered, clean_prompt = parse_wake_word(user_input)
    
    if is_triggered:
        # Log user input instantly
        with st.chat_message("user"):
            st.markdown(user_input)
        st.session_state.history.append({"role": "user", "content": user_input})
        
        with st.chat_message("assistant"):
            with st.spinner("Processing..."):
                
                # VOICE COMMAND INTERCEPT: "Mute"
                if clean_prompt.lower() == "mute":
                    st.session_state.voice_muted = True
                    response_text = "Understood. Audio muted. I will respond using only text from now on."
                
                # VOICE COMMAND INTERCEPT: "Unmute"
                elif clean_prompt.lower() == "unmute":
                    st.session_state.voice_muted = False
                    response_text = "Audio system restored. I will speak my responses to you again."
                
                # ROUTE A: Video Search
                elif "video" in clean_prompt.lower() or "youtube" in clean_prompt.lower():
                    links = search_youtube_videos(clean_prompt)
                    response_text = f"I found some video resources for you:\n\n" + "\n".join(links)
                
                # ROUTE B: Image Generation
                elif "generate an image" in clean_prompt.lower() or "draw" in clean_prompt.lower():
                    generate_ai_image(clean_prompt)
                    response_text = "I've initialized the image generation module shell. Full API hook coming next!"
                
                # ROUTE C: Gemini Standard Text Brain
                else:
                    try:
                        model = genai.GenerativeModel('gemini-pro')
                        response = model.generate_content(clean_prompt)
                        response_text = response.text
                    except Exception as e:
                        response_text = f"Error communicating with brain core: {str(e)}"
                
                # Save her text response
                st.markdown(response_text)
                st.session_state.latest_response = response_text
                st.session_state.history.append({"role": "assistant", "content": response_text})
                
                # Play audio ONLY if voice isn't muted
                if not st.session_state.voice_muted:
                    # Voice placeholder (Will swap with our real TTS API file next)
                    st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3") 
                    st.caption("🔊 Audio clip streaming...")
                else:
                    st.toast("Voice muted. Response sent silently to transmission box.")
                    
        st.rerun()
    else:
        st.toast("System Idle. Say 'April' or 'Hey April' to wake me up.")
