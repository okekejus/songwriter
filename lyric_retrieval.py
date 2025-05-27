from lyricsgenius import Genius
import pandas as pd
import os 
import requests
import time
from dask.delayed import delayed 
import dask
from dask.diagnostics.progress import ProgressBar
import errno

api_token = os.getenv("GENIUS_ACCESS_TOKEN")
artists = pd.read_csv("artist_list.csv", encoding='latin-1')

genius = Genius(api_token,
                   skip_non_songs=True, 
                   excluded_terms=["(Remix)", "(Live)"], 
                   remove_section_headers=True, 
                   retries=2,
                   timeout=10)

genius.verbose = False


@delayed 
def fetch_lyrics(artist, retries=3, max_songs=50): 
    while retries > 0:
        try: 
            lyrics = genius.search_artist(artist, max_songs=max_songs, get_full_info=False)
            if lyrics: 
                lyrics.save_lyrics(f'{artist}_Lyrics', extension='txt', verbose=False)
                return f'Lyrics retrieved for {artist}'
            
            else: 
                return f"No Lyrics retrieved for {artist}"
        except requests.exceptions.RequestException as e: 
            print(f'{e.errno} during retrieval for {artist}.') # error number 
            print(f'Message: {e.args[1]}') # Error Message

            if e.args[1].startswith('5'): 
                slp = 3
                print(f'Retrying for {artist} lyrics. Attempt {retries}')
                time.sleep(slp**2)
                lyrics = genius.search_artist(artist, max_songs = max_songs, get_full_info=False)
                lyrics.save_lyrics(f'{artist}_Lyrics', extension='txt', verbose=False)
                retries = retries-1

            elif errno.ETIMEDOUT: 
                print(f'Timeout during retrieval for {artist}')
                time.sleep(3)
                retries = retries-1
                pass
            else: 
                retries = retries-1
                pass
    return f'Max tries for {artist} reached.'
    
def main(): 
    delayed_results = []

    for artist in artists['artist_name']: 
        observed = fetch_lyrics(artist, retries=5, max_songs=150)
        delayed_results.append(observed)

    pbar = ProgressBar()
    pbar.register()
    results = dask.compute(*delayed_results)

if __name__=='__main__':
    main()
