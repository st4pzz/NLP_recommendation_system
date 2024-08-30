# Music Recommendation System by Lyrics

## Overview
This project is a music recommendation system based on lyrics. The core idea is to use the lyrical content of songs to recommend tracks that are similar in terms of keywords. This type of recommendation can be particularly useful for users who want to discover new music based on lyrical content.

## Why This Topic is Relevant
Lyrics-based recommendations offer a unique and distinctive approach compared to traditional systems, which typically rely on listening data, such as genre preferences or artist popularity. A song's lyrics are an artistic expression that can convey emotions, tell stories, and capture the essence of a culture. Exploring recommendations based on lyrical content allows users to discover songs that have emotional impact and resonate with their feelings or personal experiences. Additionally, this type of system can help highlight lesser-known songs that may not be popular but have powerful and meaningful lyrics.

## How the Web Scraping Was Done
The web scraping for this project was implemented using Python, utilizing the requests library to make HTTP requests and BeautifulSoup to parse HTML content. The primary goal was to collect a comprehensive dataset of song lyrics from various artists on the ```www.lyrics.com``` website, ensuring a broad coverage of different genres and musical styles. The script was carefully designed to scrape data efficiently while adhering to the website's structure and minimizing the load on its servers. The script file is in the following directory: ```/scripts/web_scrapping.py```.

## Scraping Process Overview
- Initialization: The script begins by defining necessary headers to simulate a browser request and avoid potential blocks by the website. A list of uppercase letters from 'A' to 'Z' is used to navigate through different sections of artists on Lyrics.com, and a dictionary tracks the number of tracks scraped per letter.

- Artist Collection: For each letter, the script navigates to the corresponding page that lists all artists whose names start with that letter. The page is fetched using a GET request, and the content is parsed with BeautifulSoup. The script checks if the page contains any artist entries; if not, it moves on to the next letter.

- Filtering Artists: The script identifies artists with a substantial number of songs by checking the second ```<td>``` element in each row of the table containing the artist list. Only artists with more than 100 songs are selected for further scraping. This filtering ensures that only artists with a rich catalog are considered, improving the quality and quantity of the collected data.

- Album Collection: For each selected artist, the script accesses their dedicated page to retrieve a list of albums. The artist's page is parsed to find all album entries. For each album, the script navigates to the album's page to extract the list of songs.

- Lyrics Collection: On the album page, the script iterates through the songs, extracting the song names and their URLs. For each song, it navigates to the song's page to fetch the lyrics. The lyrics are located within a ```<pre>``` tag. The script processes the content to remove unwanted elements, such as links or additional formatting, ensuring clean text extraction.

- Data Storage: The extracted lyrics, along with the song names, are stored in a Python dictionary and appended to a list. This list is subsequently converted into a Pandas DataFrame and saved as a CSV file ```/dataset/scraped_lyrics.csv```. This structured storage format facilitates further analysis and use in the recommendation system.

- Rate Limiting and Error Handling: To comply with web scraping best practices, the script includes a delay ```time.sleep(2)```between requests to reduce server load and avoid being blocked. Additionally, comprehensive error handling is implemented to manage potential issues during scraping, such as network errors or unexpected HTML structures.

- Scraping Constraints
Maximum Songs per Artist: The script limits the number of songs scraped per artist to a maximum of 50. This constraint helps to diversify the dataset by including more artists rather than focusing heavily on a few with extensive discographies.

- Maximum Tracks per Letter: To ensure a balanced dataset, the script also limits the total number of tracks scraped per letter to 1,000. This avoids an overrepresentation of artists from a particular letter and promotes a more comprehensive coverage of the musical landscape.

## How to Install
To install and run the project, follow the steps below:

Clone this repository:


```git clone https://github.com/st4pzz/NLP_recommendation_system.git```

Navigate to the project directory:

```cd LyricsRecommendation```
Install the necessary dependencies:

```pip install -r requirements.txt```

## How to Run
To run the project using Docker, follow these commands:


```docker build -t lyricsrecommendation .```
```docker run -d -p 6969:6969 lyricsrecommendation```
This will create and start a Docker container with the recommendation system, which will be available on port 6969.

