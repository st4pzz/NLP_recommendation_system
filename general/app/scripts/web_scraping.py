import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
}

upper_letters_list = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

max_songs_per_artist = 50

tracks_per_letter = {letter: 0 for letter in upper_letters_list}

data = []

max_tracks_per_letter = 1000

for letter in upper_letters_list:
    if tracks_per_letter[letter] >= max_tracks_per_letter:
        continue
    
    while tracks_per_letter[letter] < max_tracks_per_letter:
        url = f"https://www.lyrics.com/artists/{letter}/99999"
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            elements = soup.find_all('tr')

            if not elements:
                break

            for element in elements:
                try:
                    tds = element.find_all('td')
                    
                    if len(tds) >= 3:
                        td_value = tds[1].text.strip()
                        
                        if td_value.isdigit() and int(td_value) > 100:
                            artist_link = tds[0].find('a')
                            if artist_link:
                                artist_url = f"https://www.lyrics.com/{artist_link['href']}"
                                artist_response = requests.get(artist_url, headers=headers)
                                
                                if artist_response.status_code == 200:
                                    artist_soup = BeautifulSoup(artist_response.content, 'html.parser')
                                    songs_scraped = 0  
                                    
                                    tdata_ext = artist_soup.find('div', class_='tdata-ext')
                                    if tdata_ext:
                                        albums = tdata_ext.find_all('div', class_='clearfix')
                                        for album in albums:
                                            album_link = album.find('h3').find('a')
                                            if album_link:
                                                album_url = f"https://www.lyrics.com/{album_link['href']}"
                                                album_response = requests.get(album_url, headers=headers)
                                                
                                                if album_response.status_code == 200:
                                                    album_soup = BeautifulSoup(album_response.content, 'html.parser')
                                                    songs = album_soup.find_all('tr')
                                                    
                                                    for song in songs:
                                                        song_tds = song.find_all('td')
                                                        if len(song_tds) >= 2:
                                                            song_td = song_tds[1].find('div')
                                                            song_link = song_td.find('a')
                                                            
                                                            if song_link:
                                                                song_url = f"https://www.lyrics.com/{song_link['href']}"
                                                                song_name = song_link.text.strip()
                                                                
                                                                song_response = requests.get(song_url, headers=headers)
                                                                if song_response.status_code == 200:
                                                                    song_soup = BeautifulSoup(song_response.content, 'html.parser')
                                                                    pre_tag = song_soup.find('pre')
                                                                    
                                                                    if pre_tag:
                                                                        lyrics = []
                                                                        for element in pre_tag.children:  
                                                                            if isinstance(element, str):
                                                                                lyrics.append(element.strip())
                                                                            elif element.name == 'a':
                                                                                lyrics.append(element.get_text(strip=True))

                                                                        lyrics = ' '.join(lyrics).strip()
                                                                        data.append({
                                                                            'Song Name': song_name,
                                                                            'Lyrics': lyrics
                                                                        })
                                                                        tracks_per_letter[letter] += 1
                                                                        songs_scraped += 1
                                                                        
                                                                        if songs_scraped >= max_songs_per_artist:
                                                                            break  

                                                                        if tracks_per_letter[letter] >= max_tracks_per_letter:
                                                                            break

                                                    if tracks_per_letter[letter] >= max_tracks_per_letter:
                                                        break
                                                    if songs_scraped >= max_songs_per_artist:
                                                        break  

                                            if tracks_per_letter[letter] >= max_tracks_per_letter:
                                                break
                                            if songs_scraped >= max_songs_per_artist:
                                                break 

                except Exception as e:
                    print(f"An error occurred: {e}")

            time.sleep(2)
        else:
            print(f"Failed to access URL {url}. Status Code: {response.status_code}")
            break

    time.sleep(2)

df = pd.DataFrame(data, columns=['Song Name', 'Lyrics'])
df.to_csv("scraped_lyrics.csv", index=False)

