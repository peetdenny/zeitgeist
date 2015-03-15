import zeitgeist.twitter_adaptor as adaptor
import zeitgeist.tweet_processor as processor
import sys
import json


def get_trends_response():
    url = "https://api.twitter.com/1.1/trends/available.json"
    parameters = {}
    response = adaptor.twitter_req(url, "GET", parameters)
    return response

def fetch_samples():
  proc = processor.TweetProcessor()
  response = get_trends_response()
  for line in response:
      objs = json.loads(line);
      for obj in objs:
        print obj['country'],':',obj['woeid']
if __name__ == '__main__':

  fetch_samples()
