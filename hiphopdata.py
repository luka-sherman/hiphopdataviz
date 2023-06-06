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

FILE_READ = 'mega_0517_inprogress_with_artists.csv'
FILE_WRITE = 'mega_0517_inprogress_with_albums.csv'

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope="user-library-read"))

"""
uncomment whichever you want to run 
"""
def main():
    billboard_filter_hiphop(make_file_ishiphop=False, make_file_billboardhiphop=False)
    # add_spotify_api_to_billboard_data
    # add_extra_spotify_fields2()
    # add_track_spotify_fields()
    # add_artists_spotify_fields()
    # add_album_spotify_fields()
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

#    df['spotify_track_acousticness'] = ''
#    df['spotify_track_danceability'] = ''
#    df['spotify_track_energy'] = ''
#    df['spotify_track_instrumentalness'] = ''
#    df['spotify_track_key'] = ''
#    df['spotify_track_liveness'] = ''
#    df['spotify_track_loudness'] = ''
#    df['spotify_track_mode'] = ''
#    df['spotify_track_speechiness'] = ''
#    df['spotify_track_tempo'] = ''
#    df['spotify_track_time_signature'] = ''
#    df['spotify_track_valence'] = ''
    # df['spotify_track_embed'] = ''
    # df['spotify_track_id'] = ''
    # df['spotify_track_url'] = ''
    # df['spotify_track_isrc'] = ''
    # df['spotify_track_ean'] = ''
    # df['spotify_track_upc'] = ''
    
    # df['spotify_album_type'] = ''
    # df['spotify_album_url'] = ''
    # df['spotify_album_isrc'] = ''
    # df['spotify_album_ean'] = ''
    # df['spotify_album_upc'] = ''
    # df['spotify_album_genres'] = ''
    # df['spotify_album_label'] = ''
    # df['spotify_album_popularity'] = ''

    # df['spotify_track_artist1_followers'] = ''
    # df['spotify_track_artist1_genres'] = ''
    # df['spotify_track_artist1_url'] = ''
    # df['spotify_track_artist1_id'] = ''
    # df['spotify_track_artist1_image_url'] = ''
    # df['spotify_track_artist1_name'] = ''
    # df['spotify_track_artist1_popularity'] = ''

    # df['spotify_track_artist2_followers'] = ''
    # df['spotify_track_artist2_genres'] = ''
    # df['spotify_track_artist2_url'] = ''
    # df['spotify_track_artist2_id'] = ''
    # df['spotify_track_artist2_image_url'] = ''
    # df['spotify_track_artist2_name'] = ''
    # df['spotify_track_artist2_popularity'] = ''


    # df['spotify_track_artist3_followers'] = ''
    # df['spotify_track_artist3_genres'] = ''
    # df['spotify_track_artist3_url'] = ''
    # df['spotify_track_artist3_id'] = ''
    # df['spotify_track_artist3_image_url'] = ''
    # df['spotify_track_artist3_name'] = ''
    # df['spotify_track_artist3_popularity'] = ''


    # df['spotify_track_artist4_followers'] = ''
    # df['spotify_track_artist4_genres'] = ''
    # df['spotify_track_artist4_url'] = ''
    # df['spotify_track_artist4_id'] = ''
    # df['spotify_track_artist4_image_url'] = ''
    # df['spotify_track_artist4_name'] = ''
    # df['spotify_track_artist4_popularity'] = ''


    # df['spotify_track_artist5_followers'] = ''
    # df['spotify_track_artist5_genres'] = ''
    # df['spotify_track_artist5_url'] = ''
    # df['spotify_track_artist5_id'] = ''
    # df['spotify_track_artist5_image_url'] = ''
    # df['spotify_track_artist5_name'] = ''
    # df['spotify_track_artist5_popularity'] = ''


    # df['spotify_track_artist6_followers'] = ''
    # df['spotify_track_artist6_genres'] = ''
    # df['spotify_track_artist6_url'] = ''
    # df['spotify_track_artist6_id'] = ''
    # df['spotify_track_artist6_image_url'] = ''
    # df['spotify_track_artist6_name'] = ''
    # df['spotify_track_artist6_popularity'] = ''


    last_track_uri = ''
    d = None

    try:

        # for each entry in the billboard top 100 
        for i, row in df.iterrows():
        
            if (i>100):
                break
            
            if (i % 1000 == 0):
                print("at index: "+str(i))

            # if there is no spotify track info, continue to next row 
            if (pandas.isna(row['spotify_track_uri'])):
                continue

            # track_uri = row['spotify_track_uri']
            album_uri = row['spotify_album_uri']

            # if has the same content as last row, don't redo search 
            if (album_uri != last_track_uri): # no redundant call if same as previous song and performer
                
                try:
                    # track_audio_features = sp.audio_features(track_uri)
