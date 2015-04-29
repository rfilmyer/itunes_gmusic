#itunes-gmusic
#By Roger Filmyer, 2015

#Sketching out what I intend to do:
#Provide an interface between iTunes and Google Play Music
#  * Scratching an itch - comparing my 2 decently-large libraries with a 
#    lot of history
#  * When syncing, play counts update *once*: iTunes -> Google Play Music
#First thing I want to do: be able to pull play counts from GPM and
#    update to iTunes.
#Also: Evaluate what songs differ between my iTunes and my GPM library
#Finally: Compare "thumbs upped" songs to star ratings.

#gmusicapi requires Python 2. Watch it start being compatible with 3 as soon as I finish.

#Tools: pyItunes and gmusicapi

import plistlib  # Later, I'll use pyItunes
import gmusicapi

#Broadly, Functions needed:
#Loading iTunes library
#Loading Google Play Music library
#Match iTunes songs to GPM songs
#Updating Play Counts

#More Specifically:


#Loading iTunes library
def load_itunes(libpath):
    """
    :rtype : list
    :param libpath: path to the XML copy of the iTunes Library
    :return: A list of song dicts
    Songs are considered anything that is "Music" (ie in the Music playlist)
    """
    #One day, I'll be able to use pyItunes for this.
    #That day is not today.
    ituneslib = plistlib.readPlist(libpath)

    music = (playlist for playlist in ituneslib['Playlists']
             if playlist["Name"] == "Music").next()  # StackOverflow #8653516
    assert music['Name'] == 'Music' and music['All Items']

    songids = []
    for element in music['Playlist Items']:
        songids.append(element['Track ID'])
    assert all(isinstance(trackid, int) for trackid in songids)

    songs = []
    for trackid in songids:
        songs.append(ituneslib['Tracks'][str(trackid)])
    assert all(isinstance(song, dict) for song in songs)

    #Later in life, I'll use pyItunes' data cleaning code.

    return songs


#Loading Google Play Music Library
def gmusic_login():
    """
    Interactive login for gmusicapi
    :return: Returns a Mobileclient session
    """
    #What do I need to load gmusic?
    username = raw_input("Google Username: ")
    password = raw_input("Password (or app-specific password): ")
    session = gmusicapi.Mobileclient()
    login_result = session.login(username, password)
    if login_result:
        return session
    else:
        raise LoginError


class LoginError(Exception):
    """
    Exception for a bad Google login
    """
    pass


def gmusic_getsongs(session):
    """
    :param session: expects a Mobileclient login session.
    :return: Returns a dict of songs
    """
    songs = session.get_all_songs()
    #Catch the NotLoggedIn exception
    #Check if I have to do any data cleaning
    #something I noticed, only songs that are from Google will have a trackType
    return songs


#match iTunes songs to GPM songs
def match_songs(itsongs, gmsongs, exactmatch=True, tolerance=2):
    """
    :param itsongs: A list of dicts of songs from iTunes
    :param gmsongs: A list of dicts of songs from Google Play Music
    :param exactmatch: Whether
    :param tolerance:
    :return: A dict of matches, close matches, and mismatches. Each a list of tuples.
    """
    #tolerance is the Levenshtein distance between 2 possible track names
    #runtime is O(mn), should I worry about performance? We'll see later!
    #^  Note to self: Look up Levenshtein Automata later. O(n)
    #PS: don't expect these defaults to last until I say it's okay.

    pass


#Updating Play Counts
#2 ways - Either Applescript (mac only!) or spitting out a new XML file.
def update_itunes_playcount():
    pass

if __name__ == "__main__":
    import sys
    import os.path

    args = sys.argv
    assert os.path.isfile(args[1])

    itunes_song_list = load_itunes(args[1])
    print(itunes_song_list[1])