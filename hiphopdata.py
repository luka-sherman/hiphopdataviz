import re
import pandas
from num2words import num2words
from unidecode import unidecode
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# raw files
FILE_BILLBOARD = 'billboard_hot100_all_genres.csv'
FILE_HIPHOP_ARTISTS = 'wiki_hiphop_artists_and_groups.csv'

#created files
FILE_BILLBOARD_ISHIPHOP = 'billboard_hot100_all_genres_ishiphop.csv'
FILE_BILLBOARD_HIPHOP = 'billboard_hiphop.csv'
FILE_BILLBOARD_HIPHOP_SPOTIFY = 'billboard_hiphop_spotify.csv'
FILE_BILLBOARD_HIPHOP_SPOTIFY_COMPLETE = 'billboard_hiphop_spotify_complete.csv'

TRACK_FIELDS = [
    'id',
    'embed',
    'url',
    'isrc',
    # 'ean',
    # 'upc',
    'name',
    'popularity',
    'duration_ms',
    'explicit',
    'number',
    'uri',
]
ARTIST_FIELDS = [
    'url',
    'followers',
    'genres',
    'id',
    'image_url',
    'name',
    'popularity',
]
ALBUM_FIELDS = [
    'name',
    'release_date',
    'total_tracks',
    'image',
    'uri',
    'type',
    'url',
    # 'isrc',
    # 'ean',
    'upc',
    # 'genres',
    'label',
    'popularity',
]
AUDIO_FIELDS = [
    'acousticness', 
    'danceability',
    'energy',
    'instrumentalness',
    'key',
    'liveness',
    'loudness',
    'mode',
    'speechiness',
    'tempo',
    'time_signature',
    'valence',
]

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope="user-library-read"))


def main():

    billboard_filter_hiphop(
        make_file_ishiphop=False, 
        make_file_billboardhiphop=False)
    
    match_billboard_to_spotify_song(
        FILE_BILLBOARD_HIPHOP, 
        FILE_BILLBOARD_HIPHOP_SPOTIFY)
    
    add_spotify_fields(
        FILE_BILLBOARD_HIPHOP_SPOTIFY, 
        FILE_BILLBOARD_HIPHOP_SPOTIFY_COMPLETE, 
        track_fields=TRACK_FIELDS, 
        artist_fields=ARTIST_FIELDS, 
        album_fields=ALBUM_FIELDS, 
        audio_fields=AUDIO_FIELDS)
    
    return


