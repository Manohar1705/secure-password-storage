import streamlit as st
import hashlib
import os

# ---------------- SESSION STORAGE ----------------
if "users" not in st.session_state:
    st.session_state.users = {}

# ---------------- FUNCTIONS ----------------

def generate_salt():
    return os.urandom(16).hex()

def hash_password(password, salt):
    return hashlib.sha256((password + salt).encode()).hexdigest()

def register_user(username, password):
    if username in st.session_state.users:
        return False, "User already exists"

    salt = generate_salt()
    hashed = hash_password(password, salt)

    st.session_state.users[username] = {
        "salt": salt,
        "password": hashed
    }

    return True, "Registered successfully"

def login_user(username, password):
    if username not in st.session_state.users:
        return False, "User not found"

    salt = st.session_state.users[username]["salt"]
    hashed = hash_password(password, salt)

    if hashed == st.session_state.users[username]["password"]:
        return True, "Login successful"

    return False, "Incorrect password"

# ---------------- UI ----------------

st.set_page_config(page_title="Secure Password Storage", page_icon="🔐")

st.title("🔐 Secure Password Storage Using Hash Functions")

menu = ["Register", "Login"]
choice = st.sidebar.selectbox("Menu", menu)

# ---------------- REGISTER ----------------

if choice == "Register":
    st.subheader("Create Account")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Register"):
        success, msg = register_user(username, password)
        if success:
            st.success(msg)
        else:
            st.error(msg)

# ---------------- LOGIN ----------------

elif choice == "Login":
    st.subheader("Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        success, msg = login_user(username, password)
        if success:
            st.success(msg)
        else:
            st.error(msg)

# ---------------- FOOTER ----------------

st.markdown("---")
st.caption("Passwords are hashed using SHA-256 with salt. No plain text storage.")
st.caption("Note: Data is temporary (session-based).")