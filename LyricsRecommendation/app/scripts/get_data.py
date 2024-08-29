import pandas as pd
import os

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