#                    track_audio_analysis = sp.audio_analysis(track_uri)
                    # track_id = track_uri.split('spotify:track:')[1]
                    album_uri = album_uri.split('spotify:track:')[1]
                    d = sp.album(album_uri)
                except spotipy.exceptions.SpotifyException as e:
                    df.to_csv(FILE_WRITE)
                    print('ERROR at '+str(i))

            # if there are search results, iterate through them 

            if (d):

                df.loc[i, 'spotify_track_id'] = track_id
                df.loc[i, 'spotify_track_embed'] = """<iframe style="border-radius:12px" src="https://open.spotify.com/embed/track/"""+track_id+"""?utm_source=generator&theme=0" width="100%" height="152" frameBorder="0" allowfullscreen="" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" loading="lazy"></iframe>"""
                df.loc[i, 'spotify_track_url'] = d.get('external_urls', {}).get('spotify', '')
                df.loc[i, 'spotify_track_isrc'] = d.get('external_ids', {}).get('isrc', '')
                # df.loc[i, 'spotify_track_ean'] = d.get('external_ids', {}).get('ean', '') # removed because never present 
                # df.loc[i, 'spotify_track_upc'] = d.get('external_ids', {}).get('upc', '')# removed because never present 

                album = d.get('album')
                if album:
                    df.loc[i, 'spotify_album_type'] = album.get('album_type', '')
                    df.loc[i, 'spotify_album_url'] = album.get('external_urls', {}).get('spotify', '')
                    # df.loc[i, 'spotify_album_isrc'] = album.get('external_ids', {}).get('isrc', '') # removed because never present 
                    # df.loc[i, 'spotify_album_ean'] = album.get('external_ids', {}).get('ean', '') # removed because never present 
                    df.loc[i, 'spotify_album_upc'] = album.get('external_ids', {}).get('upc', '')
                    df.loc[i, 'spotify_album_genres'] = str(album.get('genres', []))
                    df.loc[i, 'spotify_album_label'] = album.get('label', '')
                    df.loc[i, 'spotify_album_popularity'] = album.get('popularity', '')

                for artist_i in range(len(d.get('artists'))):
                    artist = d.get('artists')[artist_i]
                    ai = str(artist_i+1)
                    df.loc[i, 'spotify_track_artist'+(ai)+'_url'] = artist.get('external_urls', {}).get('spotify', '')
                    df.loc[i, 'spotify_track_artist'+(ai)+'_followers'] = artist.get('followers', {}).get('total', '')
                    df.loc[i, 'spotify_track_artist'+(ai)+'_genres'] = str(artist.get('genres', []))
                    df.loc[i, 'spotify_track_artist'+(ai)+'_id'] = artist.get('id', '')
                    df.loc[i, 'spotify_track_artist'+(ai)+'_image_url'] = artist.get('images', [])[0].get('url', '') if artist.get('images') else ''
                    df.loc[i, 'spotify_track_artist'+(ai)+'_name'] = artist.get('name', '')
                    df.loc[i, 'spotify_track_artist'+(ai)+'_popularity'] = artist.get('popularity', '')



                # df.loc[i, 'spotify_track_liveness'] = d.get('liveness')
                # df.loc[i, 'spotify_track_loudness'] = d.get('loudness')
                # df.loc[i, 'spotify_track_mode'] = d.get('mode')
                # df.loc[i, 'spotify_track_speechiness'] = d.get('speechiness')
                # df.loc[i, 'spotify_track_tempo'] = d.get('tempo')
                # df.loc[i, 'spotify_track_time_signature'] = d.get('time_signature')
                # df.loc[i, 'spotify_track_valence'] = d.get('valence')          


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
            
