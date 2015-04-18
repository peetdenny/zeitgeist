import oauth2 as oauth
import urllib2 as urllib
from retrying import retry
import ConfigParser
Config = ConfigParser.ConfigParser()
Config.read('zeitgeist/twitter_account.ini')
print Config.sections()

api_key = Config.get('security','api_key')
api_secret = Config.get('security','api_secret')
access_token_key = Config.get('security','access_token_key')
access_token_secret = Config.get('security','access_token_secret')

_debug = 0

oauth_token = oauth.Token(key=access_token_key, secret=access_token_secret)
oauth_consumer = oauth.Consumer(key=api_key, secret=api_secret)

signature_method_hmac_sha1 = oauth.SignatureMethod_HMAC_SHA1()

http_method = "GET"
http_handler  = urllib.HTTPHandler(debuglevel=_debug)
https_handler = urllib.HTTPSHandler(debuglevel=_debug)

'''
Construct, sign, and open a twitter request
using the hard-coded credentials above.
'''
@retry(wait_exponential_multiplier=10000, wait_exponential_max=1800000)
def twitter_req(url, method, parameters):
    req = oauth.Request.from_consumer_and_token(oauth_consumer,
                                                token=oauth_token,
                                                http_method=http_method,
                                                http_url=url,
                                                parameters=parameters)

    req.sign_request(signature_method_hmac_sha1, oauth_consumer, oauth_token)
    headers = req.to_header()

    if http_method == "POST":
        encoded_post_data = req.to_postdata()
    else:
        encoded_post_data = None
        url = req.to_url()

    opener = urllib.OpenerDirector()
    opener.add_handler(http_handler)
    opener.add_handler(https_handler)

    response = opener.open(url, encoded_post_data)
    print response.info()

    return response
