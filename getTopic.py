import pandas as pd
from datetime import datetime
import json
import tweepy
from parse_raw_tweet import parse_raw_tweet
import base64
import yaml
import time


from Helper import Helper
from Tweet import Tweet
import re

# CONSUMER_KEY = st.secrets['CONSUMER_KEY']
# CONSUMER_SECRET = st.secrets['CONSUMER_SECRET']
# ACCESS_TOKEN = st.secrets['ACCESS_TOKEN']
# ACCESS_SECRET = st.secrets['ACCESS_SECRET']

CONSUMER_KEY = 'NklB4SGVsSjpXLYWVn6lXxd7U'
CONSUMER_SECRET = 'rUMAU5dIpIRTImwIBNfgxxYWwP7Y2pkgjB3X36J7JkjkfLIkMu'
ACCESS_TOKEN = '1440879620971184129-HyGEUpcpEdHedXusFfaxRZ0NlyD1hA' #Authorization: Bearer
ACCESS_SECRET = 'OIwnv2pjyT9qjgFU1PnpUIbSSWittZFnoGMojUDNAz58B'
# Bearer: AAAAAAAAAAAAAAAAAAAAADU8UAEAAAAAGVXvwcwh%2BgCv%2FFhm7rDZgdmUv4k%3DeCwAbKOPDfhNcYENvdv4B8B9nGTR2Xje6whEqCOPEI8bpks4vn
def read_config():

	## authenticate
	auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
	auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
	api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, compression=True)


	return api

