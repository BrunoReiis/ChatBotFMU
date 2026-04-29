from flask import Flask, jsonify
import unittest

class ChatBotAppTestCase(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()

    def test_home_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'*** CHATBOT - OPERADORA DE CARTÃO ***', response.data)

    def test_chatbot_response(self):
        response = self.client.post('/chat', json={'message': 'Qual é o limite do meu cartão?'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('resposta', response.json)

if __name__ == '__main__':
    unittest.main()