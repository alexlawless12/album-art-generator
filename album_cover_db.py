# imports
# /Applications/anaconda3/envs/myenv/bin/python3 album_cover_db.py
import pandas as pd
import os
import requests
from io import BytesIO
from PIL import Image

# function to get first genre
def get_genre(genre_list):
    genre_string = str(genre_list)
    genre_split = genre_string.split(",")
    return genre_split[0]

# function to download and save image 
def download_and_save_image(url, filename):
    got = requests.get(url)
    img = Image.open(BytesIO(got.content))
    img.save(filename)

def label_image(index, row, output_folder):
    genre = row['genre'].replace(' ', '').lower()
    filename = os.path.join(output_folder, genre + '_' + str(index) + '.jpeg')
    return filename

if __name__ == "__main__":
    
    # Load the CSV file into a DataFrame
    file_path = 'union_df.csv'
    df = pd.read_csv(file_path)

    # Handle missing values
    df = df.dropna(subset=['genres', 'cover'])

    # Alter the genres column to change to list for later alteration
    new_genre_column = df['genres'].apply(get_genre)

    # new_df has columns [id, genre, cover]
    new_df = pd.DataFrame()
    new_df['id'] = df['id']
    new_df['genre'] = new_genre_column
    new_df['cover'] = df['cover']
    
    print('done editing union_df.csv')

    # Set output folder path
    output_folder = './album_covers'
    os.makedirs(output_folder, exist_ok=True)

    # Download images to folder
    for index, row in new_df.iterrows():
        if index % 100 == 0:
            print('dowloading image number ' + str(index))
        filename = label_image(index, row, output_folder)
        if not os.path.exists(filename):
            download_and_save_image(row['cover'], filename)

    print('Done downloading images to ' + output_folder)