
# coding: utf-8

# # Sturmtest
# This notebook will test a bag of words approach for Sturmjäger.


import re
import tweepy
import plotly.plotly as py
import plotly.graph_objs as go
from IPython.display import clear_output
#import sign_in
#import tokens


# Set the private Twitter API keys.
#consumer_key = tokens.consumer_key
#consumer_secret = tokens.consumer_secret
#access_token = tokens.access_token
#access_token_secret = tokens.access_token_secret

# Pass tokens to Tweepy's OAuthHandler.
#auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
#auth.set_access_token(access_token, access_token_secret)


def set_api(api_user):
    global api
    api = api_user

# Define the bag of words
words = ["kekistan",
        "#kek",
        "14words",
        "14 words",
        "14 wrds",
        "fourteen words",
        "future for white children",
        "evropa",
        "ethnostate",
        "goyim",
        "cuck",
        "red pilled",
        "redpilled",
        "whitegenocide",
        "white genocide",
        "white pride",
        "whiteisright",
        "defending white",
        "prowhite",
        "pro white",
        "aryanState",
        "nationalsocialist",
        "national socialist",
        "national socialism",
        "nazionalsocialista",
        "nazional socialista",
        "white nationalist",
        "white supremacist",
        "identitarian",
        "卐",
        "⚡⚡",
        "ϟϟ",
        "✠",
        "⊕"]
print("Bag of words contains " + str(len(words)) + " words.")

def init(words):
    # set up a list of regex patterns
    # TODO: This would be more efficient as a trie.
    # Optimization may be unnecessary.
    re_patterns = []
    
    for word in words:
        re_patterns.append(r".*" + word)
    return re_patterns

        
def print_result_count(result):
    if result == 0:
        print("No match.")
    elif result == 1:
        print("There is 1 match.")
    else:
        print("There are " + str(result) + " matches.")

def test_count(string, re_patterns):
    string = str.lower(string)
    result = 0
    for pattern in re_patterns:
        if re.match(pattern, string):
            result += 1
    return result

def print_count(string, re_patterns):
    return print_result_count(test_count(string))


#TODO: define a class for results including methods to return stats & baddies
#TODO: build try/exception methods
#TODO: test rate limit, build cursor
    
def test_followers(user, re_patterns, num_results):
    # Evaluate a list of followers for Nazis. Return an array of scores.
    return test_list(api.followers_ids(user), re_patterns, num_results)

def test_follows(user, re_patterns, num_results):
    # Evaluate a list of friends for Nazis. Return an array of scores.
    return test_list(api.friends_ids(user), re_patterns, num_results)
    
    
def test_list(userlist, re_patterns, num_results):
    # Evaluate a list of users for Nazis. Return an array of scores.
    results = []
    global baddies
    baddies = []
    start = 0
    
    for i in range(start,start+num_results):
        try:
            userdata = api.get_user(userlist[i])
        except Exception:
            continue
            
        result = test_count(userdata.description, re_patterns)
        result += test_count(userdata.screen_name, re_patterns)
        result += test_count(userdata.name, re_patterns)
        result += test_1488(userdata.description)
        result += test_1488(userdata.screen_name)
        result += test_1488(userdata.name)
        
        results.append(result)
        
        # Add detected Nazis to the list of baddies.
        if result != 0:
            baddies.append(userdata)
        
        # Report scanning progress in console.
        if i % 20 == 0:
            clear_output()
            print(str(int((i-start)/num_results*100)) + "% complete")
    clear_output()
    return(results)

def test_1488(string):
    # Match 14 and 88 only if no digit precedes nor follows.
    # 14 and 88 may be separated by a single non-digit.
    # e.g., matches: 1488, 14/88, 14.88, asdf1488jkl, 13-14-88a, a14 88b.
    # e.g., non-matches: 14288, 14--88, 5551488555, 714/88.
    if re.match(r".*(?<!\d)14[\D]?88(?!\d)", string):
        return 1
    else:
        return 0


def print_results(results):
    x = [str(x) for x in range(0,5)]
    x.append("5+")
    y = []
    sum = 0
    for i in range(0,5):
        count = results.count(i)
        y.append(count)
        sum += count
    y.append(len(results) - sum)
    print(str(x))
    print(str(y))
    total = len(results) - y[0]
    ratio = round(total/len(results)*100, 1)
    print(str(ratio) + "% identified as Nazis (" + str(total) + " of " + str(len(results)) + " tested)")
    
    data = [go.Bar(
                x=x,
                y=y
        )]
    
    py.iplot(data, filename='basic-bar')

def print_baddies_details(baddies=baddies):
    # Print a list containing names, screen_names, and profile descriptions.
    countIter = iter([x for x in range(0,len(baddies))])
    
    for user in baddies:
        print(str(next(countIter)) + ": " + user.name + " / @" + user.screen_name 
             + " / https://www.twitter.com/" + user.screen_name)
        print(user.description)

def get_baddies(baddies=baddies):
    # Returns a list of baddies.
    return baddies

def get_baddies_names(baddies=baddies):
    # Return an array of screen_names from baddies.
    return [user.screen_name for user in baddies]

def check_rate():
    # Check rate limit status, return dict.
    return api.rate_limit_status()['resources']

def check_rate_users():
    # Check rate limit status for get user, return int.
    return api.rate_limit_status()['resources']['users']['/users/show/:id']['remaining']

def check_rate_lookup():
    # Check rate limit status for batch user lookups, return int.
    return api.rate_limit_status()['resources']['users']['/users/lookup']['remaining']
        

#user = "yonatanzunger"
#num_results = 800
#re_patterns = init(words)
#results = test_followers(user, re_patterns, num_results)
#print_results(results)