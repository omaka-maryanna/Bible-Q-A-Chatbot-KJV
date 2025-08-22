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
# SESSION STATE
# ------------------------
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ------------------------
# LOGIN PAGE
# ------------------------
if not st.session_state.authenticated:
    st.title("🔑 Welcome to Bibli Q&A (KJV)")
    st.write("Please log in with your email and password:")

    with st.form("login_form"):
        email = st.text_input("Email Address")
        password = st.text_input("Password", type="password")
        show_pass = st.checkbox("👁 Show Password")
        if show_pass:
            st.text_input("Password (visible)", value=password, type="default", disabled=True)

        submit = st.form_submit_button("Login")

        if submit:
            if email.strip() and password.strip():
                # Save session
                st.session_state.authenticated = True
                st.session_state.user_email = email

                # Save to users.csv
                user_data = {"Email": [email], "Password": [password]}
                df = pd.DataFrame(user_data)
                if os.path.exists("users.csv"):
                    df.to_csv("users.csv", mode="a", header=False, index=False)
                else:
                    df.to_csv("users.csv", index=False)

                st.success("Login successful! 🎉")
                st.rerun()
            else:
                st.error("Email and Password are required.")

# ------------------------
# MAIN CHAT PAGE
# ------------------------
if st.session_state.authenticated:
    st.title("📖 Biblia Q&A Chatbot (KJV)")

    # ---- Sidebar: Logout + Chat History ----
    if st.sidebar.button("🚪 Logout"):
        st.session_state.authenticated = False
        st.session_state.pop("user_email", None)
        st.success("You have been logged out.")
        st.rerun()

    st.sidebar.subheader("💬 Chat History")
    if st.session_state.chat_history:
        for chat in st.session_state.chat_history:
            st.sidebar.write(f"**You:** {chat['question']}")
            st.sidebar.write(f"**AI:** {chat['answer']}")
            st.sidebar.write("---")
    else:
        st.sidebar.info("No chat history yet.")

    # New Chat Button only
    if st.button("🆕 New Chat"):
        st.session_state.chat_history = []
        st.success("Started a new chat.")

    # Chat Input
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
            st.subheader("📖 Biblia Answer:")
            prompt = f"Using the King James Bible, answer the following question:\n\n{user_input}\n\nRelevant verses: {verses['Text'].tolist()}"
            ai_response = ask_groq(prompt)
            st.write(ai_response)

            # Save to history
            st.session_state.chat_history.append({"question": user_input, "answer": ai_response})
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