# import libraries, need these installed first to run 
import re
import pandas
from num2words import num2words
from unidecode import unidecode
import spotipy
from spotipy.oauth2 import SpotifyOAuth

FILE_READ = 'compiled9.csv'
FILE_WRITE = 'compiled10_with_extra_spotify_fields.csv'

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope="user-library-read"))

"""
uncomment whichever you want to run 
"""
def main():
    # billboard_hiphop_only()
    # last_line_only()
    # add_spotify_api_to_billboard_data
    add_extra_spotify_fields2()
    # billboard_is_hiphop()
    return


def add_extra_spotify_fields():

   

    df = pandas.read_csv(FILE_READ)

    df['spotify_track_acousticness'] = ''
    df['spotify_track_danceability'] = ''
    df['spotify_track_energy'] = ''
    df['spotify_track_instrumentalness'] = ''
    df['spotify_track_key'] = ''
    df['spotify_track_liveness'] = ''
    df['spotify_track_loudness'] = ''
    df['spotify_track_mode'] = ''
    df['spotify_track_speechiness'] = ''
    df['spotify_track_tempo'] = ''
    df['spotify_track_time_signature'] = ''
    df['spotify_track_valence'] = ''

    
    try:

        last_track_uri = ''
        all_track_uris = []

        # for each entry in the billboard top 100 
        for index, row in df.iterrows():

            # if (index > 50):
            #     break
            
            # if (index % 1000 == 0):
            #     print("at index: "+str(index))

            track_uri = row['spotify_track_uri']

            # if there is already a spotify match because columns are not empty, continue to next row 
            # if (not pandas.isna(row['spotify_track_uri'])):
            #     # print("completed: "+str(index)+" "+str(row['spotify_track_name']))
            #     continue
            # else: 
            #     print("no data yet: "+str(index)+" "+str(row['spotify_album_uri']))

            # if has the same content as last row, don't redo search 
            if (track_uri != last_track_uri): # no redundant call if same as previous song and performer
                all_track_uris.append(track_uri)


            last_track_uri = track_uri

        # print(all_track_uris)
        print('starting api call')
        # all_track_audio_features = sp.audio_features(all_track_uris)
        # print('completed api call')
        # print(all_track_audio_features)
        csv_index = 0

        for i_100s in range(0, len(all_track_uris), 100):

                

            all_track_audio_features = sp.audio_features(all_track_uris)

            for i in range(i_100s):

                if (i % 1000 == 0):
                    print("at index: "+str(i))
                
                df.loc[[3]]

                d = all_track_audio_features[i]

                # if there are search results, iterate through them 
                if (d):

                    df.loc[i, 'spotify_track_acousticness'] = d.get('acousticness')
                    df.loc[i, 'spotify_track_danceability'] = d.get('danceability')
                    df.loc[i, 'spotify_track_energy'] = d.get('energy')
                    df.loc[i, 'spotify_track_instrumentalness'] = d.get('instrumentalness')
                    df.loc[i, 'spotify_track_key'] = d.get('key')
                    df.loc[i, 'spotify_track_liveness'] = d.get('liveness')
                    df.loc[i, 'spotify_track_loudness'] = d.get('loudness')
                    df.loc[i, 'spotify_track_mode'] = d.get('mode')
                    df.loc[i, 'spotify_track_speechiness'] = d.get('speechiness')
                    df.loc[i, 'spotify_track_tempo'] = d.get('tempo')
                    df.loc[i, 'spotify_track_time_signature'] = d.get('time_signature')
                    df.loc[i, 'spotify_track_valence'] = d.get('valence')
               
            # last_track_uri = track_uri

    except KeyboardInterrupt as e:
        df.to_csv(FILE_WRITE)
        print('ABORTED at')
        print(index)

    except ValueError as e:
        df.to_csv(FILE_WRITE)
        print('ABORTED at')
        print(index)

    df.to_csv(FILE_WRITE)


