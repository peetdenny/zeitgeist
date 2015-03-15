import oauth2 as oauth
import urllib2 as urllib
import sys
import time
import zeitgeist.tweet_processor as processor
import zeitgeist.twitter_adaptor as adaptor
from pymongo import MongoClient

last_metric_timestamp=0;
client = MongoClient()
db = client['zeitgeist']
share_price =  db['share_price']
obama_sp = share_price['obama']
proc = processor.TweetProcessor()

def write_to_db(time, price):
    prices = obama_sp.prices
    price={"timestamp": time, "price":price}
    prices.insert(price)


def parse_record(line):
    if len(line)<1 or line[0] != '{':
        return None

    if line[2:8] == 'delete':
        return None

    return line

def get_response(term):
    #url = "https://stream.twitter.com/1.1/statuses/sample.json"
    url ="https://stream.twitter.com/1.1/statuses/filter.json"
    parameters = {'track':term}#{'locations':'-0.49,51.28,0.24,51.69'}
    response = adaptor.twitter_req(url, "POST", parameters)
    return response


def output_score(t, total_score):
    global last_metric_timestamp
    if (last_metric_timestamp + 60 < t):
        write_to_db(t, total_score)
        last_metric_timestamp = t


def get_most_recent_score():
    return db.share_price.obama.prices.find().sort("timestamp",-1).limit(1)[0]['price']


def fetch_samples(term):
  response = get_response(term)
  total_score=get_most_recent_score()
  for line in response:
    record = parse_record(line.strip())
    if record:
        tweet, score = proc.process_tweet_line(record)
        total_score+=score
        t=long(time.time())
        output_score(t, total_score)

if __name__ == '__main__':
    while(True):
        fetch_samples(sys.argv[1])
        print 'reconnecting...'
