# ResumeLens — AI Resume Analyzer + Persistent ChromaDB RAG
Developed by Glanith Dcunha.

## Updating an existing copy (start here)
1. Stop Streamlit with Ctrl+C and make a backup of your current project.
2. Extract this ZIP into a separate folder. Copy the updated `rag.py`, `frontend.py`, `check_chroma.py`, requirements files, README.md and UPGRADE.md into your existing ResumeLens_RAG folder. You can copy the remaining source/test files too.
3. Keep your existing `.env`, `.venv` and any `data` folder. Do not overwrite or delete them. There are no credentials or database files in this ZIP.
4. Your working Windows torch 2.8.0+cpu remains installed. Run with that existing environment:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-windows-cpu.txt
.\.venv\Scripts\python.exe -X faulthandler check_chroma.py
```
This first command may update packages to meet the supplied ranges; it is not a fully locked environment. The diagnostic checks native Chroma insertion and cross-process reopening using synthetic vectors; it does not need a model download or API key. If it fails, save the terminal output and do not repeatedly build the real index. Persistence does not by itself repair the native Windows access violation seen earlier.

If the check passes, start:

```powershell
.\.venv\Scripts\python.exe -m streamlit run frontend.py
```
Open the Local URL printed in the terminal and keep that terminal running.

## New Windows installation (Python 3.11)
Open the extracted ResumeLens_RAG folder in VS Code. From the folder containing frontend.py:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements-windows-cpu.txt
Copy-Item .env.example .env
```
Edit `.env`: set your Groq key. Keep it beside backend.py.

```env
GROQ_API_KEY=your_key
GROQ_MODEL=openai/gpt-oss-20b
```
Run the diagnostic and start commands above. No environment activation or second API server is required.
For macOS/Linux use Python 3.11+, install requirements.txt in a virtual environment and start `python -m streamlit run frontend.py`. The separate Windows requirements file selects the CPU build that imported successfully on your laptop.

## Use the saved learning index
1. Analyze your PDF resume against a pasted job description as before. AI resume feedback remains optional.
2. Under Learn the skills, upload PDF/TXT/Markdown learning notes.
3. Click Add documents to saved knowledge base. MiniLM downloads on first use, then embeddings run locally.
4. Ask a question covered in your notes, enable the Groq checkbox and generate an answer with source references.
5. Stop Streamlit, restart it, and return to the learning section. The saved documents and passage count appear automatically; no re-upload or rebuild is needed. The model still loads into RAM when needed to embed a new question.
6. Re-uploading the exact same file, even with another filename, skips saved passages. The original indexed filename remains the source label. Modifying a file creates a new document version; explicitly remove the older version when desired.
7. Expand Manage saved documents to remove one document or clear the index, with an explicit confirmation checkbox.

## Storage and persistence
- Uses `chromadb.PersistentClient`, not EphemeralClient or a NumPy-only replacement.
- Database folder: `data/chroma` beside rag.py, independent of the terminal's working directory.
- Collection: `resumelens_learning_v2`, reused on every start.
- Saved data: extracted learning text, embeddings, filenames, page numbers, passage numbers and document SHA-256 IDs. Original PDF files are not copied into the database. Resume uploads and AI answers are not persisted by this feature.
- Back up the entire `data/chroma` folder while Streamlit is stopped. Keep it when moving the project. Losing that folder loses the saved index.
- No cloud database account or additional embedding API key is required. This is one personal local index shared by tabs using this app on your computer. It has no user authentication; use locally, not as a public multi-user deployment.
- Deleting a document affects that document's saved passages. Clear removes this app's saved collection, not arbitrary folders or other Chroma collections.
- Normal close and file-uploader changes never delete the index. Chroma handles persistence automatically. Collection model/chunk metadata is checked to avoid mixing incompatible indexes.
- SHA-256 IDs and idempotent upserts permit retry after a partial insertion: previously completed passages are skipped. This is not a multi-document atomic transaction.
- Maximum: 10 saved documents, 2,000 saved passages, 10 MB per uploaded file and 100 pages per PDF.

## RAG architecture
PDF/TXT/MD → page text → 900-character passages with 200-character overlap → Sentence Transformers all-MiniLM-L6-v2 → explicit normalized embeddings → persistent Chroma cosine index.
Question → same embedding model → up to four saved passages above similarity 0.30 → Groq chat generation → answer with displayed source passages.
Chroma receives vectors explicitly; it does not load a second default embedding model. Insertion uses batches of 16 and one HNSW thread to limit concurrency. These settings are not a verified fix for every Windows native crash.
Frontend and backend are separate Python modules in one Streamlit process, not separate HTTP servers. There is no LangChain, Pinecone, model training or automatic web search.

## Limitations and troubleshooting
- Chroma native insertion previously crashed on your Windows setup. The persistence implementation is tested in the provided Linux environment; it cannot establish that Windows crash is fixed. Run check_chroma.py first. If it passes but real indexing crashes, capture the full terminal log with `-X faulthandler` and test real embeddings separately.
- If a database fails to open, preserve a backup before changing package versions. Do not downgrade Chroma against an existing database without checking migration compatibility.
- Your former in-memory index cannot be recovered after its process exited. Upload those documents once into the new persistent index.
- A first-time model download requires internet access to Hugging Face. The model cache is separate from the Chroma data folder.
- PDFs need selectable text; OCR and Word documents are not included. TXT/MD use UTF-8.
- Keyword coverage is not an ATS score. Required and preferred skills count equally, and negated mentions can match. A detected skill does not prove ability.
- Groq receives resume/JD only when optional feedback is requested. Learning requests send the question, missing-skill names and retrieved passages when enabled. Verify generated answers and citations; retrieval similarity is not confidence. Model availability, API limits and costs depend on your account.
- Keep .env and data/ out of Git. Do not include your database or keys in project submissions.

## Verification
Run `python -m unittest discover -s tests -v` inside the project environment. Tests use deterministic vectors, not a live model or API key, and include a genuine separate-process persistence check. See VALIDATION.md for what was and was not tested.