def add_extra_spotify_fields2():

    df = pandas.read_csv(FILE_READ)

    df['spotify_track_acousticness'] = ''
    df['spotify_track_danceability'] = ''
    df['spotify_track_energy'] = ''
    df['spotify_track_instrumentalness'] = ''
    df['spotify_track_key'] = ''
    df['spotify_track_liveness'] = ''
    df['spotify_track_loudness'] = ''
    df['spotify_track_mode'] = ''
    df['spotify_track_speechiness'] = ''
    df['spotify_track_tempo'] = ''
    df['spotify_track_time_signature'] = ''
    df['spotify_track_valence'] = ''

    last_track_uri = ''
    d = None

    try:

        # for each entry in the billboard top 100 
        for i, row in df.iterrows():
            
            if (i % 1000 == 0):
                print("at index: "+str(i))

            # if there is no spotify track info, continue to next row 
            if (pandas.isna(row['spotify_track_uri'])):
                continue

            track_uri = row['spotify_track_uri']

            # if has the same content as last row, don't redo search 
            if (track_uri != last_track_uri): # no redundant call if same as previous song and performer
                
                try:
                    # track_audio_features = sp.audio_features(track_uri)
                    track_audio_analysis = sp.audio_analysis(track_uri)
                except spotipy.exceptions.SpotifyException as e:
                    df.to_csv(FILE_WRITE)
                    print('ERROR at '+str(i))

            # if there are search results, iterate through them 
            # if (track_audio_features):

            #     d = track_audio_features[0]

            #     df.loc[i, 'spotify_track_acousticness'] = d.get('acousticness')
            #     df.loc[i, 'spotify_track_danceability'] = d.get('danceability')
            #     df.loc[i, 'spotify_track_energy'] = d.get('energy')
            #     df.loc[i, 'spotify_track_instrumentalness'] = d.get('instrumentalness')
            #     df.loc[i, 'spotify_track_key'] = d.get('key')
            #     df.loc[i, 'spotify_track_liveness'] = d.get('liveness')
            #     df.loc[i, 'spotify_track_loudness'] = d.get('loudness')
            #     df.loc[i, 'spotify_track_mode'] = d.get('mode')
            #     df.loc[i, 'spotify_track_speechiness'] = d.get('speechiness')
            #     df.loc[i, 'spotify_track_tempo'] = d.get('tempo')
            #     df.loc[i, 'spotify_track_time_signature'] = d.get('time_signature')
            #     df.loc[i, 'spotify_track_valence'] = d.get('valence')          
            
            if (track_audio_analysis):

                df.loc[i, 'spotify_track_acousticness'] = track_audio_analysis.get('acousticness')
                df.loc[i, 'spotify_track_danceability'] = track_audio_analysis.get('danceability')
                df.loc[i, 'spotify_track_energy'] = track_audio_analysis.get('energy')
                df.loc[i, 'spotify_track_instrumentalness'] = track_audio_analysis.get('instrumentalness')
                df.loc[i, 'spotify_track_key'] = track_audio_analysis.get('key')
                df.loc[i, 'spotify_track_liveness'] = track_audio_analysis.get('liveness')
                df.loc[i, 'spotify_track_loudness'] = track_audio_analysis.get('loudness')
                df.loc[i, 'spotify_track_mode'] = track_audio_analysis.get('mode')
                df.loc[i, 'spotify_track_speechiness'] = track_audio_analysis.get('speechiness')
                df.loc[i, 'spotify_track_tempo'] = track_audio_analysis.get('tempo')
                df.loc[i, 'spotify_track_time_signature'] = track_audio_analysis.get('time_signature')
                df.loc[i, 'spotify_track_valence'] = track_audio_analysis.get('valence')          
            
        

            last_track_uri = track_uri

    except KeyboardInterrupt as e:
        df.to_csv(FILE_WRITE)
        print('ABORTED at')
        print(i)

    except ValueError as e:
        df.to_csv(FILE_WRITE)
        print('ABORTED at')
        print(i)

    df.to_csv(FILE_WRITE)


