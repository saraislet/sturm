
# coding: utf-8

# # Sturmtest
# This notebook will test a bag of words approach for Sturmjäger.


import re
import tweepy
import plotly.plotly as py
import plotly.graph_objs as go
from IPython.display import clear_output
import tokens


# Set the private Twitter API keys.
consumer_key = tokens.consumer_key
consumer_secret = tokens.consumer_secret
access_token = tokens.access_token
access_token_secret = tokens.access_token_secret

# Pass tokens to Tweepy's OAuthHandler.
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# Define the bag of words
words = ["kekistan",
        "#kek",
        "1488",
        "14/88",
        "14-88",
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
def test_followers(user, re_patterns):
    follower_ids = api.followers_ids(user)
    
    results = []
    baddies = []
    num_results = 100
    start = 0
    
    for i in range(start,start+num_results):
        try:
            userdata = api.get_user(follower_ids[i])
        except Exception:
            continue
            
        result = test_count(userdata.description, re_patterns)
        result += test_count(userdata.screen_name, re_patterns)
        result += test_count(userdata.name, re_patterns)
        
        results.append(result)
        
        # Add detected Nazis to the list of baddies.
        if result != 0:
            baddies.append(userdata)
        
        # Report scanning progress in console.
        if i % 10 == 0:
            clear_output()
            print(str((i-start)/num_results*100) + "% complete")
    clear_output()
    return(results)


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

def print_baddies(baddies):
    countIter = iter([x for x in range(0,len(baddies))])
    
    for baddie in baddies:
        print(str(next(countIter)) + ": " + baddie.name + " / @" + baddie.screen_name 
             + " / https://www.twitter.com/" + baddie.screen_name)
        print(baddie.description)
        
        

user = "Goyveyim"
re_patterns = init(words)
results = test_followers(user, re_patterns)
print_results(results)