import streamlit as st
import pandas as pd
import os
from groq_api import ask_groq

# Load KJV Bible CSV
@st.cache_data
def load_bible_data():
    return pd.read_csv("kjv.csv", skiprows=5)

bible_df = load_bible_data()

def search_relevant_verses(query):
    matches = bible_df[bible_df['Text'].str.contains(query, case=False, na=False)]
    return matches

# Streamlit page settings
st.set_page_config(page_title="📖 Bible Q&A (KJV) — Omaka", layout="centered")

# ------------------------
# LOGIN FORM (name + email)
# ------------------------
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.title("🔑 Welcome to Bible Q&A (KJV)")
    st.write("Please enter your details to continue:")

    with st.form("login_form"):
        name = st.text_input("Full Name")
        email = st.text_input("Email Address")
        submit = st.form_submit_button("Enter")

        if submit:
            if name.strip() and email.strip():
                # Store session data
                st.session_state.authenticated = True
                st.session_state.user_name = name
                st.session_state.user_email = email  

                # Save to users.csv
                user_data = {"Name": [name], "Email": [email]}
                df = pd.DataFrame(user_data)
                if os.path.exists("users.csv"):
                    df.to_csv("users.csv", mode="a", header=False, index=False)
                else:
                    df.to_csv("users.csv", index=False)

                st.success(f"Welcome, {name}! 🎉")
            else:
                st.error("Both name and email are required.")

# ------------------------
# MAIN APP (only if logged in)
# ------------------------
if st.session_state.authenticated:
    st.title("📖 Bible Q&A Chatbot (KJV)")

    user_input = st.text_input("Ask a question about the Bible:")

    if st.button("Search"):
        if user_input.strip():
            verses = search_relevant_verses(user_input)
            st.subheader("🔍 Relevant Bible Verses:")
            if not verses.empty:
                for _, row in verses.iterrows():
                    st.write(f"**{row['Book Name']} {row['Chapter']}:{row['Verse']}** — {row['Text']}")
            else:
                st.write("No matching verses found.")

            # Ask Groq
            st.subheader("🤖 AI Answer:")
            prompt = f"Using the King James Bible, answer the following question:\n\n{user_input}\n\nRelevant verses: {verses['Text'].tolist()}"
            ai_response = ask_groq(prompt)
            st.write(ai_response)
        else:
            st.warning("Please enter a question.")

    # ------------------------
    # ADMIN PANEL (only for you: Omaka Maryanna)
    # ------------------------
    if st.session_state.get("user_email") == "omakamaryanna2018@gmail.com":
        st.sidebar.subheader("🔒 Admin Panel — Omaka Maryanna")
        if os.path.exists("users.csv"):
            users_df = pd.read_csv("users.csv")
            st.sidebar.write("### Registered Users")
            st.sidebar.dataframe(users_df)
            st.sidebar.download_button("⬇️ Download users.csv", users_df.to_csv(index=False), "users.csv")
        else:
            st.sidebar.write("No users registered yet.")