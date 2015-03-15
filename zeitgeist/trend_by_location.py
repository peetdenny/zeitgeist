import zeitgeist.twitter_adaptor as adaptor
import zeitgeist.tweet_processor as processor
import sys


def get_trends_response(woeid):
    url = "https://api.twitter.com/1.1/trends/place.json"
    parameters = {'id':woeid, 'exclude':'hashtags'}
    response = adaptor.twitter_req(url, "GET", parameters)
    return response

def fetch_samples(woeid):

  proc = processor.TweetProcessor()
  response = get_trends_response(woeid)
  for line in response:
      proc.process_trend_line(line)

if __name__ == '__main__':
  if len(sys.argv)<2:
      print 'please provide a location WOEID. E.g. \nLondon: 44418\nParis: 615702\nAfrica: 10\nBrazil: 9\nVladivostok: 1'
      sys.exit(0)
  woeid= int(sys.argv[1])
  fetch_samples(woeid)
