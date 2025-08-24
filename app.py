import streamlit as st
import jwt
import time
import datetime
import json
import os

# -----------------------------
# CONFIG
# -----------------------------
SECRET_KEY = "supersecretkey123"
CHAT_FILE = "chat.json"

# Simple user database for demo
USERS = {
    "alice": "password123",
    "bob": "mypassword"
}

# -----------------------------
# JWT HELPER FUNCTIONS
# -----------------------------
def create_token(username: str):
    payload = {
        "user": username,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

def verify_token(token: str):
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return decoded["user"]
    except Exception:
        return None

# -----------------------------
# CHAT STORAGE
# -----------------------------
def load_messages():
    if not os.path.exists(CHAT_FILE):
        with open(CHAT_FILE, "w") as f:
            json.dump([], f)
    with open(CHAT_FILE, "r") as f:
        return json.load(f)

def save_messages(messages):
    with open(CHAT_FILE, "w") as f:
        json.dump(messages, f)

# -----------------------------
# SESSION STATE INIT
# -----------------------------
if "token" not in st.session_state:
    st.session_state["token"] = None

# -----------------------------
# STREAMLIT UI
# -----------------------------
st.set_page_config(page_title="Secure Chat", layout="wide")
st.title("🔐 Secure Chat App")

# LOGIN FORM
if st.session_state["token"] is None:
    st.subheader("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username in USERS and USERS[username] == password:
            st.session_state["token"] = create_token(username)
            st.success("✅ Logged in successfully!")
            st.rerun()
        else:
            st.error("❌ Invalid username or password")

# CHAT INTERFACE
else:
    user = verify_token(st.session_state["token"])
    if not user:
        st.error("⚠️ Session expired. Please login again.")
        st.session_state["token"] = None
        st.rerun()

    st.sidebar.success(f"Logged in as: {user}")
    if st.sidebar.button("Logout"):
        st.session_state["token"] = None
        st.rerun()

    st.subheader("💬 Chat Room")

    # Load messages
    messages = load_messages()

    # Display messages
    for msg in messages:
        timestamp = datetime.datetime.fromtimestamp(msg["time"]).strftime("%H:%M:%S")
        st.write(f"[{timestamp}] *{msg['user']}*: {msg['text']}")

    # Input box
    new_msg = st.text_input("Type your message...")
    if st.button("Send"):
        if new_msg.strip():
            messages.append(
                {"user": user, "text": new_msg, "time": time.time()}
            )
            save_messages(messages)
            st.rerun()