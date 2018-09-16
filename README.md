# The Artist of Random V2.0

This is the code behind the twitter-bot [@the_random_art](https://twitter.com/the_random_art).
Also, now featured on my [Medium story](https://medium.com/@monocasero/a-useless-twitter-bot-probably-boosted-my-career-72bb3cd91701).

![alt text](https://pbs.twimg.com/media/DnM9a4lU0AALj19.jpg "Logo")

It includes the Python code to:

* Create a random image on a canvas, using [Pillow](https://python-pillow.org/)
* Send this as a Twitter status with media, using [Tweepy](https://github.com/tweepy/tweepy), at random times

![alt text](https://pbs.twimg.com/media/DnMfTiBX0AYc_e8.jpg "Logo")

It does not include:

* The talent of a real Artist

### What's new in version 2.0: *2018-09-16* 🇲🇽

* The random artist has evolved into a different beast.
* Use "Generators": lasso, explosion, grid, stain and worm
* Still using simple shapes as Rectangles and Circles but with lower probability.
* Not using Black and White or GrayScale color sets for now.

![alt text](https://pbs.twimg.com/profile_images/1040028651834630144/Tr9hkbGk_400x400.jpg "Logo")

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
$ python3 random_art.py 
```

To run it in debug mode:

```bash
$ python random_art.py --debug
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

There are several arguments you can pass to the command

```bash
$ python3 random_art.py -h
usage: random_art.py [-h] [-s SEED] [-i IMAGE_PATH] [-d] [-n]

Create a random image. By default is created in a tmp file and shown
inmediatly. It can also be stored to a path using -i <image_path>.png

optional arguments:
  -h, --help            show this help message and exit
  -s SEED, --seed SEED  Initialize numpy with a given seed. Same number will
                        always create the same image.
  -i IMAGE_PATH, --image_path IMAGE_PATH
                        Name of the file to create. Temporary file is used if
                        -i is not specified.
  -d, --debug           Enter DEBUG mode.
  -n, --dont_show       Do not open the image after creating it. Only makes
                        sense if -i is set.

```


## Run the Twitter bot and start publishing

To successfully publish the generated images to Twitter you need to modify `config.py` to add your own Twitter keys and access tokens. Obtain them creating a new app at [https://apps.twitter.com/app/new](https://apps.twitter.com/app/new)):

```python
CONSUMER_KEY = ''     # your key here
CONSUMER_SECRET = ''  # your secret here
ACCESS_KEY = ''       # your key here
ACCESS_SECRET = ''    # your secret here
```

After setting the keys you can start the process with this command. The waiting time between each published image is also calculated randomly. You can specify the minimum and the maximum waiting time (in minutes) using the command line arguments:

```bash
$ python3 twitter_bot.py 10 200
Waiting time between 10 and 200 minutes
```

## How to deploy to Heroku

**TO DO**
