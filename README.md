# AI Resume Analyzer

Existing interface and analysis behavior preserved. Two Python modules run in one application; this is not a separate HTTP API or a multipage interface.

frontend.py: Streamlit UI, styles, session state and result display.
backend.py: PDF reading, skill matching, score calculation and Groq requests.

Keep your existing .env beside backend.py, or copy .env.example to .env and enter your own key.

Run from this folder:

    python -m pip install -r requirements.txt
    python -m streamlit run frontend.py

Do not run backend.py separately.
Original credentials, virtual environment and Git history are not included.
