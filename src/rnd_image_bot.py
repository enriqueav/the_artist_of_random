"""
Twitter bot to post a random "art" at random time
between min_mins and max_mins minutes
"""
import time
import os
from random import randint
import tweepy
import randomgraph

# add your own credentials
CONSUMER_KEY = ''
CONSUMER_SECRET = ''
ACCESS_KEY = ''
ACCESS_SECRET = ''
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

min_mins = 10     # 10 minutes is the min wait time
max_mins = 60*4   # max wait time is 4 hours

tmp_file = "ri.png"

while True:
    randomgraph.image(tmp_file)
    api.update_with_media(tmp_file)
    wait_time = randint(min_mins, max_mins)
    print "Waiting " + str(wait_time) + " minutes"
    time.sleep(60 * wait_time)
    os.remove(tmp_file)
