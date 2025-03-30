import json
import pandas as pd
import unicodedata
import sklearn
import nltk
from nltk.corpus import stopwords
from nltk import word_tokenize
from nltk.stem import SnowballStemmer, WordNetLemmatizer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import joblib
import re
nltk.download('punkt')
nltk.download('stopwords')

# corregir caracteres especiales comunes

mapa_reemplazo= {
    "√°": "a",
    "√©": "e",
    "√≠": "i",
    "√≥": "o",
    "√º":"ú",
    "√±": "ñ",
    'Ã¡': 'á',
    'Ã©': 'é',
    'Ã­': 'í',
    'Ã³': 'ó',
    'Ãº': 'ú',
    'Ã±': 'ñ',
    'Ã‘': 'Ñ',
    'Â¡': '¡',
    'Â¿': '¿',
    'Â´': '´',
    'â€œ': '“',
    'â€': '”',
    'â€˜': '‘',
    'â€™': '’',
    'â€¢': '•'
}

data = pd.read_csv("./fake_news.csv", sep=";")

X_train = data[['Descripcion', 'Label']]

# aplica las correcciones definidas en el diccionario

def correct_common_replacements(text):

    for wrong, right in mapa_reemplazo.items():
        text = text.replace(wrong, right)
    return text

# elimina caracteres no ASCII
def remove_non_ascii(words):
    
    new_words = []
    for word in words:
        if word is not None:
          new_word = unicodedata.normalize('NFKD', word).encode('ascii', 'ignore').decode('utf-8', 'ignore')
          new_words.append(new_word)
    return new_words

# convierte las palabras a minúsculas

def to_lowercase(words):

    new_words = []
    for word in words:
        new_word = word.lower()
        new_words.append(new_word)
    return new_words

# elimina signos de puntuación

def remove_punctuation(words):
  
    new_words = []
    for word in words:
        new_word = re.sub(r'[^\w\s]', '', word)
        if new_word != '':
            new_words.append(new_word)
    return new_words

# elimina números enteros
def remove_integers(words):
  
    new_words = []
    for word in words:
        new_word = re.sub(r"\b\d+\b", "", word)
        if new_word != '':
            new_words.append(new_word)
    return new_words

# elimina stopwords
def remove_stopwords(words, stopwords=stopwords.words('spanish')):
    new_words = []
    for word in words:
        if word not in stopwords:
            new_words.append(word)
    return new_words

def preprocessing(words):
    text = ' '.join(words)
    text = correct_common_replacements(text)
    words = text.split()
    words = to_lowercase(words)
    words = remove_punctuation(words)
    words = remove_non_ascii(words)
    words = remove_integers(words)
    words = remove_stopwords(words)
    return words

def stem_words(words):
    """Stem words in list of tokenized words"""
    stemmer = SnowballStemmer('spanish')
    stems = []
    for word in words:
        stem = stemmer.stem(word)
        stems.append(stem)
    return stems

def lemmatize_verbs(words):
    """Lemmatize verbs in list of tokenized words"""
    lemmatizer = WordNetLemmatizer()
    lemmas = []
    for word in words:
        lemma = lemmatizer.lemmatize(word, pos='v')
        lemmas.append(lemma)
    return lemmas

#se definen funciones para reducir las palabras a su raíz

def stem_and_lemmatize(words):
    stems = stem_words(words)
    lemmas = lemmatize_verbs(words)
    return stems + lemmas

def pipeline_datos(df: pd.DataFrame):
    # Realizar una copia del conjunto de datos
    df_pipeline = df.copy()

    # Aplicar el preprocesamiento
    df_pipeline['words'] = df_pipeline['Descripcion'].apply(word_tokenize).apply(preprocessing)
    df_pipeline['words'] = df_pipeline['words'].apply(stem_and_lemmatize)
    df_pipeline['words'] = df_pipeline['words'].apply(lambda x: ' '.join(map(str, x)))

    return df_pipeline['words']

# Crear el pipeline con preprocesamiento y modelo de clasificación
pipeline = Pipeline([
    ('preprocesamiento', FunctionTransformer(pipeline_datos)),
    ('tfidf', TfidfVectorizer(max_features=10000)),
    ('clf', LogisticRegression(C=100, max_iter=100, multi_class='multinomial', solver='newton-cg'))
])

# Entrenar el pipeline con los datos (X_train['Descripcion']) y las etiquetas (X_train['Label'])
pipeline.fit(X_train.drop(columns=['Label']), X_train['Label'])

# Guardar el pipeline entrenado en un archivo
joblib.dump(pipeline, 'pipeline.joblib')