"""


"""
def add_spotify_fields(file_read, file_write, track_fields=[], artist_fields=[], album_fields=[], audio_fields=[]):

    df = pandas.read_csv(file_read)

    # create necessary columns, if don't already exist
    for field in track_fields: 
        if (field not in df): 
            df['spotify_track_'+field] = ''
    
    for field in audio_fields: 
        if (field not in df): 
            df['spotify_track_'+field] = ''
    
    for field in album_fields: 
        if (field not in df): 
            df['spotify_album_'+field] = ''

    for i in range(1, 7):
        for field in artist_fields: 
            if (field not in df): 
                df['spotify_track_artist'+str(i)+'_'+field] = ''

    last_track_uri = ''
    all_artists = {}
    d = None

    try:

        # for each entry in the billboard top 100 
        for i, row in df.iterrows():
            
            if (i % 1000 == 0):
                print("at index: "+str(i))

            # if there is no spotify track info, continue to next row 
            if (pandas.isna(row['spotify_track_id'])):
                continue
            # if there is album id already filled in, 
            # if (pandas.notna(row['spotify_album_id'])):
            #     continue
            
            track_id = row['spotify_track_id']
            album_id = row['spotify_album_id']
            # artist_id = row['spotify_track_id']

            # if has the same content as last row, don't redo search 
            if (track_id != last_track_id): # no redundant call if same as previous song and performer
                sp_track = sp.track(track_id) if len(track_fields>0) else None
                sp_album = sp.album(album_id) if len(album_fields>0) else None
                sp_audio = sp.audio_features(track_id) if len(audio_fields>0) else None

            # if there are search results, iterate through them 

            if (sp_track):
                df.loc[i, 'spotify_track_id'] = track_id
                df.loc[i, 'spotify_track_embed'] = """<iframe style="border-radius:12px" src="https://open.spotify.com/embed/track/"""+track_id+"""?utm_source=generator&theme=0" width="100%" height="152" frameBorder="0" allowfullscreen="" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" loading="lazy"></iframe>"""
                df.loc[i, 'spotify_track_url'] = d.get('external_urls', {}).get('spotify', '')
                df.loc[i, 'spotify_track_isrc'] = d.get('external_ids', {}).get('isrc', '')
                # df.loc[i, 'spotify_track_ean'] = d.get('external_ids', {}).get('ean', '') # removed because never present 
                # df.loc[i, 'spotify_track_upc'] = d.get('external_ids', {}).get('upc', '')# removed because never present 

            if (sp_audio):
                for field in audio_fields: 
                    df['spotify_track_'+field] = sp_audio.get(field)

            if (sp_album):
                df.loc[i, 'spotify_album_id'] = album_id
                df.loc[i, 'spotify_album_type'] = sp_album.get('album_type', '')
                df.loc[i, 'spotify_album_url'] = sp_album.get('external_urls', {}).get('spotify', '')
                # df.loc[i, 'spotify_album_isrc'] = sp_album.get('external_ids', {}).get('isrc', '')
                # df.loc[i, 'spotify_album_ean'] = sp_album.get('external_ids', {}).get('ean', '')
                df.loc[i, 'spotify_album_upc'] = sp_album.get('external_ids', {}).get('upc', '')
                # df.loc[i, 'spotify_album_genres'] = str(sp_album.get('genres', [])) removed because never present
                df.loc[i, 'spotify_album_label'] = sp_album.get('label', '')
                df.loc[i, 'spotify_album_popularity'] = sp_album.get('popularity', '')

            
            if len(artist_fields>0):

                for artist_index in range(1, 7):

                    if (pandas.isna(row['spotify_track_artist'+str(artist_index)+'_id'])):
                        continue
                    
                    artist_id = str(row['spotify_track_artist'+str(artist_index)+'_id'])

                    if all_artists.get(artist_id):
                        sp_artist = all_artists.get(artist_id) 
                    else:
                        sp_artist = sp.artist(artist_id) 
                        all_artists[artist_id] = d                    
                    
                    if (sp_artist):
                        df.loc[i, 'spotify_track_artist'+str(artist_index)+'_url'] = sp_artist.get('external_urls', {}).get('spotify', '')
                        df.loc[i, 'spotify_track_artist'+str(artist_index)+'_followers'] = sp_artist.get('followers', {}).get('total', '')
                        df.loc[i, 'spotify_track_artist'+str(artist_index)+'_genres'] = str(sp_artist.get('genres', []))
                        df.loc[i, 'spotify_track_artist'+str(artist_index)+'_id'] = sp_artist.get('id', '')
                        df.loc[i, 'spotify_track_artist'+str(artist_index)+'_image_url'] = sp_artist.get('images', [])[0].get('url', '') if sp_artist.get('images') else ''
                        df.loc[i, 'spotify_track_artist'+str(artist_index)+'_name'] = sp_artist.get('name', '')
                        df.loc[i, 'spotify_track_artist'+str(artist_index)+'_popularity'] = sp_artist.get('popularity', '')

            last_track_id = track_id

    except spotipy.exceptions.SpotifyException as e:
        df.to_csv(file_write)
        print('ERROR at '+str(i))

    except KeyboardInterrupt as e:
        df.to_csv(file_write)
        print('ABORTED at')
        print(i)

    except ValueError as e:
        df.to_csv(file_write)
        print('ABORTED at')
        print(i)

    df.to_csv(file_write)


