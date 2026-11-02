# What to keep and what to replace
Keep your local .env (Groq key), .venv (working torch), and data folder.
Replace frontend.py and rag.py together. Copy check_chroma.py and the updated requirements/documentation.
If you tried the NumPy replacement, the new rag.py restores ChromaDB. The old EphemeralClient index cannot be transferred after its process has exited.

Run the Windows commands in README.md, starting with check_chroma.py. Then add documents once.
After restart, saved documents should appear before an embedding model loads. You can immediately ask questions about them; the model loads to embed the question.
Changing the upload selection does not remove saved documents. Manage saved documents provides explicit removal and clear controls.

Persistence addresses index loss on restart. It is separate from the unresolved native Windows insertion failure. Small batches and one indexing thread are used, but Windows must be checked locally.
