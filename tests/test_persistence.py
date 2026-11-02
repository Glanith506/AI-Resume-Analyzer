import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

import numpy as np
from rag import KnowledgeBase, read_document

class Encoder:
    def __init__(self):
        self.calls = 0

    def encode(self, texts, **kwargs):
        self.calls += len(texts)
        return np.array([[1., 0., 0.] if 'docker' in t.lower() else [0., 1., 0.] for t in texts])

class PersistenceTests(unittest.TestCase):
    def setUp(self):
        self.folder = tempfile.mkdtemp(prefix='resumelens-test-')
        self.encoder = Encoder()
        self.kb = KnowledgeBase(encoder=self.encoder, path=self.folder)

    def test_empty_search_does_not_load_model(self):
        self.assertEqual(self.kb.search('Docker'), [])
        self.assertEqual(self.encoder.calls, 0)

    def test_duplicate_renamed_upload_skips_embeddings(self):
        first = self.kb.add_chunks(read_document('notes.txt', b'Docker containers'))
        second = self.kb.add_chunks(read_document('renamed.txt', b'Docker containers'))
        self.assertEqual(first, {'added':1, 'skipped':0})
        self.assertEqual(second, {'added':0, 'skipped':1})
        self.assertEqual(self.encoder.calls, 1)
        self.assertEqual(self.kb.count(), 1)

    def test_reopen_and_close_preserve_data(self):
        self.kb.add_chunks(read_document('docker.txt', b'Docker containers'))
        self.kb.close()
        reopened = KnowledgeBase(encoder=self.encoder, path=self.folder)
        self.assertEqual(reopened.count(), 1)
        self.assertEqual(reopened.search('Docker')[0]['source'], 'docker.txt')

    def test_changed_file_and_document_removal(self):
        old = read_document('same.txt', b'Docker old')
        new = read_document('same.txt', b'SQL new')
        self.kb.add_chunks(old + new)
        self.assertEqual(len(self.kb.documents()), 2)
        self.kb.delete_document(old[0]['document_id'])
        self.assertEqual(self.kb.count(), 1)
        self.assertEqual(self.kb.search('Docker'), [])
        self.assertEqual(self.kb.search('SQL')[0]['text'], 'SQL new')

    def test_explicit_clear_and_reuse(self):
        self.kb.add_chunks(read_document('a.txt', b'Docker'))
        self.kb.clear()
        self.assertEqual(self.kb.count(), 0)
        self.kb.add_chunks(read_document('b.txt', b'SQL'))
        self.assertEqual(self.kb.count(), 1)

    def test_independent_database_folders(self):
        self.kb.add_chunks(read_document('a.txt', b'Docker'))
        other = KnowledgeBase(encoder=self.encoder, path=str(Path(self.folder)/'other'))
        self.assertEqual(other.count(), 0)

    def test_multiple_batches_and_hnsw_flush(self):
        chunks = [{'source':'long.txt', 'page':1, 'chunk':i+1,
                   'text':f'Docker passage {i}', 'document_id':'one-document'} for i in range(120)]
        self.assertEqual(self.kb.add_chunks(chunks)['added'], 120)
        self.assertEqual(self.kb.count(), 120)
        self.assertEqual(len(self.kb.search('Docker')), 4)
        self.assertEqual(self.kb.add_chunks(chunks)['skipped'], 120)

    def test_invalid_vectors_do_not_write(self):
        class Bad:
            def encode(self, texts, **kwargs):
                return [[float('nan'), 0.]] * len(texts)
        self.kb.encoder = Bad()
        with self.assertRaises(ValueError):
            self.kb.add_chunks(read_document('bad.txt', b'Docker'))
        self.assertEqual(self.kb.count(), 0)

    def test_persistence_across_separate_processes(self):
        # No shared Python objects: first process exits, second reads and queries.
        path = str(Path(self.folder)/'restart-db')
        write = """
from rag import KnowledgeBase, read_document
import numpy as np
class E:
 def encode(self, texts, **kwargs): return np.array([[1., 0.]] * len(texts))
k = KnowledgeBase(encoder=E(), path=__import__('sys').argv[1])
k.add_chunks(read_document('restart.txt', b'Docker persists across restarts'))
"""
        read = """
from rag import KnowledgeBase
import numpy as np
class E:
 def encode(self, texts, **kwargs): return np.array([[1., 0.]] * len(texts))
k = KnowledgeBase(encoder=E(), path=__import__('sys').argv[1])
assert k.count() == 1
assert k.search('Docker')[0]['source'] == 'restart.txt'
print('RESTART_OK')
"""
        subprocess.run([sys.executable, '-c', write, path], check=True, capture_output=True, timeout=60)
        result = subprocess.run([sys.executable, '-c', read, path], check=True, capture_output=True, text=True, timeout=60)
        self.assertIn('RESTART_OK', result.stdout)

if __name__ == '__main__':
    unittest.main()
