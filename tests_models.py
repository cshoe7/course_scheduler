import unittest
from CS_code.models import user
from CS_code.models import course
from CS_code.models import schedule
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma

import os


class TestUserMethods(unittest.TestCase):

    def setUp(self):
        """Create user before each test"""
        self.user = user("Claire", 2028, ["Music", "Soccer"], ["Mathematics", "Computer Science"])

    def test_get_gradyear(self):
        self.assertEqual(self.user.get_gradyear(), 2028)

    def test_get_interets(self):
        self.assertEqual(self.user.get_interests(), ["Music", "Soccer"])
    
    def test_get_majors(self):
        self.assertEqual(self.user.get_majors(), ["Mathemetics", "Computer Science"])

    def test_set_interests(self):
        self.user.set_interests(["Dance", "Soccer"])
        self.assertEqual(self.user.get_interets(), ["Dance", "Soccer"])

    def test_set_majors(self):
        self.user.set_majors(["Psychology"])
        self.assertEqual(self.user.get_majors(), ["Psychology"])

    def test_set_invalid_interests(self):
        with self.assertRaises(ValueError):
            self.user.set_interests(12345)
    
    def set_invalid_majors(self):
        with self.assertRaises(ValueError):
            self.user.set_majors(6789)

class TestCourseMethods(unittest.TestCase):

    def setup(self):
        """Create course before each test"""
        self.course = course("Differential Equations", "A", "Dr. T", "This is a mock course description")
    
    def test_get_name(self):
        self.assertEqual(self.user.couse.get_name(), "Differential Equations")
    
    def test_get_section(self):
        self.assertEqual(self.user.course.get_section(), "A")

    def test_get_prof(self):
        self.assertEqual(self.user.course.get_prof(), "Dr. T")
    
    def test_get_description(self):
        self.assertEqual(self.user.course.get_description(), "This is a mock course description")
    

class TestScheduleMethods(unittest.TestCase):

    def setup(self):
        """Create course before each test"""
        self.schedule = schedule([[course("CIE-100", "A", "teach1", "mock1"), 
        course("Spanish-101", "B", "teach2", "mock2"), course("Math-210", "B", "teach3", "mock3"), 
        course("CS-101", "A", "teach4", "mock4")]])

    def test_get_schedule(self):
        self.assertEqual(self.schedule.get_schedule(), [[course("CIE-100", "A", "teach1", "mock1"), 
        course("Spanish-101", "B", "teach2", "mock2"), course("Math-210", "B", "teach3", "mock3"), 
        course("CS-101", "A", "teach4", "mock4")]])

"""
DISCLAIMER:

All of the following tests elements of the RAG pipeline. I had to do research on syntax
and what everything means, so it may not be all inclusive. I just wanted to make sure we included some elements of testing for the actual AI pipeline.
"""

class TestDocumentChunker(unittest.TestCase):

    def setUp(self):
        self.chunker = RecursiveCharacterTextSplitter(chunk_size = 1000, chunk_overlap = 200)
    
    def test_chunks_long_text_into_multiple_pieces(self):
        text = "a" * 1200
        chunks = self.chunker.split_documents(text)
        self.assertGreater(len(chunks), 1)
    
    def test_short_text_produces_single_chunk(self):
        text = "Short course description."
        chunks = self.chunker.split_documents(text)
        self.assertEqual(len(chunks), 1) 

    def test_empty_string_returns_empty_list(self):
        chunks = self.chunker.split_documents("")
        self.assertEqual(chunks, [])

    def test_overlap_means_chunks_share_content(self):
        text = "a" * 1000
        chunks = self.chunker.split_documents(text)
        if len(chunks) > 1:
            end_of_first = chunks[0]["end"]
            start_of_second = chunks[1]["start"]
            self.assertLess(start_of_second, end_of_first)
    

class TestEmbeddingModel(unittest.TestCase):

    def setUp(self):
        self.model = OllamaEmbeddings(
            model="qwen3-embedding",  
            base_url="https://ollama.com",
            headers={"Authorization": "Bearer " + os.environ["OLLAMA_API_KEY"]}
        )

    def test_embed_consistent_for_same_input(self):
        text = "Spanish-100"
        emb1 = self.model.embed_query(text)
        emb2 = self.model.embed_query(text)
        self.assertEqual(emb1, emb2)

    def test_embed_batch_returns_one_vector_per_text(self):
        texts = ["CS101", "CS301", "ML401"]
        embeddings = self.model.embed_documents(texts)
        self.assertEqual(len(embeddings), len(texts))

    def test_embed_raises_on_empty_string(self):
        with self.assertRaises(ValueError):
            self.model.embed_query("")

    def test_embed_raises_on_none(self):
        with self.assertRaises(TypeError):
                self.model.embed_query(None)

