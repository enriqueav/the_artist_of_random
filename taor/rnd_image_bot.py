"""
Twitter bot to post a random "art" at random time
between min_mins and max_mins minutes
"""
import sys
import time
import os
from random import randint
import tweepy
import randomgraph
import config

# add your own credentials
auth = tweepy.OAuthHandler(config.CONSUMER_KEY, config.CONSUMER_SECRET)
auth.set_access_token(config.ACCESS_KEY, config.ACCESS_SECRET)
api = tweepy.API(auth)


def twitter_bot(min_mins=30, max_mins=360, debug=False):
    print("Waiting time between %d and %d minutes" % (min_mins, max_mins))
    tmp_file = "ri.png"
    while True:
        randomgraph.image(tmp_file, debug=debug)
        api.update_with_media(tmp_file)
        wait_time = randint(min_mins, max_mins)
        print("Waiting %d minutes" % wait_time)
        time.sleep(60 * wait_time)
        os.remove(tmp_file)


if __name__ == "__main__":
    debug = False
    # check for correct argument size
    if len(sys.argv) > 3:
        print('\033[91m' + 'Argument Error!\nUsage: '
                           'python rnd_image_bot.py [min_wait_time] [max_wait_time]'
                           '\033[0m')
        exit(1)

    min_wait = None
    max_wait = None
    if len(sys.argv) == 3:
        min_wait = int(sys.argv[1])
        max_wait = int(sys.argv[2])
    twitter_bot(min_wait, max_wait, debug=debug)
