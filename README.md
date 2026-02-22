# NewsGPT (Samvaad GPT)

A production-style, modular Streamlit app that answers user questions using **real-time news** from **NewsData.io** and generates grounded responses via the **Gemini API**.

## Run locally

1. Create a virtual environment and install dependencies:

```bash
pip install -r requirements.txt
```

2. Create a `.env` file (copy from `.env.example`) and fill in keys:

- `GEMINI_API_KEY`
- `NEWSDATA_API_KEY`

3. Start the app:

```bash
streamlit run app/ui/streamlit_app.py
```

## Notes

- Conversation memory is stored per-session using `st.session_state.messages`.
- The app uses simulated ChatGPT-style streaming (word-by-word) for Streamlit stability.
- A `logs/app.log` file is written automatically.
