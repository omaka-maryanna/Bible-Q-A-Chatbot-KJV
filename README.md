**BIBLIA CHATBOT**

This an AI driven chatbot that allows you to ask quetions from the bibie,
you can simply ask questons like, what does the bible says about forgiveness
and biblia will give you a clear explanation with backup scriptures for your
reference.

It is fast, easy and available for all believer who wants a more interactive 
bible study


##  Features

*  **User Authentication** (Login & Logout system with email + password)
*  **Ask Bible Questions** → Answers generated from the **KJV dataset**
*  **Groq-Powered Responses** → Ultra-fast, real-time answers
*  **Chat History** → Keeps track of past conversations
*  **Password Toggle** → Show/hide password during login
*   **Clean Streamlit UI** for smooth interaction


## Tech Stack

* **Frontend/UI** → [Streamlit](https://streamlit.io/)
* **Backend API** → [Groq LLM](https://groq.com/)
* **Dataset** → King James Version (KJV) Bible
* **Language** → Python 3.10+


##  Installation

1. **Clone the repository**

```bash
git clone https://github.com/<your-username>/Biblia-Chatbot.git
cd Biblia-Chatbot
```

2. **Set up a virtual environment**

```bash
python -m venv venv
source venv/bin/activate   # On Mac/Linux
venv\Scripts\activate      # On Windows
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
   Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key
```

##  Run the App

```bash
streamlit run app.py
```

## Deployment

You can deploy on:

* **[Streamlit Cloud](https://streamlit.io/cloud)** (recommended)
* **Render / Vercel / Railway** for scalable hosting


##  Author

 **Maryanna Omaka**
 [omakamaryanna2018@gmail.com]
