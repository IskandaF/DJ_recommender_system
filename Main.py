#!/usr/bin/env python
# coding: utf-8

# In[8]:


#!/usr/bin/env python
# coding: utf-8

# In[1]:

CLIENT_ID="31fb73b2d6fe48178e624cfc0b53e487"
CLIENT_SECRET="7b12c66ffc5b4e5a85fc17ed8a62ac87"
import requests # note to self (Kami): HTTP library
from localvariables_iskander import path
import os # note to self (Kami): "OS module in python provides functions for interacting with the operating system"
import statistics
# These are my account's secret details. Please don't share it with anyone


# In[2]:
path="discodataset"

AUTH_URL = 'https://accounts.spotify.com/api/token'

# POST
auth_response = requests.post(AUTH_URL, {
    'grant_type': 'client_credentials',
    'client_id': CLIENT_ID,
    'client_secret': CLIENT_SECRET,
})


# In[3]:


auth_response_data = auth_response.json()

# save the access token
access_token = auth_response_data['access_token']



# In[4]:


headers = {
    'Authorization': 'Bearer {token}'.format(token=access_token)
}


# In[5]:


# Setting the local path for the music dataset, change this one to yours
# path="/Users/Kami/Downloads/Disco-Selection"


# In[6]:


import eyed3 # Library for reading the mp3 tags


discolist=os.listdir(path) # Looping over mp3 songs in data directory 
# (used to get the list of all files and directories in the specified directory)


def get_track_id(track):
    title=track.tag.title.replace(" ", "+")
    artists=track.tag.artist.replace(" ", "+")
    url="https://api.spotify.com/v1/search?q={}+{}&type=track&offset=0&limit=1".format(artists,title)
    page=requests.get(url,headers=headers)
    jsonpage=page.json()
    return(find_id(jsonpage))

def find_id(jsonpage):
    try:
        track_id=jsonpage["tracks"]["items"][0]["id"]
        return track_id
    except IndexError:
        return("No ID")


tracks_ids={} # Creating the dictionary for tracks Spotify ids
for i in discolist:
        print(i)
    
#     try:
        track=eyed3.load(str(path+"/"+i))
        tracks_ids[track.tag.title]=get_track_id(track)
        print("ID search completed for "+track.tag.title)
#     except AttributeError:
#         print("No ID for "+i)
#         continue


# In[7]:


# This is an example of extracting a feature for one audio. Just loop over the "tracks_ids" dictionary
BASE_URL = 'https://api.spotify.com/v1/'

# Track ID from the URI
track_id = '3tjFYV6RSFtuktYl3ZtYcq'

# actual GET request with proper header
r = requests.get(BASE_URL + 'audio-features/' + track_id, headers=headers)


# In[8]:


r = r.json()
r


# In[9]:


import pandas as pd


# In[10]:


track_features = []
for key,value in tracks_ids.items():
    track_features.append(requests.get(BASE_URL + 'audio-features/' + value, headers=headers).json())


# In[11]:


track_features_dict = {}
for d in track_features:
    for k, v in d.items():  
        track_features_dict.setdefault(k, []).append(v)


# In[12]:


df = pd.DataFrame.from_dict(track_features_dict)


# In[13]:


track_name = []
for key,value in tracks_ids.items():
    track_name.append(key)


# In[14]:


df.insert(0, 'Track', track_name)


# In[15]:


artist = []


# In[16]:


for i in range(len(discolist)):
    artist.append(discolist[i].replace('.',' -').split(' - ')[1])


# In[17]:


df.insert(1,'Artist',artist)


# In[6]:


tracks_energy={}

current_track= df.loc[df['Track'] == 'Shake Your Body (Down To The Ground)']
#current_track= df.loc[df['Track'] == 'Do the Damn Thang']


# Listing the features that we need
features=["danceability","energy","loudness","acousticness","tempo"]
# Setting the maximum difference barrier (not used yet)
difference=float(0.01)
features_difference=[]

# Function to find the tempo difference in percentage (usually it's best to not go over +-.8%)
def percentage_change(current_track,next_track):
    current_tempo=float(current_track["tempo"])
    next_tempo=float(next_track["tempo"])
    return(float(current_tempo-next_tempo)/next_tempo*100)

def return_next(trackname, dataframe):
    current_track=df.loc[df['Track'] == trackname]
    mean_difference=[]
#     Iterating over tracks to exctract features
    for index, row in df.iterrows():
        tracks_mean_difference=[]
#         Calculating feature difference between our track and current iteration's track
        for i in features:
                tracks_mean_difference.append(abs(float(current_track[i]-row[i])))
# adding mean difference to the general list
        mean_difference.append(((str(row["Track"]),str(row["Artist"]),statistics.mean(tracks_mean_difference)),("Tempo difference-",float(percentage_change(current_track,row)))))
#     Sort the list by the least mean difference. Doesn't sort properly :(
    print(mean_difference[1][0][2])
    return(sorted(mean_difference, key=lambda x: x[0][2]))


# print(features_difference)
return_next('Shake Your Body (Down To The Ground)',df)
        
#         print(row["Track"],float(current_track["danceability"]-row["danceability"]),row["energy"],row["key"],row["loudness"],row["mode"],row["speechiness"],row["loudness"],row["acousticness"],row["instrumentalness"],row["liveness"],row["valence"],row["tempo"])


