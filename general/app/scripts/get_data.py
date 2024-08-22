import pandas as pd


def remove_stop_words(text):
    with open("stop_words.txt", "r") as file:
        stop_words = [line.strip() for line in file]
    words = text.split()  
    return ' '.join([word for word in words if word not in stop_words])

def get_clean_dataset():
    data = pd.read_csv("scraped_lyrics.csv")
    data = data.drop_duplicates(subset="Song Name", keep="first")
    data['Lyrics'] = data['Lyrics'].str.replace(r'[\r\n]+', ' ', regex=True).str.lower()
    data["Lyrics"] = data['Lyrics'].apply(lambda x: remove_stop_words(x))
    return data

def get_clean_query(query):
    query = query.lower()
    query = remove_stop_words(query)
    return query


