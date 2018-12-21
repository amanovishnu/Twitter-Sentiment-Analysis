import re
from FileOps import readAbbrFile, readStopwordsFile
from nltk.stem import WordNetLemmatizer as wnl
from nltk.tokenize import word_tokenize
import string

exclude = set(string.punctuation)
stopwordsFile = '../data/stopwords.txt'
abbrFile = '../data/abbr.txt'

stopwords = readStopwordsFile(stopwordsFile)
abbr_dict = readAbbrFile(abbrFile)
def clean_data(original_tweets):
    pos_tweets = []
    neg_tweets = []
    neu_tweets = []
    mix_tweets = []

    for tweet,sentiment in original_tweets:
        if sentiment == 0.0:
            neu_tweets.append((process_tweet(tweet),sentiment))
        elif sentiment == 2.0:
            mix_tweets.append((process_tweet(tweet),sentiment))
        elif sentiment == 1.0:
            pos_tweets.append((process_tweet(tweet),sentiment))
        elif sentiment == -1.0:
            neg_tweets.append((process_tweet(tweet),sentiment))
    return pos_tweets, neg_tweets, neu_tweets, mix_tweets

def process_tweet(tweet):
    tweet = re.sub('((www\.[\s]+)|(https?://[^\s]+))','',tweet)
    tweet = replaceTwoOrMore(tweet)
    tweet = re.sub('@[^\s]+','',tweet)
    tweet = re.sub(r'#([^\s]+)', r'\1', tweet)
    tweet = re.sub(r'\\xe2\\x80\\x99', "'", tweet)
    tweet = re.sub(r'(<e>|</e>|<a>|</a>|\n)', '', tweet)
    tweet = ''.join(ch for ch in tweet if ch not in exclude)
    tweet = re.sub(r'\d+','',tweet)
    tweet = re.sub(r"^[^a-zA-Z]+", ' ', tweet)
    tweet = re.sub('[\s]+', ' ', tweet)
    tweet = re.sub(r'\\[xa-z0-9.*]+', '', tweet)
    tweet = tweet.strip(' .')
    tweet = convertCamelCase(tweet)
    tweet = tweet.lower()
    tweet = tokenize_tweet(tweet)
    tweet = replaceAbbr(tweet)
    tweet = wordLemmatizer(tweet)
    tweet = removeStopWords(tweet, stopwords)
    tweet = list(set(tweet))
    return tweet

def removeStopWords(tweet, stopwords):
    tmp = []
    for i in tweet:
        if i not in stopwords:
            tmp.append(i)

    return tmp

def replaceTwoOrMore(s):
    
    pattern = re.compile(r"(.)\1{1,}", re.DOTALL) 
    return pattern.sub(r"\1\1", s)

def convertCamelCase(word):
    return re.sub("([a-z])([A-Z])","\g<1> \g<2>",word)


def is_ascii(self, word):
    return all(ord(c) < 128 for c in word)

def replaceAbbr(s):
    for word in s:
        if word.lower() in abbr_dict.keys():
            s = [abbr_dict[word.lower()] if word.lower() in abbr_dict.keys() else word for word in s]
    return s

def tokenize_tweet(tweet):
    return word_tokenize(tweet)

def wordLemmatizer(tweet_words):
    return [wnl().lemmatize(word) for word in tweet_words]
