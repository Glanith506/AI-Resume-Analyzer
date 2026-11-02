import unittest
from io import BytesIO
from unittest.mock import Mock
from backend import extract_skills, compare_skills, calculate_match_percentage, extract_resume_text
from rag import read_document, grounded_answer, KnowledgeBase

class CoreTests(unittest.TestCase):
    def test_word_boundaries_aliases(self):
        found = extract_skills('JavaScript React.js Nodejs PostgreSQL Docker')
        self.assertIn('javascript', found)
        self.assertNotIn('java', found)
        self.assertIn('react', found)
        self.assertIn('node.js', found)
        self.assertIn('postgresql', found)

    def test_match_and_empty_jd(self):
        _, jobs, matching, missing = compare_skills('Python Python SQL', 'Python Docker')
        self.assertEqual(matching, ['python'])
        self.assertEqual(missing, ['docker'])
        self.assertEqual(calculate_match_percentage(matching, jobs), 50)
        self.assertEqual(calculate_match_percentage([], []), 0)

    def test_chunks_keep_source_and_overlap(self):
        text = 'a' * 1800
        chunks = read_document('notes.txt', text.encode())
        self.assertEqual([len(c['text']) for c in chunks], [900, 900, 400])
        self.assertEqual(chunks[0]['text'][-200:], chunks[1]['text'][:200])
        self.assertEqual(chunks[1]['page'], 1)
        self.assertEqual(chunks[1]['source'], 'notes.txt')

    def test_invalid_and_empty_documents(self):
        for name, data in [('empty.txt', b' '), ('file.docx', b'abc'), ('bad.pdf', b'not a pdf')]:
            with self.assertRaises(Exception):
                read_document(name, data)

    def test_no_context_skips_api(self):
        api = Mock()
        answer = grounded_answer('Docker?', [], [], api)
        self.assertIn('could not find', answer)
        api.assert_not_called()

    def test_grounding_prompt_contains_source(self):
        api = Mock(return_value='An image is a template [S1].')
        hit = {'text': 'An image is a template.', 'source': 'notes.md', 'page': 1, 'chunk': 1}
        answer = grounded_answer('What is an image?', [hit], ['docker'], api)
        self.assertIn('[S1]', answer)
        system, user = api.call_args.args
        self.assertIn('untrusted', system)
        self.assertIn('notes.md', user)
        self.assertIn('S1', user)

if __name__ == '__main__':
    unittest.main()
