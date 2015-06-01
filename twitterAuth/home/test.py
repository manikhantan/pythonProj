from twython import Twython
APP_KEY = 'cuXKU1S8RqSvYAd3oqlsOiVy8'
APP_SECRET = 'ep49dL3521Oka8CusLOlSHoSwAmfAc206wPbl0pVOjN7mG7p2G'

twitter = Twython(APP_KEY, APP_SECRET)
auth = twitter.get_authentication_tokens(callback_url='http://52.11.59.38/callback')

OAUTH_TOKEN = auth['oauth_token']
OAUTH_TOKEN_SECRET = auth['oauth_token_secret']

twitter = Twython(APP_KEY, APP_SECRET,OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

oauth_verifier_url = auth['auth_url']
oauth_verifier = requests.get(oauth_verifier_url)

final_step = twitter.get_authorized_tokens(oauth_verifier)

OAUTH_TOKEN = final_step['oauth_token']
OAUTH_TOKEN_SECRET = auth['oauth_token_secret']

twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

try:
    twitter.update_status(status='My first tweet from Twitter\'s Python API!')
except TwythonError as e:
    print e
