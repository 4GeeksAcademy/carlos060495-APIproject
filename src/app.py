import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# load the .env file variables
load_dotenv()
client_id = os.environ.get("CLIENT_ID")
client_secret = os.environ.get("CLIENT_SECRET")
auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
spotify = spotipy.Spotify(auth_manager=auth_manager)

url_artista = "https://open.spotify.com/intl-es/artist/3fMbdgg4jU18AjLCKBhRSm"

top_tracks = spotify.artist_top_tracks("3fMbdgg4jU18AjLCKBhRSm")
for track in top_tracks['tracks'][:10]:
    print('track    : ' + track['name'])

df_tracks = pd.json_normalize(top_tracks['tracks'])
df_musica = pd.DataFrame(df_tracks)
df_limpio = df_tracks[[
    'name',
    'popularity',
    'duration_ms',
    'album.name'
]].rename(columns={
    'album.name': 'album'
})
print(df_limpio)

df_limpio_ordenado = df_limpio.sort_values(by='popularity', ascending=True)

top_3_menos_popular = df_limpio_ordenado.head(3)

print(top_3_menos_popular)

plt.figure(figsize=(8, 5))
sns.scatterplot(data=df_limpio, x='duration_ms', y='popularity', s=100, color='teal')

plt.xlabel('Duración (segundos)')
plt.ylabel('Popularidad')
plt.title('¿Influye la duración en la popularidad de una canción?')
plt.grid(True)
plt.show()

# No podemos decir que entre mas corta la cancion mas popular ya que como podemos observar en el grafico no hay una relacion directa, ya que no podemos apreciar una inclinacion de popularidad decreciente hacia las canciones con mas duracion 
