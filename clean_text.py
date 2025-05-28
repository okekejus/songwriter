# Next up the data needs to be cleaned - removal of the little annotations at the start of each song, as well as the song title. 

import re 
import os 
from tqdm import tqdm
import glob


def clean_text(txt_file, pairs): 
    ''' Accepts dict of patterns and replacement, applies transformation to input (body of text)'''
    for pattern, repl in pairs.items(): 
        try: 
            txt_file = re.sub(pattern, repl, txt_file)   
        except Exception as e: 
            print(f'Error during replacement for {pattern} in {txt_file}')
            pass

    return txt_file

def main(files, pairs): 
    box = []
    for file in tqdm(files, desc='Cleaning + Dumping ...'):
        try: 
            with open(file, 'r', encoding='utf8') as f: 
                cleaned = clean_text(f.read(), pairs=pairs)
                box.append(cleaned)
                f.close()

            with open('data/lyrics/all_lyrics.txt', 'a') as g: 
                g.write(cleaned)
                g.close()
            
            print(f'{file} done.')
        except Exception as e: 
            print(f'Error during processing of {file}')
            print(e)
            pass # skip loop.

if __name__ == '__main__':

    patterns = {r"\[Song \d+: .+": '--next song--',
            r'.+\xa0': '', 
            r'\d+ Contributors.+': '', 
            r'.+ ...Read More.+': '', 
            r'.+ ...Read More.+\s ': '', 
            r'.+ ...Read More\s': '', 
            r'\[Verse \d.+': '', 
            r'Verse-\d': '',
            r'Chorus': '', 
            r'Intro' : '',
            r'Outro' : ''}
    
    files = glob.glob('data/lyrics/*.txt')
   
    path_name = 'data/lyrics/all_lyrics.txt'

    if os.path.exists(path_name): 
        os.remove(path_name)
        open(path_name, 'x')
        main(files, pairs=patterns)
    else: 
        open(path_name, 'x')
        main(files, pairs=patterns)
    




        