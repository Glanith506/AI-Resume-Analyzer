# ResumeLens

A resume analyzer with a document-based learning assistant.

Built by Glanith Dcunha.

## Features

- Compare a PDF resume with a job description.
- View matching skills and skills not detected in the resume.
- Get optional AI feedback on the resume.
- Upload learning notes and ask questions about them.
- View the source passages used to generate answers.
- Keep learning documents indexed between app restarts.
- Remove saved documents and skip duplicate uploads.

## Technologies

- Python and Streamlit
- pypdf and regular expressions
- Sentence Transformers: all-MiniLM-L6-v2
- ChromaDB
- Groq SDK: openai/gpt-oss-20b

## Setup on Windows

Use Python 3.11. Open the project folder in VS Code and run:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements-windows-cpu.txt
```

Create a file named `.env` beside `backend.py`:

```env
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=openai/gpt-oss-20b
```

The Groq key is needed for AI feedback and generated learning answers.
Skill matching works without it.

Check ChromaDB:

```powershell
.\.venv\Scripts\python.exe check_chroma.py
```

Start the app:

```powershell
.\.venv\Scripts\python.exe -m streamlit run frontend.py
```

Open the Local URL shown in the terminal.

The embedding model downloads from Hugging Face on first use.
Internet access is required for the initial download and Groq requests.

## How to use

1. Upload a text-based PDF resume.
2. Paste a job description and run the analysis.
3. Review the detected skill matches and gaps.
4. Upload PDF, TXT, or Markdown learning notes and save them.
5. Ask a question about the notes.
6. Review the answer and its source references.

Saved learning documents remain available after restarting the app.

## How the RAG feature works

The app extracts document text and splits it into overlapping passages.
MiniLM converts each passage into an embedding, which is saved in ChromaDB.

When a question is submitted, the app searches for relevant passages.
Those passages are sent to Groq to generate an answer with source references.

## Data storage

The learning index is stored locally in `data/chroma`.

It contains extracted text, embeddings, filenames, and page references.
Original uploaded files are not copied into this folder.

Keep the folder to retain the index. Back it up while the app is stopped.
Identical uploads are skipped. Changed files are indexed as new versions.

This version is intended for personal local use and has no user authentication.

## Limits

- Up to 10 saved learning documents and 2,000 passages.
- Maximum upload size of 10 MB per file.
- Learning PDFs can contain up to 100 pages.
- Scanned PDFs require OCR, which is not included.
- Skill coverage uses a predefined keyword list; it is not an ATS score.
- A missing keyword does not necessarily mean the user lacks that skill.
- AI answers and source references should be checked for accuracy.

AI feedback sends resume text and the job description to Groq.
Learning answers send the question, missing-skill names, and retrieved passages.

## Tests

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

Tests cover skill matching, document chunking, retrieval, duplicate handling,
document removal, and persistence across Python processes.

## Windows troubleshooting

If PyTorch or ChromaDB fails with a DLL error or access violation,
install or repair the latest Microsoft Visual C++ x64 Redistributable,
restart Windows, and rerun `check_chroma.py`.

## Git exclusions

Keep these local files out of the repository:

```gitignore
.env
.venv/
data/
__pycache__/
.pytest_cache/
*.log
run_log.txt
```
