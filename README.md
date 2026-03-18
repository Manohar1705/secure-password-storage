# 🔐 Secure Password Storage Using Hash Functions

A simple Streamlit app that demonstrates secure password storage using **SHA-256 hashing with salt**.

## 🚀 Live Demo

👉 https://securepasswordstorage.streamlit.app/

## 📌 Features

* User Registration & Login
* Password hashing (SHA-256)
* Unique salt for each user
* No plain text password storage

## 🔐 Security Difference (If Database is Hacked)

* **Without Hashing (Normal Systems):**

  * Passwords are stored in plain text
  * If database is hacked → attacker can see all passwords
  * High risk of account takeover

* **With Hashing (This Project):**

  * Only hashed passwords are stored
  * Even if database is hacked → passwords are not readable
  * Attacker cannot directly use the passwords
  * Salting prevents common attacks like rainbow tables

👉 Key Idea:
**Even if data is stolen, actual passwords remain protected.**

## 🛠️ Tech Stack

* Python
* Streamlit

## ▶️ Run Locally

```id="xhhg3l"
pip install streamlit
streamlit run app.py
```

## ⚠️ Note

This is a demo project with temporary storage. In real-world systems, databases and stronger hashing algorithms like bcrypt are used.
