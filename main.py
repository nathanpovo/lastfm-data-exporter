
'''
Copyright 2016 Nathan Povo

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''

import string
import time
import json
import operator
import urllib.request
import math
import threading
import os


def add_tracks(tracksList ,finalJson):
    
    Final = finalJson
    Tracks = tracksList
    
    artists = Final['artists']
    
    for track in Tracks['tracks']:
        
        
        # checks if a track is currently playing (according to lastfm)
        # if it is the track is skipped
        try:
            if track['@attr']['nowplaying'] == 'true':
                #print('Found now playing track')
                continue
        except KeyError:
            pass
        
        track_artist_info = track['artist']
        artist_mbid = track_artist_info['mbid']
        artist_name = track_artist_info['name']
        file_artist_mbid = next((item for item in artists if item["mbid"] == artist_mbid), None)
        file_artist_name = next((item for item in artists if item["name"] == artist_name), None)
        if file_artist_name == None:
            artists.append({'name': artist_name,'mbid': artist_mbid, 'albums':[]})
            currentArtist = next((item for item in artists if item["name"] == artist_name), None)
        elif file_artist_name != None:
            if file_artist_mbid == None:
                currentArtist = file_artist_name
            elif file_artist_mbid != None:
                currentArtist = file_artist_name
        #
        
        track_album_info = track['album']
        album_mbid = track_album_info['mbid']
        album_name = track_album_info['#text']
        file_album_mbid = next((item for item in currentArtist['albums'] if item["mbid"] == album_mbid), None)
        file_album_name = next((item for item in currentArtist['albums'] if item["name"] == album_name), None)
        if file_album_name == None:
            if file_album_mbid == None:
                if album_name == None:
                    currentArtist['albums'].append({'name': album_name,'mbid': album_mbid, 'tracks':[], 'playcount': 0})
                    currentAlbum = next((item for item in currentArtist['albums'] if item["name"] == album_name and item["mbid"] == album_mbid), None)
                else:
                    currentArtist['albums'].append({'name': album_name,'mbid': album_mbid, 'tracks':[], 'playcount': 0})
                    currentAlbum = next((item for item in currentArtist['albums'] if item["name"] == album_name), None)
            else:
                currentArtist['albums'].append({'name': album_name,'mbid': album_mbid, 'tracks':[], 'playcount': 0})
                currentAlbum = next((item for item in currentArtist['albums'] if item["name"] == album_name), None)
        elif file_album_name != None:
            if file_album_mbid == None:
                currentAlbum = file_album_name
            elif file_album_mbid != None:
                currentAlbum = file_album_name
        #
        
        track_mbid = track['mbid']
        track_name = track['name']
        file_track_mbid = next((item for item in currentAlbum['tracks'] if item["mbid"] == track_mbid), None)
        file_track_name = next((item for item in currentAlbum['tracks'] if item["name"] == track_name), None)
        if file_track_name == None:
            currentAlbum['tracks'].append({'name': track_name,'mbid': track_mbid, 'timestamps':[], 'playcount': 0})
            currentTrack = next((item for item in currentAlbum['tracks'] if item["name"] == track_name), None)
        elif file_track_name != None:
            if file_track_mbid == None:
                currentTrack = file_track_name
            elif file_track_mbid != None:
                currentTrack = file_track_name
        #
        
        track_timestamp = track['date']['uts']
        currentTrack['timestamps'].append(track_timestamp)
#

def get_link(tracksList, page, limit, lock, start, username):
    
    Tracks = tracksList
    
    page_time = time.clock()
    url_page = "http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&extended=1" + "&user=" + username + "&page=" + str(page) + "&limit=" + str(limit) + "&from=" + str(start) + "&api_key=" + api_key + "&format=json"
    url_page_req = urllib.request.urlopen(url_page)
    tempJson = json.loads(url_page_req.read().decode('utf-8'))
    locks_acquired = 0
    # checks if the list is locked, if it is locked the thread waits, if it isnt locked the thread locks it and write to the list
    while locks_acquired != 1:
        #print('Page {} trying to acquire lock' .format(page))
        if lock.locked() == False:
            lock.acquire()
            tracks_time = time.clock()
            #print('Lock aquired, page {}' .format(page))
            tracks = tempJson['recenttracks']['track']
            Tracks['tracks'] += tracks
            locks_acquired = 1
            print('Page {} finished' .format(page))
            print('Time to get and add tracks: {}s' .format(time.clock() - tracks_time))
            print('Time taken to finish page: {}s' .format(time.clock() - page_time))
            lock.release()
        else:
            print('Page {} could not aquire lock' .format(page))
#

def get_tracks(username, start, limit, filename):
    
    if filename[-5:] == '.json':
        pass
    else:
        filename += '.json'
    
    # gets the total amount of tracks and finds the timestamp of the last listened track
    tempLimit = 2
    url = "http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&extended=1" + "&user=" + username + "&page=1" + "&limit=" + str(tempLimit) + "&from=" + str(start) + "&api_key=" + api_key + "&format=json"
    url_req = urllib.request.urlopen(url)
    recentTrackInfo = json.loads(url_req.read().decode("utf-8"))
    #print(recentTrackInfo)
    
    total_tracks = int(recentTrackInfo['recenttracks']["@attr"]["total"])
    total_pages = math.ceil(total_tracks/limit)
    print('Total number of pages: {}' .format(total_pages))
    
    if int(start) == 0:
        Final = {}
        Final['user'] = username
        Final['artists'] = []
        presentTracks = 0
    else:
        Final = json.load(open(filename, 'r'))
        presentTracks = Final['total playcount']
    #
    
    try:
        Final['last track'] = recentTrackInfo['recenttracks']['track'][0]['date']['uts']
    except KeyError:
        try:
            Final['last track'] = recentTrackInfo['recenttracks']['track'][1]['date']['uts']
        except IndexError:
            pass
    except IndexError:
        pass
    
    CurrentPage = 1
    downloadThreads = []
    
    max_num_Threads = 20
    num_Threads = max_num_Threads
    pages_left = total_pages
    pagesAcquired = 0
    
    pages_time = time.clock()
    while pages_left > 0:
        pageTracks = {}
        pageTracks['tracks'] = []
        #print('CurrentPage {}' .format(CurrentPage))
        # number of threads to open
        # for loop with a range from the current page to (currentpage + num_Threads)
        # depending on the value of num_Threads, threads will be open simultanouesly
        
        if pages_left < num_Threads:
            num_Threads = pages_left
            print('----------------------------------------------------------')
            print('Number of threads has been decreased to {}' .format(num_Threads))
            print('----------------------------------------------------------')
        
        for page in range(CurrentPage, (CurrentPage + num_Threads)):
            downloadThread = threading.Thread(target=get_link, args=(pageTracks, page, limit, lock, start, username))
            downloadThreads.append(downloadThread)
            downloadThread.start()
            pagesAcquired += 1
        
        for downloadThread in downloadThreads:
            downloadThread.join()
        
        pages_left = total_pages - pagesAcquired
        print('Pages left {}' .format(pages_left))
        CurrentPage += num_Threads
        
        add_tracks(pageTracks, Final)
    ###
    print('----------------------------------------------------------')
    #print('number of tracks obtained: {}' .format(len(pageTracks['tracks'])))
    print('Time to get all tracks: {}' .format(time.clock() - pages_time))
    print('----------------------------------------------------------')
    
    
    
    #add_tracks(Tracks, Final)
    
    
    
    
    total_playcount = 0
    
    # finds the number of playcounts for every track, album, artist and also the total playcount
    Final['total playcount'] = 0
    
    for artist in Final['artists']:
        artist['playcount'] = 0
        for album in artist['albums']:
            album['playcount'] = 0
            for track in album['tracks']:
                track['playcount'] = 0
                for timestamp in track['timestamps']:
                    total_playcount += 1
                    track['playcount'] += 1
                    album['playcount'] += 1
                    artist['playcount'] += 1
                    Final['total playcount'] += 1
    #
    # sorts artists, albums and tracks by number of playcounts
    Final['artists'] = sorted(Final['artists'], key=operator.itemgetter('playcount'), reverse=True)
    for artist in Final['artists']:
        artist['albums'] = sorted(artist['albums'], key=operator.itemgetter('playcount'), reverse=True)
        for album in artist['albums']:
            album['tracks'] = sorted(album['tracks'], key=operator.itemgetter('playcount'), reverse=True)
            for track in album['tracks']:
                track['timestamps'] = sorted(track['timestamps'], reverse=True)
    #
    json.dump(Final, open(filename, 'w'))
    print('Total number of tracks: {}' .format(total_playcount))
    print('Number of tracks added: {}' .format(total_playcount - presentTracks))
#

def update(filename):
    
    file = json.load(open(filename, 'r'))
    lastPlay = file['last track']
    startingTime = int(lastPlay) + 1
    
    username = file['user']
    
    get_tracks(username, startingTime, 50, filename)
#

def settings():
    settings_filename = 'lastfm data settings.json'
    username = ''
    filename = ''
    
    settings = {'username': username, 'filename':filename}
    
    if os.path.isfile(settings_filename):
        settings = json.load(open(settings_filename, 'r'))
    
    return settings

#def __name__(__main__):
    
lock = threading.Lock()

valid_chars = "!£$^&()_+{}@~¬`-=[];'#,. %s%s" % (string.ascii_letters, string.digits)

api_key = '41311834bebb507fda9e070db4a0904e'
'''
    print("Enter the command 'help' to get list of avaliable commands.")
    print("Press enter to exit script")

    settings_filename = 'lastfm data settings.json'
    if os.path.isfile(settings_filename):
        settings = json.load(open(settings_filename, 'r'))
        username = settings['username']
        filename = settings['filename']
        try:
            api_key = settings['api_key']
        except KeyError:
            pass
    else:
        username = input('Enter username: ')
        filename = input('Enter filename: ')
        
        if filename[-5:] == '.json':
            pass
        else:
            filename += '.json'
        #
        
        filename = ''.join(c for c in filename if c in valid_chars)
        
        settings = {'username': username, 'filename':filename}
        remember_settings = input('Remember settings? (yes/no)\n').lower()
        if remember_settings == 'yes':
            print('Settings file created')
            print('')
            json.dump(settings, open(settings_filename, 'w'))
        else:
            print('Settings will not be remembered')
    #

    while True:
        pageTracks = {}
        pageTracks['tracks'] = []
        
        print('')
        command = input('Enter command: ').lower()
        print('')
        
        if command == 'filename':
            print('The current filename is: {}' .format(filename))
        #
        
        elif command == 'username':
            print('The current username is: {}' .format(username))
        #
        
        elif command == 'change settings':
            print('Press enter to leave field unchanged')
            print('The current username is: {}' .format(username))
            username = input('Enter username: ')
            if username != '':
                settings['username'] = username
                print('Username changed to {}' .format(username))
            else:
                username = settings["username"]
            
            print('The current filename is: {}' .format(filename))
            filename = input('Enter filename: ')
            
            if filename != '':
                if filename[-5:] == '.json':
                    pass
                else:
                    filename += '.json'
                #
                filename = ''.join(c for c in filename if c in valid_chars)
                settings['filename'] = filename
                print('Filename changed to {}' .format(filename))
            else:
                filename = settings['filename']
            
            json.dump(settings, open(settings_filename, 'w'))
        #
        
        elif command == 'update':
            if os.path.isfile(filename):
                Tracks = {}
                Tracks['tracks'] = []
                update(filename)
            else:
                print('The file with the given filename has not been found.')
                print('Would you like to change the filename or start over(get all tracks)?')
                sub_command = ''
                while sub_command != 'change' or sub_command != 'start over':
                    sub_command = input('Enter command (change/start over): ')
                    if sub_command == 'change':
                        filename = input('Enter filename: ')
                        
                        if filename[-5:] == '.json':
                            pass
                        else:
                            filename += '.json'
                        #
                        filename = ''.join(c for c in filename if c in valid_chars)
                        settings['filename'] = filename
                        print('Filename changed to {}' .format(filename))
                        
                        json.dump(settings, open(settings_filename, 'w'))
                        break
                    elif sub_command == 'start over':
                        grand_start = time.clock()
                        Tracks = {}
                        Tracks['tracks'] = []
                        limit = 200
                        get_tracks(0, limit, filename)
                        print('Total time taken: {}s' .format(time.clock() - grand_start))
                        break
                    elif sub_command == 'exit':
                        break
        #
        
        elif command == 'start over':
            grand_start = time.clock()
            limit = 200
            get_tracks(0, limit, filename)
            print('Total time taken: {}s' .format(time.clock() - grand_start))
        #
        
        elif command == 'change api':
            api_key = input('Input api key: ')
            print('Api key has been changed to: {}' .format(api_key))
        #
        
        elif command == 'help':
            print('start over')
            print('    Fetches all tracks listened by a given user. The output is put into a json file.')
            print('')
            print('update')
            print("    Updates the json file given by the user. Tracks are only added from the 'last track' timestamp. Previous tracks are not touched.")
            print('')
            print('change settings')
            print("    Allows the user to change their settings. Which consist of the username(not recommended changing) and the json filename.")
            print('')
            print('username')
            print("    Shows the current username.")
            print("")
            print("filename")
            print("    Shows the current filename.")
            print("")
            print('change api')
            print("    Allows the user to change the api key used by the script.")
            print('')
        
        elif command == '':
            break
        
        else:
            print('Unknown command.')
'''