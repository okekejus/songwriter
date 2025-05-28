# Next up the data needs to be cleaned - removal of the little annotations at the start of each song, as well as the song title. 

import re 
import os 
from tqdm import tqdm
import glob

def clean_text(txt_file): 
    txt_file = re.sub(r"\[Song \d+: .+", '--next song--', txt_file)  # need some kind of separator for each song, I like this better 
    txt_file = re.sub(r'.+\xa0', '',txt_file) # pesky space character 
    txt_file = re.sub(r'\d+ Contributors.+', '', txt_file) # removal of the first line of text after song, beginning of annotations.
    txt_file = re.sub(r'.+ ...Read More.+', '', txt_file) # removing the 'Read More' section of the annotations.
    txt_file = re.sub(r'.+ ...Read More.+\s ', '', txt_file)
    txt_file = re.sub(r'.+ ...Read More\s', '', txt_file)
    txt_file = re.sub(r'\[Verse \d.+', '', txt_file) # sometimes these appear, will likely have to do so for Chorus
    txt_file = re.sub(r'Verse-\d', '', txt_file)  
    txt_file = re.sub(r'Chorus', '', txt_file)  
    txt_file = re.sub(r'Intro', '', txt_file)  
    txt_file = re.sub(r'Outro', '', txt_file)  
    return txt_file

def main(): 

    for file in tqdm(files, desc='Cleaning + Dumping ...'):
        try: 
            with open(file, 'r', encoding='utf8') as f: 
                cleaned = clean_text(f.read())
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
    files = glob.glob('data/lyrics/*.txt')
    box = []
    n = open('data/lyrics/all_lyrics.txt', 'x')
    main()
    




        