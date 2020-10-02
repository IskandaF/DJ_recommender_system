#!/usr/bin/env python
# coding: utf-8

# In[3]:


import requests
import os
from requests_oauthlib import OAuth1
# These are my account's secret details. Please don't share it with anyone
CLIENT_ID="31fb73b2d6fe48178e624cfc0b53e487"
CLIENT_SECRET="7b12c66ffc5b4e5a85fc17ed8a62ac87"


# In[4]:


AUTH_URL = 'https://accounts.spotify.com/api/token'

# POST
auth_response = requests.post(AUTH_URL, {
    'grant_type': 'client_credentials',
    'client_id': CLIENT_ID,
    'client_secret': CLIENT_SECRET,
})


# In[5]:


auth_response_data = auth_response.json()

# save the access token
access_token = auth_response_data['access_token']


# In[6]:


headers = {
    'Authorization': 'Bearer {token}'.format(token=access_token)
}


# In[7]:


# Setting the local path for the music dataset, change this one to yours
path="/Users/soulist/Desktop/discodataset"


# In[15]:


import eyed3 # Library for reading the mp3 tags


discolist=os.listdir(path) # Looping over mp3 songs in data directory



def get_track_id(track):
    title=track.tag.title.replace(" ", "+")
    artists=track.tag.artist.replace(" ", "+")
    url="https://api.spotify.com/v1/search?q={}+{}&type=track&offset=0&limit=1".format(artists,title)
    page=requests.get(url,headers=headers)
    jsonpage=page.json()
    return(find_id(jsonpage))

def find_id(jsonpage):
    track_id=jsonpage["tracks"]["items"][0]["id"]
    return track_id


tracks_ids={} # Creating the dictionary for tracks Spotify ids
for i in discolist:
    track=eyed3.load(str(path+"/"+i))
    tracks_ids[track.tag.title]=get_track_id(track)
    print("ID search completed for "+track.tag.title)
    
    


# In[9]:


# This is an example of extracting a feature for one audio. Just loop over the "tracks_ids" dictionary
BASE_URL = 'https://api.spotify.com/v1/'

# Track ID from the URI
track_id = '3tjFYV6RSFtuktYl3ZtYcq'

# actual GET request with proper header
r = requests.get(BASE_URL + 'audio-features/' + track_id, headers=headers)


# In[10]:


r = r.json()
r


# In[ ]:




