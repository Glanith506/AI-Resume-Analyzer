"""Run native Chroma checks in subprocesses, without MiniLM or an API key."""
import faulthandler
from pathlib import Path
import subprocess
import sys
import tempfile


def worker(path, mode):
    faulthandler.enable()
    import chromadb
    from rag import KnowledgeBase
    print('Python:', sys.version, flush=True)
    print('ChromaDB:', chromadb.__version__, flush=True)
    kb = KnowledgeBase(path=path)
    if mode == 'write':
        print('Adding 120 sample vectors in small batches...', flush=True)
        for start in range(0, 120, 16):
            indexes = list(range(start, min(start + 16, 120)))
            kb.collection.upsert(
                ids=[str(i) for i in indexes], embeddings=[[1.,0.,0.] for i in indexes],
                documents=[f'Docker sample {i}' for i in indexes],
                metadatas=[{'source':'demo','page':1,'chunk':i+1,'document_id':'demo'} for i in indexes],
            )
    assert kb.count() == 120
    print('Querying saved vectors...', flush=True)
    hits = kb.collection.query(query_embeddings=[[1.,0.,0.]], n_results=1)
    assert len(hits['ids'][0]) == 1
    print(mode.upper() + '_OK', flush=True)


if __name__ == '__main__':
    if len(sys.argv) == 3:
        worker(sys.argv[1], sys.argv[2])
    else:
        with tempfile.TemporaryDirectory(prefix='resumelens-chroma-check-') as folder:
            for mode in ('write', 'reopen'):
                result = subprocess.run([sys.executable, '-X', 'faulthandler', str(Path(__file__).resolve()),
                                         str(Path(folder)/'db'), mode])
                if result.returncode:
                    print(f'FAIL during {mode}: exit code {result.returncode}. Save this terminal output.', flush=True)
                    sys.exit(1)
            print('PASS: Chroma insertion, query and cross-process reopening. Real model embeddings still need testing.')
