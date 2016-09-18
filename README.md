# zeitgeist

To get up and running with Zeitgeist Engine, create a file called twitter_account.ini in the zeitgeist directory and add the following lines:
(To set up a new twitter dev account, visit https://apps.twitter.com/ and create a new app)

```
[security]

api_key=<Your Twitter Account Info Here>

api_secret=<Your Twitter Account Info Here>

access_token_key=<Your Twitter Account Info Here>

access_token_secret=<Your Twitter Account Info Here>
```

To get a list of the top 10 most popular topics being talked about in a particular location, try
`python zeitgeist/trend_by_location.py 44418`

44418 is the woeid for London, you can try other locations by providing the woeid for that location
There's a list of them in the resources directory.
Read more about 'em here: https://developer.yahoo.com/geo/geoplanet/guide/concepts.html