"""
 
"""
def match_billboard_to_spotify_song(file_read, file_write):

    prompt = input("prompt if no automatic match found? (y/n) ")

    # df = pandas.read_csv('billboard_hot100_hiphop.csv')
    df = pandas.read_csv(file_read)

    last = ''
    d = None

    try:

        # for each entry in the billboard top 100 
        for index, row in df.iterrows():
            
            if (index % 1000 == 0):
                print("at index: "+str(index))

            match = False

            bb_song = row['billboard_song']
            bb_performer = row['billboard_performer']
            # print(row['spotify_track_name'])

            # if there is already a spotify match because columns are not empty, continue to next row 
            if (not pandas.isna(row['spotify_album_uri'])):
                # print("completed: "+str(index)+" "+str(row['spotify_track_name']))
                continue
            else: 
                print("no data yet: "+str(index)+" "+str(row['spotify_album_uri']))

            # if has the same content as last row, don't redo search 
            if (bb_song+bb_performer != last): # no redundant call if same as previous song and performer
                d = (sp.search(q=bb_song+"artist:"+(bb_performer),type="track",limit=10))
                my_i = ""

            # if there are search results, iterate through them 
            if (d and d.get('tracks') and d.get('tracks').get('items')):

                for dd_index in range(len(d.get('tracks').get('items'))):
                    
                    # if a previous result item was a match, continue to next row 
                    if (match):
                        last = bb_song+bb_performer
                        break
                    
                    dd = d.get('tracks').get('items')[dd_index]
                    s_name = dd['name']

        
                    # loop through all artists in case multiple, to find a match with the billboard row data
                    for i in range(len(dd.get('artists'))):

                        if (len(dd.get('artists')) == 0):
                            break

                        artist_name = dd.get('artists')[i].get('name')

                        if ((clean(s_name) in clean(bb_song) or clean(bb_song) in clean(s_name)) and (clean(artist_name) in clean(bb_performer) or clean(bb_performer) in clean(artist_name))):
                            match = True
                            break
                            
                        if not match and prompt.lower() == 'y':
                            print("row "+str(index)+"\tresult: "+str(dd_index)+"\t"+clean(s_name)+"  !=  "+clean(bb_song)+"\t\t\t\t"+clean(artist_name)+"  !=  "+clean(bb_performer))
                        # print(d)
                    
                    if match: 

                        df = write(df, index, dd)              
            
            if not match and prompt.lower() == 'y': 
                print("\nno match found for "+bb_song+" by "+bb_performer)

                # if this row is the same as last one, do not prompt again
                if my_i=="" and my_i!="0":
                    my_i = str(input("\nwhich index should be chosen? (or n for none, d to print dict, a to abort, or url)"))
                
                if (my_i == 'd'):
                    print(d)
                    my_i = str(input("\nwhich index should be chosen? (or n for none, a to abort, or url)"))

                if (my_i == 'a'):
                    df.to_csv(file_write)
                    print("aborting")
                    return
                    
                elif (my_i == 'n'):
                    print('n, will skip')
                    last = bb_song+bb_performer
                    continue

                elif (len(my_i)> 2):
                    new_track_id = "spotify:track:"+my_i.split("?")[0].split('/')[-1]
                    print(new_track_id)
                    d = (sp.track(new_track_id))
                    df = write(df, index, d)
                    print("manually added "+d.get('name'))

                elif (int(my_i) <= len(d.get('tracks').get('items'))):

                    dd = d.get('tracks').get('items')[int(my_i)]

                    df = write(df, index, d.get('tracks').get('items')[int(my_i)])

                    print('filled '+str(my_i))
                else:
                    print('ERROR, saving file')
                    df.to_csv(file_write)
                    return
                
                print('\n\n\n')
                # break

            last = bb_song+bb_performer

    except KeyboardInterrupt as e:
        df.to_csv(file_write)
        print('ABORTED at')
        print(index)

    except ValueError as e:
        df.to_csv(file_write)
        print('ABORTED at')
        print(index)

    df.to_csv(file_write)


"""

"""
def clean(dirty):
    return re.sub(r'[^a-zA-Z0-9]', '',(unidecode((dirty.replace("&","and").replace("#","number").replace("%", "percent").lower().strip()))))
    # return dirty.replace("&","and").replace("#","number").replace("%", "percent").lower().strip()

