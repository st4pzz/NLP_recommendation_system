import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# Definir um User-Agent comum de navegador
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
}

# Lista de letras maiúsculas
upper_letters_list = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

max_songs_per_artist = 10

# Dicionário para contar quantas músicas foram coletadas por letra
tracks_per_letter = {letter: 0 for letter in upper_letters_list}

# Lista para armazenar os dados
data = []

# Quantidade máxima de músicas por letra do alfabeto
max_tracks_per_letter = 100

# Loop principal para cada letra do alfabeto
for letter in upper_letters_list:
    
    if tracks_per_letter[letter] >= max_tracks_per_letter:
        continue
    
    page_number = 1
    
    while tracks_per_letter[letter] < max_tracks_per_letter:
        print(f"Coletando músicas com a letra {letter}..., {tracks_per_letter[letter]}/{max_tracks_per_letter} músicas coletadas")
        if page_number == 1:
            url = f"https://www.lyrics.com/artists/{letter}"
        else:
            url = f"https://www.lyrics.com/artists/{letter}/{page_number}"

        # Fazer requisição à URL com o User-Agent
        response = requests.get(url, headers=headers)

        # Verificar se a requisição foi bem-sucedida
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')

            # Encontrar todos os elementos <tr>
            elements = soup.find_all('tr')

            if not elements:
                break

            for element in elements:
                try:
                    # Encontrar todos os elementos <td> dentro do <tr>
                    tds = element.find_all('td')
                    
                    # Verificar se existem pelo menos 3 <td>
                    if len(tds) >= 3:
                        # Verificar se o valor do segundo <td> é maior que 50
                        td_value = tds[1].text.strip()
                        
                        if td_value.isdigit() and int(td_value) > 100:
                            # Redirecionar para a URL no <a> dentro do primeiro <td>
                            artist_link = tds[0].find('a')
                            if artist_link:
                                artist_url = f"https://www.lyrics.com/{artist_link['href']}"
                                
                                # Requisitar a página do artista
                                artist_response = requests.get(artist_url, headers=headers)
                                if artist_response.status_code == 200:
                                    artist_soup = BeautifulSoup(artist_response.content, 'html.parser')
                                    songs_scraped = 0  # Contador de músicas por artista
                                    
                                    # Encontrar todos os álbuns do artista dentro da div com a classe tdata-ext
                                    tdata_ext = artist_soup.find('div', class_='tdata-ext')
                                    if tdata_ext:
                                        albums = tdata_ext.find_all('div', class_='clearfix')
                                        for album in albums:
                                            album_link = album.find('h3').find('a')
                                            if album_link:
                                                album_url = f"https://www.lyrics.com/{album_link['href']}"
                                                
                                                # Requisitar a página do álbum
                                                album_response = requests.get(album_url, headers=headers)
                                                if album_response.status_code == 200:
                                                    album_soup = BeautifulSoup(album_response.content, 'html.parser')
                                                    
                                                    # Encontrar todas as músicas do álbum
                                                    songs = album_soup.find_all('tr')
                                                    for song in songs:
                                                        # Verificar se o <tr> possui pelo menos 2 <td>
                                                        song_tds = song.find_all('td')
                                                        if len(song_tds) >= 2:
                                                            song_td = song_tds[1].find('div')
                                                            song_link = song_td.find('a')
                                                            if song_link:
                                                                song_url = f"https://www.lyrics.com/{song_link['href']}"
                                                                song_name = song_link.text.strip()
                                                                
                                                                # Requisitar a página da música
                                                                song_response = requests.get(song_url, headers=headers)
                                                                if song_response.status_code == 200:
                                                                    song_soup = BeautifulSoup(song_response.content, 'html.parser')
                                                                    
                                                                    # Encontrar o elemento <pre> contendo a letra da música
                                                                    pre_tag = song_soup.find('pre')
                                                                    if pre_tag:
                                                                        
                                                                        
                                                                        # Extrair o texto, incluindo os textos dentro dos links <a>
                                                                        lyrics = []
                                                                        for element in pre_tag.children:  # Usando children em vez de descendants
                                                                            if isinstance(element, str):
                                                                                # Adicionar texto fora de <a> diretamente à lista
                                                                                lyrics.append(element.strip())
                                                                            elif element.name == 'a':
                                                                                # Adicionar texto de dentro de <a> diretamente à lista
                                                                                lyrics.append(element.get_text(strip=True))

                                                                        # Combinar a lista em uma única string com espaços corretos
                                                                        lyrics = ' '.join(lyrics).strip()
                                                                        
                                                                        
                                                                        # Adicionar ao dataset
                                                                        data.append({
                                                                            'Song Name': song_name,
                                                                            'Lyrics': lyrics
                                                                        })
                                                                        
                                                                        
                                                                        # Atualizar contador de músicas por letra
                                                                        tracks_per_letter[letter] += 1

                                                                        songs_scraped += 1
                                                                        
                                                                        
                                                                        if songs_scraped >= max_songs_per_artist:
                                                                            break  # Parar de buscar músicas se o limite for atingido

                                                                        # Verificar se atingiu o máximo de músicas por letra
                                                                        if tracks_per_letter[letter] >= max_tracks_per_letter:
                                                                            break

                                                    # Verificar se atingiu o máximo de músicas por letra
                                                    if tracks_per_letter[letter] >= max_tracks_per_letter:
                                                        break
                                                    if songs_scraped >= max_songs_per_artist:
                                                        break  # Parar de buscar álbuns se o limite for atingido

                                            # Verificar se atingiu o máximo de músicas por letra
                                            if tracks_per_letter[letter] >= max_tracks_per_letter:
                                                break
                                            if songs_scraped >= max_songs_per_artist:
                                                break  # Parar de buscar álbuns se o limite for atingido

                except Exception as e:
                    print(f"Um erro ocorreu: {e}")

            # Pausar entre as páginas para evitar sobrecarga no servidor
            time.sleep(2)
            page_number += 1

        else:
            print(f"Falha ao acessar a URL {url}. Status Code: {response.status_code}")
            break

    # Pausar entre as letras do alfabeto
    time.sleep(2)

# Criar um DataFrame do pandas com os dados coletados
df = pd.DataFrame(data, columns=['Song Name', 'Lyrics'])

# Salvar o DataFrame em um arquivo CSV
df.to_csv("scraped_lyrics.csv", index=False)

print("Dados coletados e salvos em scraped_lyrics.csv")