"""
 
"""
def add_spotify_api_to_billboard_data():

    prompt = input("prompt if no automatic match found? (y/n) ")

    # df = pandas.read_csv('billboard_hot100_hiphop.csv')
    df = pandas.read_csv(FILE_READ)

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
                    df.to_csv(FILE_WRITE)
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
                    df.to_csv(FILE_WRITE)
                    return
                
                print('\n\n\n')
                # break

            last = bb_song+bb_performer

    except KeyboardInterrupt as e:
        df.to_csv(FILE_WRITE)
        print('ABORTED at')
        print(index)

    except ValueError as e:
        df.to_csv(FILE_WRITE)
        print('ABORTED at')
        print(index)

    df.to_csv(FILE_WRITE)


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
starting with the billboard_hot100_all_genres.csv, remove all rows that do not correspond to a hiphop artist in wiki_hiphop_artists_and_groups
"""

def billboard_is_hiphop():
    billboard = pandas.read_csv('billboard_hot100_all_genres.csv')
    artists = pandas.read_csv('wiki_hiphop_artists_and_groups.csv')

    not_hiphop_artist = {}
    hiphop_artist = {}

    artist_list = artists['hiphop_artist_name'].values.tolist()

    # making some new rows
    billboard['is_wiki_hiphop_artist'] = ''
    billboard['artist1_name'] = ''
    billboard['artist2_name'] = ''

    for index, row in billboard.iterrows():

        if (index % 5000 == 0):
            print("at index: "+str(index))

        bb_artists = clean(row['billboard_performer']).split('featuring')
        billboard.loc[index, 'artist1_name'] = bb_artists[0]
        if (len(bb_artists) > 1):
            billboard.loc[index, 'artist2_name'] = bb_artists[1]

        for artist in bb_artists:
            # if artist not in hiphop_artist and (artist in not_hiphop_artist or artist not in artist_list):
            if not hiphop_artist.get(artist) and (not_hiphop_artist.get(artist) or artist not in artist_list):
                not_hiphop_artist[artist] = True
                break
            else:
                hiphop_artist[artist] = True
                billboard.loc[index, 'is_wiki_hiphop_artist'] = 'YES'

    billboard.to_csv('billboard_is_hiphop.csv')
    print('new file saved: billboard_is_hiphop.csv')
    

def billboard_hiphop_only():
    
    billboard = pandas.read_csv('billboard_hot100_all_genres.csv')
    artists = pandas.read_csv('wiki_hiphop_artists_and_groups.csv')

    not_hiphop_artist = {}
    hiphop_artist = {}
    indices_to_remove = []

    artist_list = artists['hiphop_artist_name'].values.tolist()

    for index, row in billboard.iterrows():
        bb_artists = clean(row['billboard_performer']).split('featuring')
        for artist in bb_artists:
            # if artist not in hiphop_artist and (artist in not_hiphop_artist or artist not in artist_list):
            if not hiphop_artist.get(artist) and (not_hiphop_artist.get(artist) or artist not in artist_list):
                indices_to_remove.append(index)
                not_hiphop_artist[artist] = True
                # print (str(index)+"\t\t"+artist)
                break
            else:
                hiphop_artist[artist] = True
                # print (str(index)+"\t\t"+artist)

    billboard.drop(billboard.index[indices_to_remove], inplace=True)

    billboard['spotify_album_name'] = ''
    billboard['spotify_album_release_date'] = ''
    billboard['spotify_album_total_tracks'] = ''
    billboard['spotify_album_image'] = ''
    billboard['spotify_album_uri'] = ''
    billboard['spotify_track_name'] = ''
    billboard['spotify_track_popularity'] = ''
    billboard['spotify_track_duration_ms'] = ''
    billboard['spotify_track_explicit'] = ''
    billboard['spotify_track_number'] = ''
    billboard['spotify_track_uri'] = ''
  
    billboard['spotify_artist1_name'] = ''
    billboard['spotify_artist1_uri'] = ''
  
    billboard['spotify_artist2_name'] = ''
    billboard['spotify_artist2_uri'] = ''

    billboard['spotify_artist3_name'] = ''
    billboard['spotify_artist3_uri'] = ''

    billboard['spotify_artist4_name'] = ''
    billboard['spotify_artist4_uri'] = ''

    billboard.to_csv('billboard_hiphop2.csv')
    print('new file saved: billboard_hiphop2.csv')


"""
the billboard data has one row for each time a song was in the billboard top 100 chart, so each song could have multiple rows. 
If there are consecutive rows for the same song, this function will remove all but the last 
TODO: make sure is sorted by date + song first  
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