"""

"""
def write(df, index, track_dict):
    for a in range(len(track_dict.get('artists'))):
        df.loc[index, 'spotify_artist'+str(a+1)+'_name'] = track_dict.get('artists')[a].get('name')
        df.loc[index, 'spotify_artist'+str(a+1)+'_uri'] = track_dict.get('artists')[a].get('uri')

    df.loc[index, 'spotify_album_release_date'] = track_dict.get('album').get('release_date')
    df.loc[index, 'spotify_album_name'] = track_dict.get('album').get('name')
    df.loc[index, 'spotify_album_total_tracks'] = track_dict.get('album').get('total_tracks')
    df.loc[index, 'spotify_album_uri'] = track_dict.get('album').get('uri')
    df.loc[index, 'spotify_album_image'] = track_dict.get('album').get('images')[0].get('url') if (len(track_dict.get('album').get('images'))>0) else ''
    df.loc[index, 'spotify_track_name'] = track_dict.get('name')
    df.loc[index, 'spotify_track_popularity'] = track_dict.get('popularity')
    df.loc[index, 'spotify_track_duration_ms'] = track_dict.get('duration_ms')
    df.loc[index, 'spotify_track_explicit'] = track_dict.get('explicit')
    df.loc[index, 'spotify_track_number'] = track_dict.get('track_number')
    df.loc[index, 'spotify_track_uri'] = track_dict.get('uri')
    return df
    

"""
starting with csv of all billboard hot 100 songs, can do one or both of these functions:    

    make_file_ishiphop: annotate file with YES/NO is hip hop 

    make_file_billboardhiphop: remove all rows that do not correspond to a hiphop artist in wiki_hiphop_artists_and_groups

"""
def billboard_filter_hiphop(make_file_ishiphop = False, make_file_billboardhiphop = False):
    
    billboard = pandas.read_csv(FILE_BILLBOARD)

    if (make_file_ishiphop):
        billboard_is_hiphop = pandas.read_csv(FILE_BILLBOARD)
        billboard_is_hiphop['is_wiki_hiphop_artist'] = ''
        billboard_is_hiphop['artist1_name'] = ''
        billboard_is_hiphop['artist2_name'] = ''
    
    artists = pandas.read_csv(FILE_HIPHOP_ARTISTS)
    artist_list = artists['hiphop_artist_name'].values.tolist()

    # significantly faster to drop all indices of dataframe at once
    indices_to_remove = []

    # once matches to list, saves to dict for O(1) lookup later
    not_hiphop_artist = {}
    hiphop_artist = {}

    for index, row in billboard.iterrows():
        if (index % 5000 == 0):
            print("at index: "+str(index))

        bb_artists = clean(row['billboard_performer']).split('featuring')
        for artist_index in range(len(bb_artists)):

            artist = bb_artists[artist_index]
            
            if (make_file_ishiphop):
                billboard.loc[index, 'artist'+(artist_index+1)+'_name'] = artist
           
            # if artist not in hiphop_artist and (artist in not_hiphop_artist or artist not in artist_list):
            if not hiphop_artist.get(artist) and (not_hiphop_artist.get(artist) or artist not in artist_list):
                indices_to_remove.append(index)
                not_hiphop_artist[artist] = True
                break
            else:
                hiphop_artist[artist] = True
                if (make_file_ishiphop):
                    billboard_is_hiphop.loc[index, 'is_wiki_hiphop_artist'] = 'YES'

    if (make_file_billboardhiphop):
        billboard.drop(billboard.index[indices_to_remove], inplace=True)
        billboard.to_csv(FILE_BILLBOARD_HIPHOP)
        print('new file saved with only hiphop billboard instances:', FILE_BILLBOARD_HIPHOP)
    
    elif(make_file_ishiphop):
        billboard_is_hiphop.to_csv(FILE_BILLBOARD_ISHIPHOP)
        print('new file saved with if billboard instance is hiphop:', FILE_BILLBOARD_ISHIPHOP)
    
    else:
        print('WARNING, did not specify flag for billboard_hiphop_only')


"""
the billboard data has one row for each time a song was in the billboard top 100 chart, so each song could have multiple rows. 
If there are consecutive rows for the same song, this function will remove all but the last 
Assumes is already sorted by song + date first, as is current csv. 

Not used in final visualization.
"""
def last_line_only():
    
    billboard = pandas.read_csv('compiled10.csv')

    indices_to_remove = []
    last_billboard_song_id = ''

    for index, row in billboard.iterrows():

        if (last_billboard_song_id == row['billboard_song_id']):
            indices_to_remove.append(index-1)

        last_billboard_song_id = row['billboard_song_id']

    billboard.drop(billboard.index[indices_to_remove], inplace=True)
    billboard.to_csv('compiled10.csv')
    print('new file saved')

main()
