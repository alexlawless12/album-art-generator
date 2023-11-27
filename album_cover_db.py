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
    return genre_split[0].replace(' ', '').lower()

# function to download and save image 
def download_and_save_image(url, filename):
    got = requests.get(url)
    img = Image.open(BytesIO(got.content))
    img.save(filename)

def label_image(row, output_folder):
    genre = row['genre']
    filename = os.path.join(output_folder, genre + '_' + str(row['id']) + '.jpeg')
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
    new_df['genre'] = new_genre_column
    new_df['cover'] = df['cover']
    new_df['spotify_tag'] = df['id'] # id to refrence back to union_df.csv if needed
    
    # drop cover repeats
    new_df.drop_duplicates(subset=['cover'], inplace=True)
    
    # add readable integer id
    new_df['id'] = range(0, len(new_df))
    print('     new_df now ', len(new_df))
    
    print('done editing union_df.csv, now group genres')
    
    # Mapping of genres to buckets
    genre_buckets = {
        'rock': ['alternativerock', 'rock', 'classicrock', 'newwave', 'permenantwave', 'adultstandards', 'modernrock', 'albumrock', 'emo', 'altz', 'hardrock', 'punkrock', 'poprock', 'neomellow', 'psychedelicrock', 'softrock', 'bluesrock', 'rootsrock', 'stompandholler', 'heartlandrock', 'glamrock', 'sleazerock', 'rockandroll', 'dancerock', 'britishinvasion', 'grunge', 'acidrock', 'pianorock', 'garagerock', 'freakbeat', 'merseybeat', 'rockenespanol', 'mpb', 'rockquebecois', 'rockbaiano', 'eggpunk', 'trashrock', 'rocknacional', 'rockabilly', 'rockabillyenespanol', 'novacanco', 'swissalternativerock', 'flamencofusion', 'italianpoprock', 'rhythmrock', 'grunge pop', 'grungerevival', 'newzealandrock', 'countryrock'],
        'pop': ['pop', 'dancepop', 'electropop', 'indiepop', 'newwavepop', 'bubblegumpop', 'sophistipop', 'brillbuildingpop', 'teenpop', 'europop', 'lapop', 'popelectronico', 'poprap', 'popworship', 'poppunk', 'popsoul', 'classicukpop', 'popr&b', 'popemo', 'ccm', 'popreggaeton', 'poplgbtq+brasileira'],
        'metal': ['metal', 'numetal', 'alternativemetal', 'powermetal', 'epicore', 'glammetal', 'deathmetal', 'melodicmetal', 'speedmetal', 'thrashmetal', 'oldschoolthrashmetal', 'neoclassicalmetal', 'paganmetal', 'vikingmetal', 'tolkienmetal', 'technicaldeathmetal', 'brutaldeathmetal', 'groovemetal', 'nümetal', 'metalcore', 'melodicdeathmetal', 'doommetal', 'gothicmetal', 'industialmetal', 'djent', 'folkmetal', 'avantgardemetal', 'symphonicmetal', 'progressivemetal', 'sludgemetal', 'stonermetal', 'dronemetal', 'postmetal', 'atmosphericblackmetal', 'blackmetal', 'depressiveblackmetal'],
        'hiphop': ['hiphop', 'rap', 'poprap', 'undergroundhiphop', 'southernhiphop', 'trap', 'melodicrap', 'raprock', 'rapmetal', 'oldschoolhiphop', 'hardorehiphop', 'gangsterrap', 'rapconscient', 'abstracthiphop', 'boom bap', 'jazzrap', 'eastcoasthiphop', 'westcoasthiphop', 'dirtysouthrap', 'choppedandscewed', 'memphishiphop', 'neworleansbounce', 'hyphy', 'crunk', 'phonk', 'cloudrap', 'soundcloudrap', 'mumblerap', 'afropop', 'hiplife', 'gengetone', 'asanteakanhighlife', 'ghanaianhiplife', 'hippop', 'hawaiianhiphop', 'melodicrap'],
        'electronic': ['electronic','tronica','indieelectropop','edm', 'chillstep', 'electronica', 'electro', 'electroclash', 'electropop', 'electropowerpop', 'indietronica', 'electronicrock', 'electronic', 'house', 'techno', 'trance', 'hardstyle', 'hardcore', 'jungle', 'drumandbass', 'dubstep', 'brostep', 'glitchhop', 'industrial', 'darkelectro', 'ebm', 'futurepop', 'synthpop', 'synthwave', 'vaporwave', 'hyperpop', 'artifical', 'breakbeat', 'bigbeat', 'tekno', 'gabber', 'speedcore', 'happyhardcore', 'hardstyle', 'UKhardcore', 'makina', 'techstep', 'darksidejungle', 'darkstep', 'neurofunk', 'techno', 'minimaltechno', 'nrghardcore', 'breakcore', 'rhythmgame', 'videogamemusic', 'chiptune', 'bitpop', 'intelligentdancemusic', 'braindance', 'experimental', 'lofi', 'lo-fi', 'complextro', 'speedrun', 'bigroom'],
        'dance': ['dance', 'dancepop', 'popdance', 'house', 'tropicalhouse', 'floatinghouse', 'shuffle', 'basshouse', 'clubhouse', 'slaphouse', 'groovehouse', 'funkyhouse', 'discohouse', 'psytrance', 'techhouse', 'electrohouse', 'futurehouse', 'bounce', 'crunk', 'bass', 'tribalhouse', 'highenergy', 'eurobeat', 'hyperbeat', 'speedcore', 'speedgarage', '2stepgarage', 'futuregarage', 'garagerock'],
        'funk': ['funk', 'pfunk', 'gogo', 'boogie', 'electrofunk', 'modernfunk'],
        'folk': ['folk', 'indiefolk', 'freakfolk', 'folkrock', 'americana', 'roots', 'blue'],
        'classical': ['classical'],
        'country': ['country', 'countryrock'],
        'r&b': ['r&b', 'soul', 'neosoul', 'quietstorm', 'contemporaryr&b', 'alternativer&b'],
        'indie': ['indie', 'indierock', 'indiepop', 'indiepoptimism', 'indier&b', 'indiefolk', 'indieelectronica', 'singersongwriter'],
        'reggae' : ['reggae'],
    }

    # Default bucket for genres not in any specified bucket
    default_bucket = 'other'

    # Update genre column based on buckets
    new_df['genre_no_bucket'] = new_df['genre']
    new_df['genre'] = new_df['genre'].apply(lambda x: next((bucket for bucket, genres in genre_buckets.items() if any(keyword in x.lower() for keyword in genres)), default_bucket))

    # Print counts of genres in each bucket
    for bucket, genres in genre_buckets.items():
        count = new_df[new_df['genre'].isin(genres)].shape[0]
        print(f'{bucket}: {count}')

    # Count of genres in the default bucket
    count_other = new_df[new_df['genre'] == default_bucket].shape[0]
    print(f'{default_bucket}: {count_other}')

    # Save the updated DataFrame to a new CSV file
    new_df.to_csv('genre_df.csv', index=False)
    print('Done updating genres, saved in genre_df.csv')

    # Set output folder path
    output_folder = './album_covers'
    os.makedirs(output_folder, exist_ok=True)

    # Download images to folder (300 px x 300 px)
    for index, row in new_df.iterrows():
        filename = label_image(row, output_folder)
        print(filename)
        if not os.path.exists(filename):
            download_and_save_image(row['cover'], filename)

    print('Done downloading images to ' + output_folder)