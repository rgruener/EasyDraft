import urlparse
import httplib2
import time
import json
import oauth2 as oauth

# Largely based on sample code for simplegeo's python-oauth2 repository on github
# OAuth is used to access Yahoo Sports for filling database

consumer_key = 'dj0yJmk9SlBOaEx5VjJvRjJMJmQ9WVdrOWIyOVZiMUZpTnpnbWNHbzlNVE0xTURnNE1UVTJNZy0tJnM9Y29uc3VtZXJzZWNyZXQmeD1hOA--'
consumer_secret = 'eb800ec46583d123c8df54ac2c28f5d2975c06d9'

nfl_game_key = '273'
my_league_id = '840811'
my_league_key = nfl_game_key + '.l.' + my_league_id

def yahoo_oauth_get_token(callback_url):

    request_token_url = 'https://api.login.yahoo.com/oauth/v2/get_request_token?oauth_callback=%s' % callback_url
    access_token_url = 'https://api.login.yahoo.com/oauth/v2/get_token'
    authorize_url = 'https://api.login.yahoo.com/oauth/v2/request_auth'

    consumer = oauth.Consumer(consumer_key, consumer_secret)
    client = oauth.Client(consumer)

    # Get a request token
    resp, content = client.request(request_token_url, "GET")
    if resp['status'] != '200':
        raise Exception("Invalid response %s." % resp['status'])

    request_token = dict(urlparse.parse_qsl(content))

    # Step 2: Redirect to the provider. Since this is a CLI script we do not 
    # redirect. In a web application you would redirect the user to the URL
    # below.

    print "Go to the following link in your browser:"
    print "%s?oauth_token=%s" % (authorize_url, request_token['oauth_token'])

    redirect = "%s?oauth_token=%s" % (authorize_url, request_token['oauth_token'])

    return (redirect, request_token)

    # After the user has granted access to you, the consumer, the provider will
    # redirect you to whatever URL you have told them to redirect to. You can 
    # usually define this in the oauth_callback argument as well.
    accepted = 'n'
    while accepted.lower() == 'n':
        accepted = raw_input('Have you authorized me? (y/n) ')
    oauth_verifier = raw_input('What is the PIN? ')

def yahoo_oauth_access_token(request_token, oauth_verifier):

    token = oauth.Token(request_token['oauth_token'],
        request_token['oauth_token_secret'])
    token.set_verifier(oauth_verifier)
    client = oauth.Client(consumer, token)

    resp, content = client.request(access_token_url, "POST")
    access_token = dict(urlparse.parse_qsl(content))

    return access_token

    #print "Access Token:"
    #print "    - oauth_token        = %s" % access_token['oauth_token']
    #print "    - oauth_token_secret = %s" % access_token['oauth_token_secret']
    #print
    #print "You may now access protected resources using the access tokens above." 
    #print

def yahoo_get_resource(url, oauth_token, oauth_token_secret, extras=None):

    base_url = 'http://fantasysports.yahooapis.com/fantasy/v2/'

    params = {
            'format': 'json', 
            'oauth_version': "1.0",
            'oauth_nonce': oauth.generate_nonce(),
            'oauth_timestamp': int(time.time()),
    }

    if extras:
        params = dict(params.items() + extras.items())

    token = oauth.Token(key=oauth_token, secret=oauth_token_secret)
    consumer = oauth.Consumer(key=consumer_key, secret=consumer_secret)

    params['oauth_token'] = token.key
    params['oauth_consumer_key'] = consumer.key

    signature_method = oauth.SignatureMethod_HMAC_SHA1()

    oauth_request = oauth.Request.from_consumer_and_token(consumer, token=token, http_method='GET', http_url=base_url+url, parameters=params)
    oauth_request.sign_request(signature_method, consumer, token)
    #print 'REQUEST'
    url = oauth_request.to_url()
    #print url
    resp, content = httplib2.Http.request(oauth.Client(consumer), url, 'GET')
    #print 'GOT'
    #print resp
    return resp, json.loads(content)

if __name__ == '__main__':
    token = yahoo_oauth_get_token('http://localhost:5000')
    yahoo_get_resource('http://fantasysports.yahooapis.com/fantasy/v2/league/' + my_league_key + '/players', token['oauth_token'], token['oauth_token_secret'])