def df2tweet (d):
	tweet_template = {'created_at': datetime.strptime(d['tweet_time'],'%Y-%m-%d %H:%M:%S').strftime('%a %b %d %H:%M:%S +0000 %Y'),
					  'id': d['tweetid'],
					  'id_str': str(d['tweetid']),
					  'full_text': d['tweet_text'],
					  'truncated': False,
					  'display_text_range': [0, len(d['tweet_text'])],
					  'entities': {'hashtags': getArray(d['hashtags'],True),
								   'symbols': [],
								   'user_mentions': [],#getArray(d['user_mentions']),
								   'urls': None
								   },
					  'source': '<a href="https://mobile.twitter.com" rel="nofollow">Twitter Web App</a>',
					  'in_reply_to_status_id': d['in_reply_to_tweetid'],
					  'in_reply_to_status_id_str': str(d['in_reply_to_tweetid']),
					  'in_reply_to_user_id': d['in_reply_to_userid'],
					  'in_reply_to_user_id_str': str(d['in_reply_to_userid']),
					  # 'in_reply_to_screen_name': 'Quicktake',
					  'user': {'id': d['userid'],
							   'id_str': str(d['userid']),
							   'name': d['user_display_name'],
							   'screen_name': d['user_screen_name'],
							   'location': d['user_reported_location'],
							   'description': d['user_profile_description'],
							   'url': d['user_profile_url'],
							   # 'entities': {'url': {'urls': []},
							   #  'description': {'urls': []}},
							   # 'entities': {'url': {'urls': [{'url': 'https://t.co/ugp6buImQl',
							   #     'expanded_url': 'http://bloomberg.com/quicktake',
							   #     'display_url': 'bloomberg.com/quicktake',
							   #     'indices': [0, 23]}]},
							   #  'description': {'urls': []}},
							   'protected': False,
							   'followers_count': d['follower_count'],
							   'friends_count': d['following_count'],
							   # 'listed_count': 8732,
							   'created_at': d['account_creation_date'],
							   # 'favourites_count': 1606,
							   # 'utc_offset': None,
							   # 'time_zone': None,
							   # 'geo_enabled': True,
							   # 'verified': True,
							   # 'statuses_count': 226211,
							   'lang': d['account_language'],
							   # 'contributors_enabled': False,
							   # 'is_translator': False,
							   # 'is_translation_enabled': False,
							   # 'profile_background_color': 'C0DEED',
							   # 'profile_background_image_url': 'http://abs.twimg.com/images/themes/theme1/bg.png',
							   # 'profile_background_image_url_https': 'https://abs.twimg.com/images/themes/theme1/bg.png',
							   # 'profile_background_tile': False,
							   # 'profile_image_url': 'http://pbs.twimg.com/profile_images/1325664416558354434/FLlKusI3_normal.png',
							   # 'profile_image_url_https': 'https://pbs.twimg.com/profile_images/1325664416558354434/FLlKusI3_normal.png',
							   # 'profile_banner_url': 'https://pbs.twimg.com/profile_banners/252751061/1604898002',
							   # 'profile_link_color': '7FDBB6',
							   # 'profile_sidebar_border_color': 'C0DEED',
							   # 'profile_sidebar_fill_color': 'DDEEF6',
							   # 'profile_text_color': '333333',
							   # 'profile_use_background_image': True,
							   # 'has_extended_profile': False,
							   # 'default_profile': False,
							   # 'default_profile_image': False,
							   # 'following': False,
							   # 'follow_request_sent': False,
							   # 'notifications': False,
							   # 'translator_type': 'none',
							   # 'withheld_in_countries': []
							   },
					  'geo': None,
					  'coordinates': None,
					  'place': None,
					  'contributors': None,
					  # 'is_quote_status': True,
					  # 'quoted_status_id': 1392535793038671872,
					  # 'quoted_status_id_str': '1392535793038671872',
					  # 'quoted_status_permalink': {'url': 'https://t.co/KKcWkUW0Zh',
					  #  'expanded': 'https://twitter.com/Quicktake/status/1392535793038671872',
					  #  'display': 'twitter.com/Quicktake/stat…'},
					  # 'quoted_status': {'created_at': 'Wed May 12 17:42:59 +0000 2021',
					  #  'id': 1392535793038671872,
					  #  'id_str': '1392535793038671872',
					  #  'full_text': 'DarkSide, the Russia-linked ransomware group connected to the Colonial pipeline shutdown, has made millions of dollars providing hacking tools and services to others in the world of cybercrime. https://t.co/VC5pWhFSy4\n\n@asebenius explains👇 https://t.co/B0061fec8e',
					  #  'truncated': False,
					  #  'display_text_range': [0, 239],
					  #  'entities': {'hashtags': [],
					  #   'symbols': [],
					  #   'user_mentions': [{'screen_name': 'asebenius',
					  #     'name': 'Alyza Sebenius',
					  #     'id': 1106223019,
					  #     'id_str': '1106223019',
					  #     'indices': [219, 229]}],
					  #   'urls': [{'url': 'https://t.co/VC5pWhFSy4',
					  #     'expanded_url': 'https://trib.al/rTtkRLS',
					  #     'display_url': 'trib.al/rTtkRLS',
					  #     'indices': [194, 217]}],
					  #   'media': [{'id': 1392535526868197383,
					  #     'id_str': '1392535526868197383',
					  #     'indices': [240, 263],
					  #     'media_url': 'http://pbs.twimg.com/amplify_video_thumb/1392535526868197383/img/8cXWddjiQcx9d4IC.jpg',
					  #     'media_url_https': 'https://pbs.twimg.com/amplify_video_thumb/1392535526868197383/img/8cXWddjiQcx9d4IC.jpg',
					  #     'url': 'https://t.co/B0061fec8e',
					  #     'display_url': 'pic.twitter.com/B0061fec8e',
					  #     'expanded_url': 'https://twitter.com/Quicktake/status/1392535793038671872/video/1',
					  #     'type': 'photo',
					  #     'sizes': {'thumb': {'w': 150, 'h': 150, 'resize': 'crop'},
					  #      'medium': {'w': 1200, 'h': 675, 'resize': 'fit'},
					  #      'small': {'w': 680, 'h': 383, 'resize': 'fit'},
					  #      'large': {'w': 1280, 'h': 720, 'resize': 'fit'}}}]},
					  #  'extended_entities': {'media': [{'id': 1392535526868197383,
					  #     'id_str': '1392535526868197383',
					  #     'indices': [240, 263],
					  #     'media_url': 'http://pbs.twimg.com/amplify_video_thumb/1392535526868197383/img/8cXWddjiQcx9d4IC.jpg',
					  #     'media_url_https': 'https://pbs.twimg.com/amplify_video_thumb/1392535526868197383/img/8cXWddjiQcx9d4IC.jpg',
					  #     'url': 'https://t.co/B0061fec8e',
					  #     'display_url': 'pic.twitter.com/B0061fec8e',
					  #     'expanded_url': 'https://twitter.com/Quicktake/status/1392535793038671872/video/1',
					  #     'type': 'video',
					  #     'sizes': {'thumb': {'w': 150, 'h': 150, 'resize': 'crop'},
					  #      'medium': {'w': 1200, 'h': 675, 'resize': 'fit'},
					  #      'small': {'w': 680, 'h': 383, 'resize': 'fit'},
					  #      'large': {'w': 1280, 'h': 720, 'resize': 'fit'}},
					  #     'video_info': {'aspect_ratio': [16, 9],
					  #      'duration_millis': 84851,
					  #      'variants': [{'bitrate': 288000,
					  #        'content_type': 'video/mp4',
					  #        'url': 'https://video.twimg.com/amplify_video/1392535526868197383/vid/480x270/rO_qjo2jLVFEXHJ8.mp4?tag=14'},
					  #       {'bitrate': 832000,
					  #        'content_type': 'video/mp4',
					  #        'url': 'https://video.twimg.com/amplify_video/1392535526868197383/vid/640x360/g4PQ15UN8nNKZaVL.mp4?tag=14'},
					  #       {'bitrate': 2176000,
					  #        'content_type': 'video/mp4',
					  #        'url': 'https://video.twimg.com/amplify_video/1392535526868197383/vid/1280x720/0wzxgpF72i5_o54K.mp4?tag=14'},
					  #       {'content_type': 'application/x-mpegURL',
					  #        'url': 'https://video.twimg.com/amplify_video/1392535526868197383/pl/Z3lnuZPeeKmQbNs9.m3u8?tag=14'}]},
					  #     'additional_media_info': {'monetizable': False}}]},
					  #  'source': '<a href="http://www.socialflow.com" rel="nofollow">SocialFlow</a>',
					  #  'in_reply_to_status_id': None,
					  #  'in_reply_to_status_id_str': None,
					  #  'in_reply_to_user_id': None,
					  #  'in_reply_to_user_id_str': None,
					  #  'in_reply_to_screen_name': None,
					  #  'user': {'id': 252751061,
					  #   'id_str': '252751061',
					  #   'name': 'Bloomberg Quicktake',
					  #   'screen_name': 'Quicktake',
					  #   'location': '',
					  #   'description': 'Live global news and original shows. \nStreaming free, 24/7.',
					  #   'url': 'https://t.co/ugp6buImQl',
					  #   'entities': {'url': {'urls': [{'url': 'https://t.co/ugp6buImQl',
					  #       'expanded_url': 'http://bloomberg.com/quicktake',
					  #       'display_url': 'bloomberg.com/quicktake',
					  #       'indices': [0, 23]}]},
					  #    'description': {'urls': []}},
					  #   'protected': False,
					  #   'followers_count': 1254382,
					  #   'friends_count': 1519,
					  #   'listed_count': 8732,
					  #   'created_at': 'Tue Feb 15 20:50:58 +0000 2011',
					  #   'favourites_count': 1606,
					  #   'utc_offset': None,
					  #   'time_zone': None,
					  #   'geo_enabled': True,
					  #   'verified': True,
					  #   'statuses_count': 226211,
					  #   'lang': None,
					  #   'contributors_enabled': False,
					  #   'is_translator': False,
					  #   'is_translation_enabled': False,
					  #   'profile_background_color': 'C0DEED',
					  #   'profile_background_image_url': 'http://abs.twimg.com/images/themes/theme1/bg.png',
					  #   'profile_background_image_url_https': 'https://abs.twimg.com/images/themes/theme1/bg.png',
					  #   'profile_background_tile': False,
					  #   'profile_image_url': 'http://pbs.twimg.com/profile_images/1325664416558354434/FLlKusI3_normal.png',
					  #   'profile_image_url_https': 'https://pbs.twimg.com/profile_images/1325664416558354434/FLlKusI3_normal.png',
					  #   'profile_banner_url': 'https://pbs.twimg.com/profile_banners/252751061/1604898002',
					  #   'profile_link_color': '7FDBB6',
					  #   'profile_sidebar_border_color': 'C0DEED',
					  #   'profile_sidebar_fill_color': 'DDEEF6',
					  #   'profile_text_color': '333333',
					  #   'profile_use_background_image': True,
					  #   'has_extended_profile': False,
					  #   'default_profile': False,
					  #   'default_profile_image': False,
					  #   'following': False,
					  #   'follow_request_sent': False,
					  #   'notifications': False,
					  #   'translator_type': 'none',
					  #   'withheld_in_countries': []},
					  #  'geo': None,
					  #  'coordinates': None,
					  #  'place': None,
					  #  'contributors': None,
					  #  'is_quote_status': False,
					  #  'retweet_count': 160,
					  #  'favorite_count': 244,
					  #  'favorited': False,
					  #  'retweeted': False,
					  #  'possibly_sensitive': False,
					  #  'possibly_sensitive_appealable': False,
					  #  'lang': 'en'},
					  'retweet_count': d['retweet_count'],
					  'favorite_count': d['like_count'],
					  # 'favorited': False,
					  'retweeted': False,
					  'possibly_sensitive': False,
					  'possibly_sensitive_appealable': False,
					  'lang': d['tweet_language']}

	return tweet_template

