import streamlit as st
import sqlite3
import bcrypt
import pandas as pd
from datetime import datetime

# ---------------- DATABASE ----------------

conn = sqlite3.connect("users.db", check_same_thread=False)
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS users (
    username TEXT PRIMARY KEY,
    password BLOB,
    created_at TEXT
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS logs (
    activity TEXT,
    time TEXT
)
""")

conn.commit()

# ---------------- SESSION ----------------

if "total_attempts" not in st.session_state:
    st.session_state.total_attempts = 0

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "current_user" not in st.session_state:
    st.session_state.current_user = ""

if "show_reset" not in st.session_state:
    st.session_state.show_reset = False

if "login_msg" not in st.session_state:
    st.session_state.login_msg = ""

# ---------------- FUNCTIONS ----------------

def log_activity(activity):
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute("INSERT INTO logs VALUES (?, ?)", (activity, time))
    conn.commit()

def register_user(username, password):
    c.execute("SELECT * FROM users WHERE username=?", (username,))
    if c.fetchone():
        return False, "Username already exists. Try another."

    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    c.execute("INSERT INTO users VALUES (?, ?, ?)",
              (username, hashed, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()

    log_activity(f"{username} registered")
    return True, "Registered successfully"

def login_user(username, password):
    c.execute("SELECT password FROM users WHERE username=?", (username,))
    result = c.fetchone()

    st.session_state.total_attempts += 1

    if not result:
        return False, "User not found"

    stored_password = result[0]

    if bcrypt.checkpw(password.encode(), stored_password):
        log_activity(f"{username} login success")
        return True, "Login successful"
    else:
        log_activity(f"{username} login failed")
        return False, "Incorrect password"

def reset_password(username, new_password):
    c.execute("SELECT * FROM users WHERE username=?", (username,))
    if not c.fetchone():
        return False, "User not found"

    hashed = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt())

    c.execute("UPDATE users SET password=? WHERE username=?",
              (hashed, username))
    conn.commit()

    log_activity(f"{username} password reset")
    return True, "Password updated successfully"

# ---------------- UI ----------------

st.set_page_config(page_title="Secure Password System", page_icon="🔐")
st.markdown("## 🔐 Secure Password Storage System")

# ---------------- BEFORE LOGIN ----------------

if not st.session_state.logged_in:

    tab1, tab2 = st.tabs(["Login", "Register"])

    # -------- LOGIN --------
    with tab1:
        st.subheader("Login")

        username = st.text_input("Username", key="login_user")
        password = st.text_input("Password", type="password", key="login_pass")

        col1, col2, col3 = st.columns([2, 5, 2])

        with col1:
            if st.button("Login"):
                success, msg = login_user(username, password)
                st.session_state.login_msg = msg

                if success:
                    st.session_state.logged_in = True
                    st.session_state.current_user = username
                    st.rerun()

        with col3:
            if st.button("Forgot Password?"):
                st.session_state.show_reset = True

        if st.session_state.login_msg:
            if st.session_state.login_msg == "Login successful":
                st.success(st.session_state.login_msg)
            else:
                st.error(st.session_state.login_msg)

        # ---- RESET PASSWORD ----
        if st.session_state.show_reset:
            st.subheader("Reset Password")

            user = st.text_input("Username", key="reset_user")
            new_pass = st.text_input("New Password", type="password", key="new_pass")
            confirm_pass = st.text_input("Confirm Password", type="password", key="confirm_pass")

            if st.button("Update Password"):
                if new_pass != confirm_pass:
                    st.error("Passwords do not match")
                else:
                    success, msg = reset_password(user, new_pass)
                    if success:
                        st.success(msg)
                        st.session_state.show_reset = False
                    else:
                        st.error(msg)

    # -------- REGISTER --------
    with tab2:
        st.subheader("Create Account")

        username = st.text_input("Username", key="reg_user")
        password = st.text_input("Password", type="password", key="reg_pass")

        if password:
            if len(password) < 6:
                st.warning("Weak password")
            elif len(password) < 10:
                st.info("Medium strength password")
            else:
                st.success("Strong password")

        if st.button("Register"):
            if len(password) < 6:
                st.error("Password must be at least 6 characters")
            else:
                success, msg = register_user(username, password)
                if success:
                    st.success(msg)
                else:
                    st.error(msg)

# ---------------- AFTER LOGIN ----------------

else:

    header = st.columns([8, 2])

    with header[0]:
        st.subheader("Security Dashboard")

    with header[1]:
        if st.button("Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.current_user = ""
            st.rerun()

    st.info(f"Logged in as: {st.session_state.current_user}")

    st.divider()

    # Metrics
    c.execute("SELECT COUNT(*) FROM users")
    total_users = c.fetchone()[0]

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Users", total_users)

    with col2:
        st.metric("Total Attempts", st.session_state.total_attempts)

    st.divider()

    # Users table (FIXED)
    st.subheader("👥 Registered Users")
    c.execute("SELECT username, created_at FROM users")
    users = c.fetchall()
    df_users = pd.DataFrame(users, columns=["Username", "Created At"])
    st.dataframe(df_users, use_container_width=True, hide_index=True)

    st.divider()

    # Logs
    st.subheader("📜 Activity Logs")
    c.execute("SELECT activity, time FROM logs ORDER BY time DESC")
    logs = c.fetchall()
    df_logs = pd.DataFrame(logs, columns=["Activity", "Time"])

    if df_logs.empty:
        st.warning("No activity yet")
    else:
        st.dataframe(df_logs, use_container_width=True, hide_index=True)

    if st.button("🗑️ Clear Activity Logs"):
        c.execute("DELETE FROM logs")
        conn.commit()
        st.success("Logs cleared successfully")
        st.rerun()