#            if (track_audio_analysis):
#
#                df.loc[i, 'spotify_track_acousticness'] = track_audio_analysis.get('acousticness')
#                df.loc[i, 'spotify_track_danceability'] = track_audio_analysis.get('danceability')
#                df.loc[i, 'spotify_track_energy'] = track_audio_analysis.get('energy')
#                df.loc[i, 'spotify_track_instrumentalness'] = track_audio_analysis.get('instrumentalness')
#                df.loc[i, 'spotify_track_key'] = track_audio_analysis.get('key')
#                df.loc[i, 'spotify_track_liveness'] = track_audio_analysis.get('liveness')
#                df.loc[i, 'spotify_track_loudness'] = track_audio_analysis.get('loudness')
#                df.loc[i, 'spotify_track_mode'] = track_audio_analysis.get('mode')
#                df.loc[i, 'spotify_track_speechiness'] = track_audio_analysis.get('speechiness')
#                df.loc[i, 'spotify_track_tempo'] = track_audio_analysis.get('tempo')
#                df.loc[i, 'spotify_track_time_signature'] = track_audio_analysis.get('time_signature')
#                df.loc[i, 'spotify_track_valence'] = track_audio_analysis.get('valence')
            
        

            last_track_uri = album_uri

    except KeyboardInterrupt as e:
        df.to_csv(FILE_WRITE)
        print('ABORTED at')
        print(i)

    except ValueError as e:
        df.to_csv(FILE_WRITE)
        print('ABORTED at')
        print(i)

    df.to_csv(FILE_WRITE)

def add_track_spotify_fields():

    df = pandas.read_csv(FILE_READ)

    last_track_uri = ''
    d = None

    try:

        # for each entry in the billboard top 100 
        for i, row in df.iterrows():
        
            if (i<13113):
                continue
            
            if (i % 1000 == 0):
                print("at index: "+str(i))

            # if there is no spotify track info, continue to next row 
            if (pandas.isna(row['spotify_track_uri'])):
                continue

            track_uri = row['spotify_track_uri']

            # if has the same content as last row, don't redo search 
            if (track_uri != last_track_uri): # no redundant call if same as previous song and performer
                
                try:
                    track_id = track_uri.split('spotify:track:')[1]
                    d = sp.track(track_id)
                except spotipy.exceptions.SpotifyException as e:
                    df.to_csv(FILE_WRITE)
                    print('ERROR at '+str(i))

            # if there are search results, iterate through them 

            if (d):

                df.loc[i, 'spotify_track_id'] = track_id
                # df.loc[i, 'spotify_track_embed'] = """<iframe style="border-radius:12px" src="https://open.spotify.com/embed/track/"""+track_id+"""?utm_source=generator&theme=0" width="100%" height="152" frameBorder="0" allowfullscreen="" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" loading="lazy"></iframe>"""
                # df.loc[i, 'spotify_track_url'] = d.get('external_urls', {}).get('spotify', '')
                # df.loc[i, 'spotify_track_isrc'] = d.get('external_ids', {}).get('isrc', '')
                # df.loc[i, 'spotify_track_ean'] = d.get('external_ids', {}).get('ean', '')
                # df.loc[i, 'spotify_track_upc'] = d.get('external_ids', {}).get('upc', '')

                # album = d.get('album')
                # if album:
                #     df.loc[i, 'spotify_album_type'] = album.get('album_type', '')
                #     df.loc[i, 'spotify_album_url'] = album.get('external_urls', {}).get('spotify', '')
                #     df.loc[i, 'spotify_album_isrc'] = album.get('external_ids', {}).get('isrc', '')
                #     df.loc[i, 'spotify_album_ean'] = album.get('external_ids', {}).get('ean', '')
                #     df.loc[i, 'spotify_album_upc'] = album.get('external_ids', {}).get('upc', '')
                #     df.loc[i, 'spotify_album_genres'] = str(album.get('genres', []))
                #     df.loc[i, 'spotify_album_label'] = album.get('label', '')
                #     df.loc[i, 'spotify_album_popularity'] = album.get('popularity', '')

                for artist_i in range(len(d.get('artists'))):
                    artist = d.get('artists')[artist_i]
                    ai = str(artist_i+1)
                    df.loc[i, 'spotify_track_artist'+(ai)+'_url'] = artist.get('external_urls', {}).get('spotify', '')
                    df.loc[i, 'spotify_track_artist'+(ai)+'_followers'] = artist.get('followers', {}).get('total', '')
                    df.loc[i, 'spotify_track_artist'+(ai)+'_genres'] = str(artist.get('genres', []))
                    df.loc[i, 'spotify_track_artist'+(ai)+'_id'] = artist.get('id', '')
                    df.loc[i, 'spotify_track_artist'+(ai)+'_image_url'] = artist.get('images', [])[0].get('url', '') if artist.get('images') else ''
                    df.loc[i, 'spotify_track_artist'+(ai)+'_name'] = artist.get('name', '')
                    df.loc[i, 'spotify_track_artist'+(ai)+'_popularity'] = artist.get('popularity', '')

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



