# The Artist of Random

This is the code behind the twitter-bot [@the_random_art](https://twitter.com/the_random_art).
Also, now featured on my [Medium story](https://medium.com/@monocasero/a-useless-twitter-bot-probably-boosted-my-career-72bb3cd91701).

![alt text](https://pbs.twimg.com/media/DL0UtCNWAAA9Qgc.jpg "Logo")

It includes the Python code to:

* Create a random image on a canvas, using [Pillow](https://python-pillow.org/)
* Send this as a Twitter status with media, using [Tweepy](https://github.com/tweepy/tweepy), at random times

![alt text](https://pbs.twimg.com/media/DL0LfzyWsAAQDcJ.jpg "Logo")

It does not include:

* The talent of a real Artist

### What's new in version 1.2: *2018-09-11*

* Pick a random aspect ratio, 1:1, 4:3, 19:6
* Use of alpha channel to *possibly* create opaque shapes
* Optional mirroring effects, vertical, horizontal or both
* New file `src/tester.py` to launch images and automatically open them
* Tuned the probabilities of several parameters and numbers

## How to clone and install

Clone the repository

```sh
git clone https://github.com/enriqueav/the_artist_of_random.git
cd the_artist_of_random
```

You might need to install Pillow, Tweepy and numpy first

```sh
pip install tweepy
pip install Pillow
pip install numpy
```

## Generate images locally

To create an image and immediately show it:

```bash
$ python src/tester.py 
```

To run it in debug mode:

```bash
$ python src/tester.py --debug
Debug mode is ON
Selected values: 
colorset = color
use alpha = False
quantity of shapes = 4
size = 1024
aspect ratio = 1:1
mirroring axis 1 = 'h'
mirroring axis 2 = None
```

To save the image to a file

```bash
$ python src/tester.py /tmp/file.png --debug
Debug mode is ON
Selected values: 
colorset = gs
use alpha = False
quantity of shapes = 4
size = 128
aspect ratio = 4:3
mirroring axis 1 = 'h'
mirroring axis 2 = None
$ file /tmp/file.png 
/tmp/file.png: PNG image data, 128 x 96, 8-bit/color RGB, non-interlaced
```


## Run the Twitter bot and start publishing

To successfully publish the generated images to Twitter you need to modify `src/rnd_image_bot.py` to add your own Twitter keys and access tokens. Obtain them creating a new app at [https://apps.twitter.com/app/new](https://apps.twitter.com/app/new)):

```python
CONSUMER_KEY = ''     # your key here
CONSUMER_SECRET = ''  # your secret here
ACCESS_KEY = ''       # your key here
ACCESS_SECRET = ''    # your secret here
```

After setting the keys you can start the process with this command:

```sh
$ python src/rnd_image_bot.py
```

The waiting time between each published image is also calculated randomly. You can specify the minimum and the maximum waiting time (in minutes) using the command line arguments:

```bash
$ python src/rnd_image_bot.py 10 200
Waiting time between 10 and 200 minutes
```

## How to deploy to Heroku

**TO DO**
