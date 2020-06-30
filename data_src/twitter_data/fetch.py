import os
import sys
sys.path.insert(1, os.path.join(os.path.dirname(os.path.realpath(__file__)), '..\\..\\'))
import time
from pandas import DataFrame
import tweepy
import json
from k3y5 import TWITTER_API_KEY,TWITTER_API_SECRET_KEY,TWITTER_ACCESS_TOKEN,TWITTER_ACCESS_TOKEN_SECRET,IBM_API_KEY,IBM_URL
from ibm_watson import PersonalityInsightsV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

# loading keys from json file
MAX_TWEET = 100

# connecting to twitter api
auth = tweepy.OAuthHandler(TWITTER_API_KEY,TWITTER_API_SECRET_KEY)
auth.set_access_token(TWITTER_ACCESS_TOKEN,TWITTER_ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

authenticator = IAMAuthenticator(IBM_API_KEY)
PI = PersonalityInsightsV3( 
    version='2020-06-15',
    authenticator=authenticator
    )
PI.set_service_url(IBM_URL)

def limit_handled(cursor,list_name):
    while True:
        try:
            yield cursor.next()

        # catch the api rate limit exception and wait for 15 minutes
        except tweepy.RateLimitError:
            print(f"\nData points in list = {len(list_name)}")
            print("Hit Twitter API rate limit.")
            for i in range(3,0,-1):
                print(f"Wait for {i*5} mins.")
                time.sleep(5*60)
        
        # catch other api exceptions
        except tweepy.error.TweepError:
            print("\n Caught TweepError exception")

# this function outputs the csv file for all the tweets received
def get_all_tweets_df(username):
    all_tweets = []
    
    # requesting the most recent tweets(200 max)
    new_tweets = api.user_timeline(screen_name=username,count=MAX_TWEET)
    all_tweets.extend(new_tweets)

    # saving the id of the oldest tweet fetched
    oldest = all_tweets[-1].id - 1

    # to get tweets until there are none left
    while len(new_tweets)>0:
        print(f"getting tweets before {oldest}")

        # requesting tweets and saving new tweets to all tweets
        new_tweets = api.user_timeline(screen_name = username,count=MAX_TWEET,max_id = oldest) 
        # max_id is to return tweets with an id less than or equal to specified id
        all_tweets.extend(new_tweets) # adds all the iterms in iterable list unlike append

        # updating the id of the oldest tweet
        oldest = all_tweets[-1].id - 1
        print(f"...{len(all_tweets)} tweets downloaded so far")

    # transforming the tweets to 2D array
    out_tweets = [[tweet.id_str,tweet.created_at,tweet.text,
                  tweet.favorite_count,tweet.in_reply_to_screen_name,tweet.retweeted]for tweet in all_tweets]

    # converting list of list to dataframe
    data = DataFrame(out_tweets,columns=['id','created_at','text','likes','in reply to','retweeted'])
    data.to_csv(f'{username}_tweets.csv',index=False)

    pass

'''
returns the tweets in a dictionary format containing a list of dictionary formatted tweets

dictionary = {
    'contentItems':[
        {
            'content': tweets text,
            'contenttype': 'application/json',
            'id': tweets id,
            'created':tweets creation date,
            'language':'en'
        }
    ]
}
'''
def get_all_tweets_dic(username):
    all_tweets = []
    tweet_dic = {
        'contentItems':[]
    }
    
    # requesting the most recent tweets(200 max)
    try:
        new_tweets = api.user_timeline(screen_name=username,count=MAX_TWEET)
        all_tweets.extend(new_tweets)
    except tweepy.error.TweepError:
        print("Username doesn't exist or the API or ACCESS tokens is wrong")

    '''while len(new_tweets)>0:
        print(f"getting tweets before {oldest}")

        # requesting tweets and saving new tweets to all tweets
        new_tweets = api.user_timeline(screen_name = username,count=MAX_TWEET,max_id = oldest) 
        # max_id is to return tweets with an id less than or equal to specified id
        all_tweets.extend(new_tweets) # adds all the iterms in iterable list unlike append

        # updating the id of the oldest tweet
        oldest = all_tweets[-1].id - 1
        print(f"...{len(all_tweets)} tweets downloaded so far")'''

    # appending the tweets into the list on contentItems
    for tweet in all_tweets:
        td = {
            'content':tweet.text,
            'contenttype':'application/json',
            'id':tweet.id_str,
            'created':tweet.created_at,
            'language':'en'
        }
        tweet_dic['contentItems'].append(td)
        
    return json.dumps(tweet_dic,indent=2,default=str)

# pushes the dictionary created into the personality insights to get the results
def get_insight(dic):
    profile = PI.profile(
        dic,
        'application/json',
        raw_scores=True,
        consumption_preferences=True).get_result()

    return json.dumps(profile, indent=2)

# getting a dictionary of PERSONALITY score for each value
'''
- personality
    - big5_openness
        - adventurousness
        - artistic interests
        - emotionality
        - imagination
        - intellect
        - liberalism
    - big5_conscientiousness
        - achievement striving
        - cautiousness
        - dutifulness
        - orderliness
        - self-discipline
        - self-efficacy --> producing results?
    - big5_extraversion
        - activity level
        - assertiveness
        - cheerfulness
        - excitement seeking
        - outgoing
        - gregariousness --> sociable
    - big5_agreeableness
        - altruism --> disinterested and selfless concern for the well-being of others
        - cooperation
        - modesty
        - uncompromising
        - sympathy
        - trust
    - big5_neuroticism (emotional range)
        - fiery
        - prone to worry
        - melancholy
        - immoderation
        - self consciousness
        - susceptible to stress
'''
def get_personality(insight):
    personality = dict()
    for i in range(len(insight['personality'])):
        if insight['personality'][i]['trait_id'] == 'big5_openness':
            personality[f"personality_{insight['personality'][i]['trait_id'][5:]}_score"] = insight['personality'][i]['raw_score']
            for o in range(len(insight['personality'][i]['children'])):
                personality[f"personality_{insight['personality'][i]['children'][o]['trait_id'][6:]}_score"] = insight['personality'][i]['children'][o]['raw_score']
        if insight['personality'][i]['trait_id'] == 'big5_conscientiousness':
            personality[f"personality_{insight['personality'][i]['trait_id'][5:]}_score"] = insight['personality'][i]['raw_score']
            for c in range(len(insight['personality'][i]['children'])):
                personality[f"personality_{insight['personality'][i]['children'][c]['trait_id'][6:]}_score"] = insight['personality'][i]['children'][c]['raw_score']
        if insight['personality'][i]['trait_id'] == 'big5_extraversion':
            personality[f"personality_{insight['personality'][i]['trait_id'][5:]}_score"] = insight['personality'][i]['raw_score']
            for c in range(len(insight['personality'][i]['children'])):
                personality[f"personality_{insight['personality'][i]['children'][c]['trait_id'][6:]}_score"] = insight['personality'][i]['children'][c]['raw_score']
        if insight['personality'][i]['trait_id'] == 'big5_agreeableness':
            personality[f"personality_{insight['personality'][i]['trait_id'][5:]}_score"] = insight['personality'][i]['raw_score']
            for c in range(len(insight['personality'][i]['children'])):
                personality[f"personality_{insight['personality'][i]['children'][c]['trait_id'][6:]}_score"] = insight['personality'][i]['children'][c]['raw_score']
        if insight['personality'][i]['trait_id'] == 'big5_neuroticism':
            personality[f"personality_{insight['personality'][i]['trait_id'][5:]}_score"] = insight['personality'][i]['raw_score']
            for c in range(len(insight['personality'][i]['children'])):
                personality[f"personality_{insight['personality'][i]['children'][c]['trait_id'][6:]}_score"] = insight['personality'][i]['children'][c]['raw_score']

    return personality

# getting NEED scores for each value
'''
- needs
    - challenge
    - closeness
    - curiosity
    - excitement
    - harmony
    - liberty
    - love
    - practicality
    - self expression
    - stability
    - structure
'''
def get_need(insight):
    need = dict()
    for i in range(len(insight['needs'])):
        need[f"need_{insight['needs'][i]['trait_id'][5:]}_score"] = insight['needs'][i]['raw_score']

    return need

# getting VALUES scores for each value
'''
- values
    - conservation
    - openness to change
    - hedonism --> pursuit of pleasure
    - self enhancement
    - self transcendence --> experience
'''
def get_value(insight):
    value = dict()
    for i in range(len(insight['values'])):
        value[f"value_{insight['values'][i]['trait_id'][6:]}_score"] = insight['values'][i]['raw_score']

    return value

# calculating distance between two profiles
def difference(dic1,dic2):
    res = dict()
    for i,j in zip(dic1.items(),dic2.items()):
        res[i[0]] = i[1] - j[1]

    return res

# combining all personality, need and value into a score dictionary
def combine(personality,need,value):
    score = {
        'personality':personality,
        'need':need,
        'value':value
    }
    
    return score

# returning a score of a single username
def get_score(insight):
    p = get_personality(insight)
    n = get_need(insight)
    v = get_value(insight)

    score = combine(p,n,v)

    return score

def get_dist(insight1,insight2):
    # calling all functions to get personality, need and value for both profiles
    try:
        p1 = get_personality(insight1)
        n1 = get_need(insight1)
        v1 = get_value(insight1)
        p2 = get_personality(insight2)
        n2 = get_need(insight2)
        v2 = get_value(insight2)

        # calling function difference to get the difference between 
        # all scores of personality, need and value
        p_diff = difference(p1,p2)
        n_diff = difference(n1,n2)
        v_diff = difference(v1,v2)

        # profile distance combined into one score
        dist = combine(p_diff,n_diff,v_diff)
        return dist
    
    except:
        insight1 = json.loads(insight1)
        insight2 = json.loads(insight2)

        p1 = get_personality(insight1)
        n1 = get_need(insight1)
        v1 = get_value(insight1)
        p2 = get_personality(insight2)
        n2 = get_need(insight2)
        v2 = get_value(insight2)

        # calling function difference to get the difference between 
        # all scores of personality, need and value
        p_diff = difference(p1,p2)
        n_diff = difference(n1,n2)
        v_diff = difference(v1,v2)

        # profile distance combined into one score
        dist = combine(p_diff,n_diff,v_diff)
        return dist

def twtScore(username):
    tw_dic1 = get_all_tweets_dic(username)
    # tw_dic2 = get_all_tweets_dic(username2)
    insight1 = get_insight(tw_dic1)
    # insight2 = get_insight(tw_dic2)
    '''print(insight1)
    print(insight2)'''
    # diff = get_dist(insight1,insight2)
    insight1 = json.loads(insight1)
    score = {
        'big5': {
            'openness': insight1['personality'][0]['raw_score'],
            'conscientiousness': insight1['personality'][1]['raw_score'],
            'extraversion': insight1['personality'][2]['raw_score'],
            'agreeableness': insight1['personality'][3]['raw_score'],
            'neuroticism': insight1['personality'][4]['raw_score']
        },
        'values': {
            'conservation':  insight1['values'][0]['raw_score'],
            'open_to_change':  insight1['values'][1]['raw_score'],
            'self_enhancement': insight1['values'][3]['raw_score'],
            'self_transcendence':  insight1['values'][4]['raw_score']
        }
    }
    big5_score = (score['big5']['openness'] + score['big5']['conscientiousness'] + score['big5']['extraversion'] + score['big5']['agreeableness'] + score['big5']['neuroticism'])/5
    value_score = (score['values']['conservation'] + score['values']['open_to_change'] + score['values']['self_enhancement'] + score['values']['self_transcendence'])/4 
    return big5_score, value_score
'''
raw
- openness
- extraversion
- agreeableness
- conscientiousness
- neuroticism
'''
# print(twtScore('@sidtweetsnow', '@cached_cadet'))
# print(get_insight(get_all_tweets_dic('@cached_cadet')))