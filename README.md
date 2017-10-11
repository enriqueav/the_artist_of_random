# The Artist of Random

This is the code behind the twitter-bot [@the_random_art](https://twitter.com/the_random_art).

**It should be executed with Python2**

![alt text](https://pbs.twimg.com/media/DL0UtCNWAAA9Qgc.jpg "Logo")

It includes the Python code to:

* Create a random image on a canvas, using [Pillow](https://python-pillow.org/)
* Send this as a Twitter status with media, using [Tweepy](https://github.com/tweepy/tweepy), at random times

![alt text](https://pbs.twimg.com/media/DL0LfzyWsAAQDcJ.jpg "Logo")

It does not include:

* The talent of a real Artist

## How to run

Clone the repository

```sh
git clone https://github.com/enriqueav/the_artist_of_random.git
cd the_artist_of_random.git
```

Modify src/rnd_image_bot.py to add your own Twitter credentials (obtain them at [https://apps.twitter.com/app/new](https://apps.twitter.com/app/new)):

```python
CONSUMER_KEY = ''     # your key here
CONSUMER_SECRET = ''  # your secret here
ACCESS_KEY = ''       # your key here
ACCESS_SECRET = ''    # your secret here
```

You might need to install Pillow, Tweepy and numpy first

```sh
pip install tweepy
pip install Pillow
pip install numpy
```

Finally, to run it

```sh
python src/rnd_image_bot.py
```

## How to deploy to Heroku

**TO DO**
