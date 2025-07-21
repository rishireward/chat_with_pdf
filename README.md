# Chat with PDF (Quiz & Quest Documentation)

This Streamlit app allows you to chat with your PDF documentation using Groq's LLaMA 3 model and LangChain.

## Features

- Upload a PDF
- Ask questions about the content
- Backed by FAISS, LangChain, and LLaMA 3

## Setup

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deployment

You can deploy this to:
- [Render](https://render.com/)
- [Streamlit Community Cloud](https://streamlit.io/cloud) (free)

## API Key

Add a `.streamlit/secrets.toml` file:

```toml
GROQ_API_KEY = "your-groq-api-key"
```
