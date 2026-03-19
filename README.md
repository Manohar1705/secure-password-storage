# 🔐 Secure Password Storage Using Hash Functions

A Streamlit application that demonstrates secure password storage using **bcrypt hashing** and a simple authentication system.

---

## 🚀 Live Demo

👉 https://securepasswordstorage.streamlit.app/

---

## 📌 Features

* User Registration & Login
* Password hashing using **bcrypt**
* Password reset functionality
* SQLite database storage
* Activity logs and dashboard
* No plain text password storage

---

## 🔐 Security

* Passwords are stored as **hashed values**, not plain text
* bcrypt adds salting and makes brute-force attacks difficult
* Even if the database is compromised, passwords remain protected

---

## 🛠️ Tech Stack

* Python
* Streamlit
* SQLite
* bcrypt

---

## ▶️ Run Locally

```bash id="4j2cru"
pip install -r requirements.txt
streamlit run app.py
```

---

## ⚠️ Note

This is a demo project. Real systems use advanced security and authentication mechanisms.
