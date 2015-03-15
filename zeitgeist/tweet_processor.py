import sys
import json

class TweetProcessor():
    terms = {}
    totalWords = float(0)

    scores = {}
    tweets = []
    sentiment_by_state = {}


    def calcScore(self, tweet):
        score = 0
        for word in tweet.split():
            word = word.lower()
            if word in self.scores:
                score += self.scores[word]
        return score


    def loadDictionary(self,fp):
        for line in fp:
            term, score = line.split("\t")
            self.scores[term] = int(score)


    def find_location(self, obj):
        if 'location' in obj['user']:
            location = obj['user']['location']
            return location
        else:
            return None

    def process_trend_line(self, line):
        objs = json.loads(line)
        for obj in objs:
            for trend in obj['trends']:
                print trend['name']

    def process_tweet_line(self,line):
        state = None
        obj = json.loads(line)
        if 'text' in obj:
            tweet = obj["text"]
            score = self.calcScore(tweet)
            state = self.find_location(obj)
            return [tweet, score]

    def __init__(self):
        sentiment_file = open('resources/AFINN-111.txt')
        self.loadDictionary(sentiment_file)
