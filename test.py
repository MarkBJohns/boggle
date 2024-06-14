import unittest
from app import app, boggle_game
from flask import session
from boggle import Boggle


class FlaskTests(unittest.TestCase):

    def setUp(self):
        '''Set up a test client'''
        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'testkey'
        self.client = app.test_client()
        self.client.testing = True
        
    def test_home_page(self): 
        '''Test the home page route'''
        with self.client as client:
            response = client.get('/')
            self.assertEqual(response.status_code, 200)
            response_data = response.data.decode('utf-8')
            self.assertIn('Boggle Assignment', response_data)
            self.assertIn('High Score', response_data)
            self.assertIn('Score:', response_data)
            self.assertIn('Time', response_data)
            self.assertIn('board', session)

            
    def test_check_guess(self):
        '''Test the check-guess route'''
        with self.client as client:
            with client.session_transaction() as session:
                session['board'] = boggle_game.make_board()
                
            response = client.get('/check-guess', query_string={'word':'test'})
            self.assertEqual(response.status_code, 200)
            self.assertIn('result', response.data.decode('utf-8'))
            
    def test_post_score(self):
        '''Test the post-score route'''
        with self.client as client:
            with client.session_transaction() as session:
                session['highscore'] = 10
                session['nplays'] = 5
                
            response = client.post('/post-score', json={'score': 20})
            self.assertEqual(response.status_code, 200)
            data = response.get_json()
            self.assertTrue(data['brokeRecord'])
            
            with client.session_transaction() as session:
                self.assertEqual(session['highscore'], 20)
                self.assertEqual(session['nplays'], 6)
                
class BoggleTestClass(unittest.TestCase):
    def setUp(self):
        '''Set up a Boggle instance for testing'''
        self.boggle_game = Boggle()
        
    def test_make_board(self):
        '''Test that the board is created correctly'''
        board = self.boggle_game.make_board()
        self.assertEqual(len(board), 5)
        for row in board:
            self.assertEqual(len(row), 5)
        
    def test_valid_word_in_dict_and_on_board(self):
        '''Test if a valid word is correctly identified'''
        board = [
            ['C', 'A', 'T', 'S', 'R'],
            ['R', 'A', 'T', 'S', 'R'],
            ['A', 'T', 'S', 'R', 'C'],
            ['T', 'S', 'R', 'C', 'A'],
            ['S', 'R', 'C', 'A', 'T']
        ]
        self.boggle_game.words = ['CATS', 'CAR', 'STAR', 'RAT', 'ART']
        self.assertEqual(self.boggle_game.check_valid_word(board, 'CATS'), 'ok')
        self.assertEqual(self.boggle_game.check_valid_word(board, 'CAR'), 'ok')

    def test_valid_word_not_in_dict(self): # FAILED
        '''Tests for valid words that aren't in the dictionary'''
        board = [
            ['C', 'A', 'T', 'S', 'R'],
            ['R', 'A', 'T', 'S', 'R'],
            ['A', 'T', 'S', 'R', 'C'],
            ['T', 'S', 'R', 'C', 'A'],
            ['S', 'R', 'C', 'A', 'T']
        ]
        self.boggle_game.words = ['DOG']
        self.assertEqual(self.boggle_game.check_valid_word(board, 'DOG'), 'not-on-board')
        
    def test_find_word_on_board(self):
        '''Tests that a word can be found if in the board'''
        board = [
            ['C', 'A', 'T', 'S', 'R'],
            ['R', 'A', 'T', 'S', 'R'],
            ['A', 'T', 'S', 'R', 'C'],
            ['T', 'S', 'R', 'C', 'A'],
            ['S', 'R', 'C', 'A', 'T']
        ]
        self.assertTrue(self.boggle_game.find(board, 'CATS'))
        self.assertFalse(self.boggle_game.find(board, 'DOG'))
    
if __name__ == '__main__':
    unittest.main()