def getArray(d,object=False):
	if( (not isinstance(d,str)) or (d=='[]')):
		if object:
			return [];
		else:
			return None
	else:
		h = d.replace('[', '').replace(']', '').split(',');
		if(object):
			return [{"text":t} for t in h]
		else:
			return h

def getTopic (tweet_url,_raw_tweet):
	if(tweet_url):
		api = read_config();
		id_of_tweet = tweet_url.split("/")[-1]
		try:
			raw_tweet = api.get_status(id_of_tweet, tweet_mode="extended")._json
		except:
			if(_raw_tweet):
				raw_tweet = _raw_tweet
			else:
				raw_tweet = None
		if raw_tweet:
			top_n_topics_df, keywords_appearing_df = handleData(raw_tweet)
		return top_n_topics_df,keywords_appearing_df
	else:
		raw_tweet = _raw_tweet
		if raw_tweet:
			top_n_topics_df, keywords_appearing_df = handleData(raw_tweet)
		return top_n_topics_df,keywords_appearing_df
def getTopicv2 (raw_tweet):
	if raw_tweet:
		top_n_topics_df, keywords_appearing_df = handleData(raw_tweet)
	return top_n_topics_df,keywords_appearing_df


def handleData(raw_tweet):
	tweet = parse_raw_tweet(raw_tweet)
	data = tweet.data
	# df = pd.DataFrame([data], columns=data.keys())

	data['Date'] = data['Date']
	data['Time'] = data['Time'] + " UTC"

	top_n_topics_df, keywords_appearing_df = tweet.get_top_n_topics()

	return top_n_topics_df, keywords_appearing_df