## How It Works
The music recommendation system operates by analyzing the lyrical content of songs and identifying those that are most similar to a user-provided query. The system uses a combination of natural language processing (NLP) and machine learning techniques to achieve this. Here's a breakdown of how the system works:

1. User Input and Query Cleaning
When a user makes a request to the /query endpoint of the API, they provide a search query, typically a string of text describing their desired lyrical content. This query is then cleaned, which scripts are in the ```/scripts/get_data.py``` directory, and preprocessed to remove unnecessary words, which are in the ```/app/scripts/stop_words.txt``` file, ensuring more accurate results. This step is crucial as it standardizes the input, making it easier to compare with the lyrics in the database.

2. Dataset Preparation
The system utilizes a dataset of song lyrics that was scraped from Lyrics.com. Before the recommendation process begins, the dataset is also cleaned and preprocessed to ensure consistency and accuracy. This involves removing unnecessary words, the same stop words as the query cleaning, removing the duplicate songs, because some musics have more than 1 artist standardizing the format, and preparing the text for vectorization.

3. Vectorization of Lyrics and Query
The core of the recommendation engine relies on the TF-IDF (Term Frequency-Inverse Document Frequency) vectorization technique. This method converts the textual data (both the lyrics and the user query) into numerical vectors that can be easily compared mathematically.

TF-IDF Vectorization: The system uses the TfidfVectorizer from the scikit-learn library to transform the cleaned lyrics into a TF-IDF matrix (X). Each row in this matrix represents a song’s lyrics as a vector, where each element of the vector represents the importance of a word in the context of all lyrics.

Query Transformation: Similarly, the user’s query is transformed into a TF-IDF vector (Q) using the same vectorizer. This ensures that the query and the lyrics are represented in the same vector space, allowing for direct comparison.

4. Calculating Similarity Scores
To find the most relevant songs based on the user’s query, the system calculates the similarity between the query vector and each song's lyrics vector. This is done using a dot product operation (X @ Q.T), which computes the cosine similarity between the vectors. The result is a similarity score (R) for each song, indicating how closely its lyrics match the query.

5. Ranking and Selecting Top Matches
The system then sorts the songs based on their similarity scores in descending order. The top 10 songs with the highest scores are selected as the most relevant matches to the user's query. This ranking process ensures that the most lyrically similar songs are recommended first.

6. Formatting and Returning Results
For each of the top 10 matches, the system compiles a dictionary containing:

Title: The name of the song.
Content: A preview of the song lyrics, limited to the first 500 words if the lyrics are long. This provides the user with a quick glimpse of the song's content.
Relevance: The calculated similarity score, which indicates how closely the song’s lyrics match the query.
These results are then formatted into a JSON response, which is returned to the user. The response includes the list of recommended songs, each with its title, content preview, and relevance score, making it easy for users to explore and discover new music based on their lyrical preferences.

```py
{
    "results": [
        {
            "title": "Song Title 1",
            "content": "Lyrics of the song truncated after 500 words...",
            "relevance": 0.85
        },
        {
            "title": "Song Title 2",
            "content": "Complete lyrics of a shorter song.",
            "relevance": 0.80
        }
        // more results...
    ],
    "message": "OK"
}
```
 

## Where I Got Data From
The data was obtained through web scraping from the site ```wwww.lyrics.com``` This site was chosen for its comprehensiveness and easy access to a large number of song lyrics from different genres and artists.

## How to Test
To test the system, you can use the URLs provided for each lyric and run queries to check if the system is returning appropriate recommendations. Below are some example URLs used for testing:


- [A test that yields 10 results](http://10.103.0.28:6969/query?query=life%20is%20beautiful)
- [A test that yields more than 1, but less than 10 results because there are not enough relevant documents in the database](http://10.103.0.28:6969/query?query=capitalism)
- [A test that yields something non-obvious](http://10.103.0.28:6969/query?query=songs%20about%20happiness) . ```Why this result is non-obvious ? Because While the song explicitly mentions "happiness" several times, the context in which the word is used is more complex and introspective. The lyrics reflect a struggle with pain, emotional challenges, and a contrast between the difficulty of finding happiness and the desire to share it if found. This creates a juxtaposition where the song isn't directly about pure, straightforward happiness but rather the elusive and often difficult nature of achieving it.```

## Authors 
- Sergio Eduardo Ramella Junior