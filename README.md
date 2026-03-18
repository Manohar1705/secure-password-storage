# 🔐 Secure Password Storage Using Hash Functions

A simple Streamlit app that demonstrates secure password storage using **SHA-256 hashing with salt**.

## 🚀 Live Demo

👉 https://securepasswordstorage.streamlit.app/

## 📌 Features

* User Registration & Login
* Password hashing (SHA-256)
* Unique salt for each user
* No plain text password storage

## ⚖️ Difference: Real Database vs This Project

* **Real Database:**

  * Stores data permanently
  * Used in real-world applications
  * Requires setup (MySQL, PostgreSQL, etc.)

* **This Project:**

  * Uses temporary session storage
  * Data resets on refresh
  * Built for demonstration of **security concepts**

👉 Key point:
**Security comes from hashing, not from the database itself.**

## 🛠️ Tech Stack

* Python
* Streamlit

## ▶️ Run Locally

```id="o48g4t"
pip install streamlit
streamlit run app.py
```

## ⚠️ Note

This is a demo project. In real systems, databases and stronger hashing methods like bcrypt are used.
