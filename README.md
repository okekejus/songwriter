# Songwriter 
Song writing is a mystery to me - being able to find the right words that match the right melodies while also telling a story is a respectable skill. Using Deep Learning models and lyrics from established songwriters, I wanted to attempt to create a text generator for songs. 

This is not/will not be used in any commercial capacity, I simply want to find out if I can train a model to make somewhat coherent text. 

## Fetching Training Data 
I repurposed the script from my [lyric analysis](https://github.com/okekejus/lyric-analysis) project, using it to fetch the lyrics of 53 artists. I decided to download 150 songs per artist to begin the training set. 

A function `fetch_lyrics(artist, retries, max_songs)` gathers and saves the lyrics for each artist in the list, using the `lyricsgenius` library. I delayed this function using `dask.delayed`, which sped up its run time from over an hour to 21 minutes. The full code is available in lyric_retrieval.py.


## Data Cleaning
The retrieved lyrics were already relatively clean thanks to the `lyricsgenius` library. Each song came with a header (Song 1, Song 2, etc.), as well as a truncated version of the song's description, taken from the Genius webpage. These are not needed in the model, so I created the function `clean_text(text)` to take care of all unwanted labellings/headers. The result is one text file with 150 songs per artist, each song separated by a "--next song--" marker. 

## Data Preprocessing
- figure out how to train model using both structured lyrics + vocab from other places so it is not just limited to the songs. 