def add_artists_spotify_fields():

    df = pandas.read_csv(FILE_READ)

    # last_spotify_track_artist1_id = '' 
    # last_spotify_track_artist2_id = '' 
    # last_spotify_track_artist3_id = ''
    # last_spotify_track_artist4_id = ''
    # last_spotify_track_artist5_id = ''
    # last_spotify_track_artist6_id = ''
    # d = None

    #     billboard['spotify_album_name'] = ''
    # billboard['spotify_album_release_date'] = ''
    # billboard['spotify_album_total_tracks'] = ''
    # billboard['spotify_album_image'] = ''
    # billboard['spotify_album_uri'] = ''
    # billboard['spotify_track_name'] = ''
    # billboard['spotify_track_popularity'] = ''
    # billboard['spotify_track_duration_ms'] = ''
    # billboard['spotify_track_explicit'] = ''
    # billboard['spotify_track_number'] = ''
    # billboard['spotify_track_uri'] = ''

    all_artists = {}

    try:

        # for each entry in the billboard top 100 
        for i, row in df.iterrows():
        
            # if (i>100):
            #     break
            
            if (i % 1000 == 0):
                print("at index: "+str(i))

            # if there is no spotify track info, continue to next row 
            if (pandas.isna(row['spotify_track_uri'])):
                continue

            
            for artist_index in range(1, 7):

                if (pandas.isna(row['spotify_track_artist'+str(artist_index)+'_id'])):
                    continue
                
                artist_id = str(row['spotify_track_artist'+str(artist_index)+'_id'])
                # print(artist_id)
                if all_artists.get(artist_id):
                    d = all_artists.get(artist_id) 
                else:
                    d = sp.artist(artist_id)
                    all_artists[artist_id] = d                    
                
                # print(d)
                
                if (d):
                    df.loc[i, 'spotify_track_artist'+str(artist_index)+'_url'] = d.get('external_urls', {}).get('spotify', '')
                    df.loc[i, 'spotify_track_artist'+str(artist_index)+'_followers'] = d.get('followers', {}).get('total', '')
                    df.loc[i, 'spotify_track_artist'+str(artist_index)+'_genres'] = str(d.get('genres', []))
                    df.loc[i, 'spotify_track_artist'+str(artist_index)+'_id'] = d.get('id', '')
                    df.loc[i, 'spotify_track_artist'+str(artist_index)+'_image_url'] = d.get('images', [])[0].get('url', '') if d.get('images') else ''
                    df.loc[i, 'spotify_track_artist'+str(artist_index)+'_name'] = d.get('name', '')
                    df.loc[i, 'spotify_track_artist'+str(artist_index)+'_popularity'] = d.get('popularity', '')

                # every_artist[row['spotify_track_artist1_id']]) if (pandas.notna(row['spotify_track_artist1_id'])) else None
                # every_artist.append(row['spotify_track_artist2_id']) if (pandas.notna(row['spotify_track_artist2_id'])) else None
                # every_artist.append(row['spotify_track_artist3_id']) if (pandas.notna(row['spotify_track_artist3_id'])) else None
                # every_artist.append(row['spotify_track_artist4_id']) if (pandas.notna(row['spotify_track_artist4_id'])) else None
                # every_artist.append(row['spotify_track_artist5_id']) if (pandas.notna(row['spotify_track_artist5_id'])) else None
                # every_artist.append(row['spotify_track_artist6_id']) if (pandas.notna(row['spotify_track_artist6_id'])) else None


            # spotify_track_artist1_id = row['spotify_track_artist1_id']
            # spotify_track_artist2_id = row['spotify_track_artist2_id']
            # spotify_track_artist3_id = row['spotify_track_artist3_id']
            # spotify_track_artist4_id = row['spotify_track_artist4_id']
            # spotify_track_artist5_id = row['spotify_track_artist5_id']
            # spotify_track_artist6_id = row['spotify_track_artist6_id']

            # artists = []
            # artists.append(row['spotify_track_artist1_id']) if (pandas.notna(row['spotify_track_artist1_id'])) else None
            # artists.append(row['spotify_track_artist2_id']) if (pandas.notna(row['spotify_track_artist2_id'])) else None
            # artists.append(row['spotify_track_artist3_id']) if (pandas.notna(row['spotify_track_artist3_id'])) else None
            # artists.append(row['spotify_track_artist4_id']) if (pandas.notna(row['spotify_track_artist4_id'])) else None
            # artists.append(row['spotify_track_artist5_id']) if (pandas.notna(row['spotify_track_artist5_id'])) else None
            # artists.append(row['spotify_track_artist6_id']) if (pandas.notna(row['spotify_track_artist6_id'])) else None

            # if has the same content as last row, don't redo search 
            # if (artists != last_artists): 


            # if (spotify_track_artist1_id != last_spotify_track_artist1_id 
            #     and spotify_track_artist2_id != last_spotify_track_artist2_id 
            #     and spotify_track_artist3_id != last_spotify_track_artist3_id
            #     and spotify_track_artist4_id != last_spotify_track_artist4_id
            #     and spotify_track_artist5_id != last_spotify_track_artist5_id
            #     and spotify_track_artist6_id != last_spotify_track_artist6_id): # no redundant call if same as previous song and performer
                
                # try:
                    # if spotify_track_artist1_id:
                        # note, getting error when try to call artists[list of multiple artists]
                    # d1 = sp.artist(spotify_track_artist1_id) if not (pandas.isna(row['spotify_track_artist1_id'])) else None
                    # d2 = sp.artist(spotify_track_artist2_id) if not (pandas.isna(row['spotify_track_artist2_id'])) else None
                    # d3 = sp.artist(spotify_track_artist3_id) if not (pandas.isna(row['spotify_track_artist3_id'])) else None
                    # d4 = sp.artist(spotify_track_artist4_id) if not (pandas.isna(row['spotify_track_artist4_id'])) else None
                    # d5 = sp.artist(spotify_track_artist5_id) if not (pandas.isna(row['spotify_track_artist5_id'])) else None
                    # d6 = sp.artist(spotify_track_artist6_id) if not (pandas.isna(row['spotify_track_artist6_id'])) else None
                    # artists = []
                    # artists.append(spotify_track_artist1_id) if (pandas.notna(row['spotify_track_artist1_id'])) else None
                    # artists.append(spotify_track_artist2_id) if (pandas.notna(row['spotify_track_artist2_id'])) else None
                    # artists.append(spotify_track_artist3_id) if (pandas.notna(row['spotify_track_artist3_id'])) else None
                    # artists.append(spotify_track_artist4_id) if (pandas.notna(row['spotify_track_artist4_id'])) else None
                    # artists.append(spotify_track_artist5_id) if (pandas.notna(row['spotify_track_artist5_id'])) else None
                    # artists.append(spotify_track_artist6_id) if (pandas.notna(row['spotify_track_artist6_id'])) else None
                    
                    # artists_dicts = sp.artists(artists)
                #     # artists_dicts = sp.artists([spotify_track_artist1_id, spotify_track_artist2_id, spotify_track_artist3_id, spotify_track_artist4_id, spotify_track_artist5_id, spotify_track_artist6_id])
                # except spotipy.exceptions.SpotifyException as e:
                #     df.to_csv(FILE_WRITE)
                #     print('ERROR at '+str(i))

            # if there are search results, iterate through them 

            # for d in [d1, d2, d3, d4, d5, d5, d6]:
            #     if (d):
            #         df.loc[i, 'spotify_track_artist1_url'] = d.get('external_urls', {}).get('spotify', '')
            #         df.loc[i, 'spotify_track_artist1_followers'] = d.get('followers', {}).get('total', '')
            #         df.loc[i, 'spotify_track_artist1_genres'] = str(d.get('genres', []))
            #         df.loc[i, 'spotify_track_artist1_id'] = d.get('id', '')
            #         df.loc[i, 'spotify_track_artist1_image_url'] = d.get('images', [])[0].get('url', '') if d.get('images') else ''
            #         df.loc[i, 'spotify_track_artist1_name'] = d.get('name', '')
            #         df.loc[i, 'spotify_track_artist1_popularity'] = d.get('popularity', '')
            # for d in artists_dicts:
            #     if (d):
            #         df.loc[i, 'spotify_track_artist1_url'] = d.get('external_urls', {}).get('spotify', '')
            #         df.loc[i, 'spotify_track_artist1_followers'] = d.get('followers', {}).get('total', '')
            #         df.loc[i, 'spotify_track_artist1_genres'] = str(d.get('genres', []))
            #         df.loc[i, 'spotify_track_artist1_id'] = d.get('id', '')
            #         df.loc[i, 'spotify_track_artist1_image_url'] = d.get('images', [])[0].get('url', '') if d.get('images') else ''
            #         df.loc[i, 'spotify_track_artist1_name'] = d.get('name', '')
            #         df.loc[i, 'spotify_track_artist1_popularity'] = d.get('popularity', '')
    

            # last_artists = artists
    except spotipy.exceptions.SpotifyException as e:
        df.to_csv(FILE_WRITE)
        print('ERROR at '+str(i))

    except KeyboardInterrupt as e:
        df.to_csv(FILE_WRITE)
        print('ABORTED at')
        print(i)

    except ValueError as e:
        df.to_csv(FILE_WRITE)
        print('ABORTED at')
        print(i)

    df.to_csv(FILE_WRITE)

