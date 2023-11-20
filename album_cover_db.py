# imports
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

def label_image(index, row):
    genre = row['genre'].replace(' ', '').lower()
    filename = os.path.join(output_folder, f"{genre}_{index}.jpeg")
    return filename

if __name__ == "__main__":
    
    print('this is supposed to be a test about branches')
    
    # Load the CSV file into a DataFrame
    file_path = 'union_df.csv'
    df = pd.read_csv(file_path)
    
    # Alter the genres column to change to list for later alteration
    new_genre_column = df['genres'].apply(get_genre)
    
    # new_df has columns [id, genre, cover]
    new_df = pd.DataFrame()
    new_df['id'] = df['id']
    new_df['genre'] = new_genre_column
    new_df['cover'] = df['cover']
    
    # Set output folder path in colab
    output_folder = '~/Downloads/album_covers'
    os.makedirs(output_folder, exist_ok=True)
    
    # dowload images to folder
    for index, row in new_df.iterrows():
        filename = lable_image(index, row)
        download_and_save_image(row['cover'], filename)
    print('done downloading images to' + output_folder)

