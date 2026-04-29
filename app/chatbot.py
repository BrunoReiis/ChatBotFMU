from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
import pandas as pd
import json
import pathlib
import unicodedata
import re

# Caminhos absolutos baseados no local do arquivo
_BASE_DIR = pathlib.Path(__file__).resolve().parents[1]
_CSV_PATH = _BASE_DIR / 'data' / 'perguntas.csv'
_JSON_PATH = _BASE_DIR / 'data' / 'respostas.json'


def _normalizar(texto: str) -> str:
    """Lowercase + remove acentos + remove pontuação."""
    texto = texto.lower().strip()
    texto = unicodedata.normalize('NFD', texto)
    texto = ''.join(c for c in texto if unicodedata.category(c) != 'Mn')
    texto = re.sub(r'[^\w\s]', ' ', texto)
    return texto


class ChatBot:
    def __init__(self):
        df = pd.read_csv(str(_CSV_PATH))
        df.columns = df.columns.str.strip()
        df['frase'] = df['frase'].str.strip().apply(_normalizar)
        df['categoria'] = df['categoria'].str.strip()

        self.frases = df['frase'].tolist()
        self.categorias = df['categoria'].tolist()

        # Pipeline: TF-IDF + Naive Bayes
        self.pipeline = Pipeline([
            ('tfidf', TfidfVectorizer(ngram_range=(1, 2), min_df=1)),
            ('clf', MultinomialNB(alpha=0.5)),
        ])
        self.pipeline.fit(self.frases, self.categorias)

        with open(str(_JSON_PATH), 'r', encoding='utf-8') as f:
            self.respostas = json.load(f)

    def get_response(self, pergunta: str) -> str:
        if not pergunta or not pergunta.strip():
            return "Por favor, envie uma mensagem."

        pergunta_norm = _normalizar(pergunta)
        categoria = self.pipeline.predict([pergunta_norm])[0]
        probabilidade = max(self.pipeline.predict_proba([pergunta_norm])[0])

        if probabilidade < 0.15:
            return "Não entendi sua pergunta. Posso ajudar com: limite, fatura, pagamento, taxas, desbloqueio ou saldo."

        return self.respostas.get(
            categoria,
            f"Entendi que você perguntou sobre '{categoria}', mas ainda não tenho uma resposta para isso."
        )

    def get_category(self, pergunta: str) -> str:
        """Retorna apenas a categoria prevista para a pergunta."""
        if not pergunta or not pergunta.strip():
            return ''
        return self.pipeline.predict([_normalizar(pergunta)])[0]