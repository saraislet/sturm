# -*- coding: utf-8 -*-
"""
Created on Tue Sep 12 20:12:44 2017

@author: Sarai
"""

import os, re
from flask import Flask, request, render_template, redirect
from flask import session
import flask
import tweepy
import Sturmtest as st

app = Flask(__name__)

#app.config.from_pyfile('config.cfg', silent=True)

consumer_key = os.environ['consumer_key']
consumer_secret = os.environ['consumer_secret']
#OAUTH_TOKEN = os.environ['TWITTER_OAUTH_TOKEN']
#OAUTH_TOKEN_SECRET = os.environ['TWITTER_OAUTH_TOKEN_SECRET']


callback_url = 'https://murmuring-wildwood-21076.herokuapp.com/verify'
#session = dict()
#db = dict()


@app.route('/')
def send_token():
    redirect_url = ""
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret, callback_url)
#    redirect_url = auth.get_authorization_url()

    try: 
        #get the request tokens
        redirect_url= auth.get_authorization_url()
        session['request_token'] = auth.request_token
        
        return render_template('start.html', redirect_url = redirect_url)
    except tweepy.TweepError:
        print('Error! Failed to get request token')
        return flask.render_template('error.html')




@app.route("/verify")
def get_verification():

    #get the verifier key from the request url
    verifier = request.args['oauth_verifier']

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    print("session dict object is: " + str(session))
    token = session['request_token']
#    del session['request_token']

    auth.request_token = token

    try:
        auth.get_access_token(verifier)
        global api_user
        api_user = tweepy.API(auth)
        userdata = api_user.me()
        
        #store in a db
#        session['api'] = api_user
        session['key'] = auth.access_token
        session['secret'] = auth.access_token_secret
        session['userdata'] = userdata
#        print("Variable db contains: " + str(db))
        
        return flask.render_template('app.html', 
                                 name = userdata.name, 
                                 screen_name = userdata.screen_name, 
                                 bg_color = userdata.profile_background_color, 
                                 followers_count = userdata.followers_count, 
                                 created_at = userdata.created_at,
                                 logged_in = True)
        
    except tweepy.TweepError:
        print('Error! Failed to get access token.')
        
        return flask.render_template('error.html')


    

    

@app.route('/main')
def main():
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(session['key'], session['secret'])
    userdata = session['userdata']
    
        
    return flask.render_template('app.html', 
                                 logged_in = True,
                                 name = userdata.name,
                                 followers_count = userdata.followers_count)


@app.route('/sturm', methods=['POST'])
def sturm():
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(session['key'], session['secret'])
    api_user = tweepy.API(auth)
    
#    api_user = session['api']
    user = request.form['screen_name']
    num_results = request.form['num_results']
    
    if num_results.isdigit():
        num_results = int(num_results)
    else:
        num_results = 30
        
    user = re.sub(r"@","",user)
    
    re_patterns = st.init(st.words)
    st.set_api(api_user)
    results = st.test_followers(user, re_patterns, num_results)
    st.print_results(results.scores)
    if results.num_baddies > 0:
        show_baddies = True
    else:
        show_baddies = False
    
    return flask.render_template('results.html', 
                             user = user,
                             baddies_names = results.baddies_names,
                             baddies = results.baddies,
                             results = results.scores,
                             num_baddies = results.num_baddies,
                             num_results = results.num_results,
                             ratio = results.ratio,
                             show_baddies = show_baddies,
                             logged_in = True)

@app.route('/logout')
def logout():
    # remove variables from session
    del session['request_token']
    return redirect('../')

if __name__ == '__main__':
    app.debug = True
    app.run()
    
app.secret_key = '\n\x8d-\xd1"\xfa;EG`\xc1?|\xd5*\xeaO\x91\x0c\x0c\x1as\x1e<'