def add_album_spotify_fields():

    df = pandas.read_csv(FILE_READ)

    last_spotify_album_uri = '' 
    album = None

    # df['spotify_album_id'] = ''

    try:

        # for each entry in the billboard top 100 
        for i, row in df.iterrows():
        
            # if (i>58):
            #     break
            
            if (i % 500 == 0):
                print("at index: "+str(i))

            # if there is no spotify track info, continue to next row 
            if (pandas.isna(row['spotify_album_uri'])):
                continue
            # if there is album id already filled in, 
            # if (pandas.notna(row['spotify_album_id'])):
            #     continue
            
    
            spotify_album_uri = row['spotify_album_uri']

            # if has the same content as last row, don't redo search 
            if (spotify_album_uri != last_spotify_album_uri): # no redundant call if same as previous song and performer
                try:
                    spotify_album_id = spotify_album_uri.split('spotify:album:')[1]
                    album = sp.album(spotify_album_id) 
                    # print(album)
                except spotipy.exceptions.SpotifyException as e:
                    df.to_csv(FILE_WRITE)
                    print('ERROR at '+str(i))

            # if there are search results, iterate through them 
            if (album):
                df.loc[i, 'spotify_album_id'] = spotify_album_id
                df.loc[i, 'spotify_album_type'] = album.get('album_type', '')
                df.loc[i, 'spotify_album_url'] = album.get('external_urls', {}).get('spotify', '')
                df.loc[i, 'spotify_album_isrc'] = album.get('external_ids', {}).get('isrc', '')
                df.loc[i, 'spotify_album_ean'] = album.get('external_ids', {}).get('ean', '')
                df.loc[i, 'spotify_album_upc'] = album.get('external_ids', {}).get('upc', '')
                # df.loc[i, 'spotify_album_genres'] = str(album.get('genres', [])) removed because never present
                df.loc[i, 'spotify_album_label'] = album.get('label', '')
                df.loc[i, 'spotify_album_popularity'] = album.get('popularity', '')
    
            last_spotify_album_uri = spotify_album_uri 

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
