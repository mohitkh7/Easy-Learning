
#!/bin/bash
import requests


#Create credentials from Google API Console for Youtube Data API and replace in the below line.
# key = {YOUR API KEY}



# search_id = "Ys7-6_t7OEQ"

def retreivingYoutubeData(search_id,key):
    #URL to search through API.
    url = "https://www.googleapis.com/youtube/v3/videos?part=snippet%2C+statistics%2C+contentDetails&id="+ search_id +"&maxResults=50&key=" + key
    #Getting response from the API with desired Query
    response = requests.get(url)

    #Getting JSON from the response to extract data.
    json_response = response.json()

    items = json_response['items']
    contentDetails = items[0]["contentDetails"]
    snippet = items[0]['snippet']
    statistics = items[0]['statistics']
    m,s = contentDetails["duration"].replace("PT","").replace("S","").split("M")
    dur = int(s) + int(m)*60
    result = {
    	"published_at"	:	snippet["publishedAt"].replace("T"," ").replace("Z",""),
    	"title"			:	snippet['title'],
    	"description"	:	snippet['description'],
    	"thumbnail_url"	:	snippet['thumbnails']['high']['url'],
    	"duration"		:	dur,
    	"view_count"	:	int(statistics['viewCount']),
    	"like_count"	:	int(statistics['likeCount']),
    	"dislike_count"	:	int(statistics['dislikeCount']),
    	"comment_count"	:	int(statistics['commentCount'])}

    #returns a json with all the data needed.
    return result
