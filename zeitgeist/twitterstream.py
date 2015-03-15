import oauth2 as oauth
import urllib2 as urllib
import sys
import zeitgeist.tweet_processor as processor
import zeitgeist.twitter_adaptor as adaptor

def parse_record(line):
    if line[0] != '{':
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

def fetch_samples(term):
  proc = processor.TweetProcessor()
  response = get_response(term)
  for line in response:
    record = parse_record(line.strip())
    if record:
        tweet, score = proc.process_tweet_line(record)
        print tweet
if __name__ == '__main__':
  fetch_samples(sys.argv[1])
