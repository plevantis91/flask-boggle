from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle


# test.py

import unittest
from app import app

class FlaskTests(unittest.TestCase):
    
    def setUp(self):
        """Stuff to do before every test."""
        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_homepage(self):
        """Test homepage route."""
        res = self.client.get('/')
        html = res.get_data(as_text=True)
        self.assertEqual(res.status_code, 200)
        self.assertIn('<table id="board">', html)

    def test_check_word_valid(self):
        """Test check_word route with valid word."""
        with self.client as client:
            with client.session_transaction() as sess:
                sess['board'] = [['A', 'B', 'C', 'D', 'E'],
                                 ['F', 'G', 'H', 'I', 'J'],
                                 ['K', 'L', 'M', 'N', 'O'],
                                 ['P', 'Q', 'R', 'S', 'T'],
                                 ['U', 'V', 'W', 'X', 'Y']]
        res = self.client.get('/check-word?word=DOG')
        self.assertEqual(res.json['result'], 'ok')

    def test_check_word_invalid(self):
        """Test check_word route with invalid word."""
        with self.client as client:
            with client.session_transaction() as sess:
                sess['board'] = [['A', 'B', 'C', 'D', 'E'],
                                 ['F', 'G', 'H', 'I', 'J'],
                                 ['K', 'L', 'M', 'N', 'O'],
                                 ['P', 'Q', 'R', 'S', 'T'],
                                 ['U', 'V', 'W', 'X', 'Y']]
        res = self.client.get('/check-word?word=APPLE')
        self.assertEqual(res.json['result'], 'not-on-board')

    def test_post_score(self):
        """Test post_score route."""
        res = self.client.post('/post-score', json={"score": 10})
        self.assertEqual(res.json['brokeRecord'], False)


