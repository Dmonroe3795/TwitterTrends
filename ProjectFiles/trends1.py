"""Visualizing Twitter Sentiment Across America
     For CSCI 203 Final Project, Spring 2015"""

from data import word_sentiments, load_tweets
from datetime import datetime
from doctest import run_docstring_examples
from geo import us_states, geo_distance, make_position, longitude, latitude
from string import ascii_letters
from ucb import main, trace, interact, log_current_line
import re

def extract_words(text):
    """Return the words in a tweet, not including punctuation.
    needs import re
    """
    tweetWords = re.split('\W',text)
    tweetWords = [x for x in tweetWords if x != '']
    return tweetWords #Don't use text.split()

def analyze_tweet_sentiment(tweet):
    """ Return a sentiment representing the degree of positive or negative
    sentiment in the given tweet, averaging over all the words in the tweet
    that have a sentiment value.

    If no words in the tweet have a sentiment value, return
    make_sentiment(None).
    """
    sentiment = 0
    wordCount = 0
    tweetWords = extract_words(tweet["text"])
    for tWord in tweetWords:
        s = get_word_sentiment(tWord)
        if s == None:
            s = 0
        sentiment += s
        wordCount += 1
    average_tweet = sentiment/wordCount
    return average_tweet

def find_closest_state(tweet, state_centers):
    
    """Return the name of the state closest to the given tweet's location.

    Use the geo_distance function (already provided) to calculate distance
    in miles between two latitude-longitude positions.

    Arguments:
    tweet -- a tweet abstract data type
    state_centers -- a dictionary from state names to positions.

    """
    stateCode = None
    stateDistance = geo_distance(tweet_location(tweet),state_centers["OR"])
    for key, value in state_centers:
        if geo_distance(tweet_location(tweet),value) <= stateDistance:
            stateCode = key
    
    return stateCode   

def group_tweets_by_state(tweets):
    """Return a dictionary that aggregates tweets by their nearest state center.

    The keys of the returned dictionary are state names, and the values are
    lists of tweets that appear closer to that state center than any other.

    tweets -- a sequence of tweet abstract data types

    """
            
    return tweets_by_state

def average_sentiments(tweets_by_state):
    """Calculate the average sentiment of the states by averaging over all
    the tweets from each state. Return the result as a dictionary from state
    names to a list of two numbers - average sentiment values and number of tweets.

    If a state has no tweets with sentiment values, leave it out of the
    dictionary entirely.  Do NOT include states with no tweets, or with tweets
    that have no sentiment, as 0.  0 represents neutral sentiment, not unknown
    sentiment.

    tweets_by_state -- A dictionary from state names to lists of tweets
   
    """
      
        
    return averaged_state_sentiments


def ExportToCSV(term=""):
    """ Create a vPython Graph of the tweets in the US by state, for a given
        subject denoted by "term".

        input 'term': the word to analyze tweet sentiment for.

        returns: Will create a vPython histogram of the sentiments and 
                 frequency of tweets containing 'term' organized by state.
    """

    if term == "":
        term = input("Enter a term to be graphed by sentiment.\n\n\t>")

    tweets = load_tweets(make_tweet, term)
    tweetDict = group_tweets_by_state(tweets)
    sentDict = average_sentiments(tweetDict)
    # Your code to export sentDict to .CSV file

    
#----------------------------------------------------------------------#
#----------------------------------------------------------------------#
#------      You shouldn't change anything beyond this line!     ------#
#----------------------------------------------------------------------#
#----------------------------------------------------------------------#

# tweet ADT

def make_tweet(text, time, lat, lon):
    """Return a tweet, represented as a python dictionary.

    text  -- A string; the text of the tweet, all in lowercase
    time  -- A datetime object; the time that the tweet was posted
    lat   -- A number; the latitude of the tweet's location
    lon   -- A number; the longitude of the tweet's location

    >>> t = make_tweet("just ate lunch", datetime(2012, 9, 24, 13), 38, 74)
    >>> tweet_words(t)
    ['just', 'ate', 'lunch']
    >>> tweet_time(t)
    datetime.datetime(2012, 9, 24, 13, 0)
    >>> p = tweet_location(t)
    >>> latitude(p)
    38
    """
    return {'text': text, 'time': time, 'latitude': lat, 'longitude': lon}

def tweet_words(tweet):
    """Return a list of the words in the text of a tweet."""

    return tweet['text'].split()

def tweet_time(tweet):
    """Return the datetime that represents when the tweet was posted."""

    return tweet['time']

def tweet_location(tweet):
    """Return a position (see geo.py) that represents the tweet's location."""

    return make_position(tweet['latitude'], tweet['longitude'])

