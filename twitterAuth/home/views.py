from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django.utils.http import urlquote

import json
import urlparse
import oauth2 as oauth

global_request_token = None
client = None

consumer_key = 'cuXKU1S8RqSvYAd3oqlsOiVy8'
consumer_secret = 'ep49dL3521Oka8CusLOlSHoSwAmfAc206wPbl0pVOjN7mG7p2G'

def login(request):
        a = '<a class="twitter_button submit_button" href="/" action_mousedown="SignupTwitterClick" tabindex="6" id="__w2_ChdKUQJ_twitter_conne$
        return HttpResponse(a)

def index(request):

        global global_request_token, consumer_key, consumer_secret

        request_token_url = 'https://api.twitter.com/oauth/request_token'
        authorize_url = 'https://api.twitter.com/oauth/authorize'
        consumer = oauth.Consumer(consumer_key, consumer_secret)
        global client
        client = oauth.Client(consumer)

        resp, content = client.request(request_token_url, "GET")
        if resp['status'] != '200':
                raise Exception("Invalid response %s." % resp['status'])

        request_token = dict(urlparse.parse_qsl(content))

        global_request_token = request_token

	final_auth_url = "%s?oauth_token=%s" % (authorize_url, request_token['oauth_token'])
        return redirect(final_auth_url)


def callback(request):

        global global_request_token, consumer_key, consumer_secret, client

        access_token_url = 'https://api.twitter.com/oauth/access_token'

        oauth_verify = request.REQUEST['oauth_verifier']

        consumer = oauth.Consumer(consumer_key, consumer_secret)
        try:
                token = oauth.Token(global_request_token['oauth_token'], global_request_token['oauth_token_secret'])
                token.set_verifier(oauth_verify)
                client = oauth.Client(consumer, token)
		resp, content = client.request(access_token_url, "POST")
                access_token = dict(urlparse.parse_qsl(content))
        except:
                return HttpResponse("Error. Refresh again")

        if access_token:
                print access_token
                #name = access_token["screen_name"]
                name ="_name"
                tmp = json.dumps(access_token)
                token = oauth.Token(access_token['oauth_token'], access_token['oauth_token_secret'])
                client = oauth.Client(consumer, token)

                res = 'Hi '+access_token["screen_name"]+'<br/><br/><form name="tweetForm" method="post" action="/post_feed/"> Tweet:   <input t$
                res+=get_feeds(client)
                return HttpResponse(res)

                #return HttpResponse("Hi " + name + "<br/>" + get_followers(client))
        #return HttpResponse("Hi " + name + "<br/>" + get_feeds(client, 3))

	else:
                return HttpResponse("Access Token Error")


def get_followers(client):
        timeline_endpoint = "https://api.twitter.com/1.1/followers/list.json"

        response, data = client.request(timeline_endpoint)

        followers = json.loads(data)

        print followers

        name_list = []
        for user in followers["users"]:
                name_list.append(user["name"])
        name_list = "<br/>".join(name_list)
	return "Your followers: " + name_list

def get_feeds(client, maxLimit = 10):
        timeline_endpoint = "https://api.twitter.com/1.1/statuses/user_timeline.json"
        response, data = client.request(timeline_endpoint)

        tweets_data = json.loads(data)

        last_tweets = []

        count = 0
        for tweet in tweets_data:
                count = count + 1
                last_tweets.append(tweet.get("text"))
                if count == maxLimit:
                        break

        last_tweets = '<br/>'.join(last_tweets)
        return "Your <10 last tweets:<br/> " + last_tweets

@csrf_exempt
def post_feed(request):
        status = request.REQUEST["tweetBox"]
        global client
        postpointOne = 'https://api.twitter.com/1.1/statuses/update.json?status='+urlquote(status,safe='/')
#       postpoint = 'https://api.twitter.com/1.1/statuses/update.json?status='+status
        client.request(postpointOne, "POST")
        return HttpResponse("success")

