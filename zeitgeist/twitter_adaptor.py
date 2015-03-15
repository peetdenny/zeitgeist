import oauth2 as oauth
import urllib2 as urllib
from retrying import retry

api_key = "RIPFFvW915REqc5j04Hzx0w0g"
api_secret = "CyKuILWH6PbikpeoDHMf9NAgCWa3zGbhijYjXwsqsDqxlY2zdj"
access_token_key = "529239260-ak0udIH3cNI1AtZbc0AImzYIoq2CQI0TT2zeXe0k"
access_token_secret = "gmcZAKLLpxa4TbejBCGS0WMxJcfjt1OWhi8Z7noQQOQzQ"

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