def tweet_string(tweet):
    """Return a string representing the tweet."""
    
    return '"{0}" @ {1}'.format(tweet['text'], tweet_location(tweet))

# sentiment ADT

def make_sentiment(value):
    """Return a sentiment, which represents a value that may not exist.

    >>> positive = make_sentiment(0.2)
    >>> neutral = make_sentiment(0)
    >>> unknown = make_sentiment(None)
    >>> has_sentiment(positive)
    True
    >>> has_sentiment(neutral)
    True
    >>> has_sentiment(unknown)
    False
    >>> sentiment_value(positive)
    0.2
    >>> sentiment_value(neutral)
    0
    """
    assert value is None or (value >= -1 and value <= 1), 'Illegal value'

    if value == None:
        return None
    else:
        return value
    
def has_sentiment(s):
    """Return whether sentiment s has a value."""

    if s == None:
        return False
    else:
        return True
    
def sentiment_value(s):
    """Return the value of a sentiment s."""
    assert has_sentiment(s), 'No sentiment value'

    return s

def get_word_sentiment(word):
    """Return a sentiment representing the degree of positive or negative
    feeling in the given word.

    >>> sentiment_value(get_word_sentiment('good'))
    0.875
    >>> sentiment_value(get_word_sentiment('bad'))
    -0.625
    >>> sentiment_value(get_word_sentiment('winning'))
    0.5
    >>> has_sentiment(get_word_sentiment('Berkeley'))
    False
    """
    # Learn more: http://docs.python.org/3/library/stdtypes.html#dict.get
    return make_sentiment(word_sentiments.get(word))

# Find center position of a state

def find_centroid(polygon):
    """Find the centroid of a polygon.

    http://en.wikipedia.org/wiki/Centroid#Centroid_of_polygon

    polygon -- A list of positions, in which the first and last are the same

    Returns: 3 numbers; centroid latitude, centroid longitude, and polygon area

    Hint: If a polygon has 0 area, use the latitude and longitude of its first
    position as its centroid.

    >>> p1, p2, p3 = make_position(1, 2), make_position(3, 4), make_position(5, 0)
    >>> triangle = [p1, p2, p3, p1]  # First vertex is also the last vertex
    >>> find_centroid(triangle)
    (3.0, 2.0, 6.0)
    >>> find_centroid([p1, p3, p2, p1])
    (3.0, 2.0, 6.0)
    >>> tuple(map(float, find_centroid([p1, p2, p1])))  # A zero-area polygon
    (1.0, 2.0, 0.0)
    """

    # polygon is list of positions.  position[0] is latitude, postion[1] is longitude
    results = []
          
    b = polygon
    cx = cy = a = 0
    for k in range(len(polygon)):
       # consider point k and the one before it (knowing that -1 maps to last point)
       temp = (b[k-1][1] * b[k][0] - b[k][1] * b[k-1][0])
       a += temp
       cx += temp * (b[k-1][1] + b[k][1]) 
       cy += temp * (b[k-1][0] + b[k][0])
    if a != 0:
       a *= 0.5
       cx /= (6*a)
       cy /= (6*a)
       a = abs(a)
       results.append( (cy,cx,a) )
    else:
       results.append( (b[0][0], b[0][1], 0) )
    return results

def find_center(polygons):
    """Compute the geographic center of a state, averaged over its polygons.

    The center is the average position of centroids of the polygons in polygons,
    weighted by the area of those polygons.

    Arguments:
    polygons -- a list of polygons

    >>> ca = find_center(us_states['CA'])  # California
    >>> round(latitude(ca), 5)
    37.25389
    >>> round(longitude(ca), 5)
    -119.61439

    >>> hi = find_center(us_states['HI'])  # Hawaii
    >>> round(latitude(hi), 5)
    20.1489
    >>> round(longitude(hi), 5)
    -156.21763
    """
 
    if len(polygons) > 1:
        # For states that have two or more pieces, we compute
        # a composite centroid as a weighted average

        results = []
        for k in range(len(polygons)):
             results += find_centroid(polygons[k])    
        # print(results)
        
        cy = sum( results[k][0]*results[k][2]  for k in range(len(results)) )
        cx = sum( results[k][1]*results[k][2]  for k in range(len(results)) )
        total = sum( entry[2] for entry in results )
        return (cy/total, cx/total)
    else:
        centroid = find_centroid(polygons[0])
        return (centroid[0][0], centroid[0][1])

def print_sentiment(text='Are you virtuous or verminous?'):
    """Print the words in text, annotated by their sentiment scores."""
    words = extract_words(text.lower())
    layout = '{0:>' + str(len(max(words, key=len))) + '}: {1:+}'
    for word in words:
        s = get_word_sentiment(word)
        if has_sentiment(s):
            print(layout.format(word, sentiment_value(s)))

