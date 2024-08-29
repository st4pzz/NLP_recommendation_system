import pandas as pd
import os
from sklearn.feature_extraction.text import TfidfVectorizer
import joblib


def remove_stop_words(text):
    file_path = os.path.join(os.path.dirname(__file__), "stop_words.txt")
    with open(file_path, "r") as file:
        stop_words = [line.strip() for line in file]
    words = text.split()  
    return ' '.join([word for word in words if word not in stop_words])

def get_clean_dataset():
    dataset_path = os.path.join(os.path.dirname(__file__), '..', 'dataset', 'scraped_lyrics.csv')
    data = pd.read_csv(dataset_path)
    data = data.drop_duplicates(subset="Lyrics", keep="first")
    data['Lyrics'] = data['Lyrics'].str.replace(r'[\r\n]+', ' ', regex=True).str.lower()
    return data

def get_clean_query(query):
    query = query.lower()
    query = remove_stop_words(query)
    return query



DATA = get_clean_dataset()
data_clean = DATA.copy()
data_clean["Lyrics"] = data_clean["Lyrics"].apply(lambda x: remove_stop_words(x))
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(data_clean["Lyrics"])
model_path = os.path.join(os.path.dirname(__file__), '..', 'model', 'tfidf_model.pkl')
joblib.dump((vectorizer, X), model_path)