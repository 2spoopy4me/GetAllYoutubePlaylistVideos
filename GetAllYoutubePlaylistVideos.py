'''This program grabs all video titles+ids from a youtube playlist, inserts into db'''

import requests
import json
import sqlite3

def insert_into_db(dbName, videos):
	conn = sqlite3.connect(dbName)
	c = conn.cursor()
	# delete existing table, recreate it
	c.execute('DROP TABLE IF EXISTS youtube_videos') # (title TEXT, id TEXT)')
	c.execute('CREATE TABLE youtube_videos (title TEXT, id TEXT)')
	conn.commit()
	# insert videos
	for _ in videos:
		# remove qoutes that may cause and issue
		_['title'] = _['title'].replace('"', '')
		_['title'] = _['title'].replace("'", '')
		c.execute('INSERT INTO youtube_videos VALUES ("{}", "{}")'.format(_['title'], _['videoId']) )
		conn.commit()
	conn.close()

def get_all_playlist_videos(playListId, key, pageToken=None):
	'''Recursively grab all videos from playListId using API key'''
	if pageToken != None:
		url = "https://www.googleapis.com/youtube/v3/playlistItems?&pageToken="+pageToken+"&part=snippet&playlistId="+playListId+"&key="+key+"&maxResults=50";
  	else:
  		url = "https://www.googleapis.com/youtube/v3/playlistItems?&part=snippet&playlistId="+playListId+"&key="+key+"&maxResults=50";
  	response_json = requests.get(url).json()
	# list that will hold all titles and video IDs
	videos = []
	# for each item in response, add video and id to to videos list as a dict
  	for item in response_json['items']:
		print(item)
		videos.append( {'title':item['snippet']['title'].encode('utf-8'), 'videoId':item['snippet']['resourceId']['videoId']} )
	# if there is a nextPageToken token, call the function again and add results to current videos array
  	if response_json.get('nextPageToken') != None:
		new_videos = get_all_playlist_videos(playListId, key, response_json.get('nextPageToken'))
		for _ in new_videos:
			videos.append(_) #print(_)
  	else:
  		token = None
  	return videos




if __name__ == '__main__':
	my_videos = get_all_playlist_videos("playlistID here", "youtube API key here")
	print('# of videos Ive liked: {}'.format(len(my_videos)))
	insert_into_db('youtube.db', my_videos)
