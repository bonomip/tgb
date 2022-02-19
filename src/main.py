import re
import tweepy
import time
import math
import logging
import json
#remove this and use your own keyz
import keys

# GIVAWAY DATA
owner_tweet = "charlieesposito" #of the tweet that should be retweeted and replied
tweet_id = 1493930782238253057  #of the tweet that should be retweeted and replied
to_follow = [ "screen_name1", "screen_name2" ]
to_like = [ tweet_id ]
giveaway_keyword = "s8per"
number_of_tags = 0 ## @crysto @culo @gay
giveaway_end = "2022-02-19"
number_of_winners = 1 #sum of all the winners of all categories
split = False # there are more categories
number_of_winners2 = 3 # winners of second categories

######
###### MESSAGE FORMAT 
######       DISCORD_USER_NAME NAMI_WALLET_ADRESS TAG_1 ... TAG_N KEYWORD
######
###### SHOULD ONLY REPLY ONCE WITH THE KEYWORD!!!
###### SHOULD ONLY USE ONE SPACE AS DELIMETER! NOT MULTIPLE SPACES!!!! 
######

#File names
file_base_dir = "data/"
like_file = "like_"+str(tweet_id)
retweet_file = "retweet_"+str(tweet_id)
followers_base_file = "followers_"
candidates_file = "candidates_"+str(tweet_id)

# KEYS
client_id = keys.client_id
client_secret = keys.client_secret
api_key = keys.api_key
api_key_secret = keys.api_key_secret
bearer_token = keys.bearer_token
api_token =  keys.api_token
api_token_secret = keys.api_token_secret

#SETUP ENDPOINT
auth = tweepy.OAuthHandler(api_key, api_key_secret, "oop")
api = tweepy.API(auth)
auth.set_access_token(api_token, api_token_secret) 
client = tweepy.Client(bearer_token=bearer_token)

# PARAMETERS
sleep_time = 60
api_cool_down = 60*15

#remove from l1 the elemnts of l2
def difference(l1, l2):
    l3 = [x for x in l1 if x not in l2]
    return l3

def writeDict(file_name, d):
    with open(file_base_dir+file_name, 'w') as cf:
        cf.write(json.dumps(d))

def writePlain(file_name, list):
    with open(file_base_dir+file_name, "a") as fp:
        for status in list:
            fp.write(json.dumps(status._json))

def writeFile(file_name, list):
    with open(file_base_dir+file_name, "w") as fp:
        for user in list:
            fp.writelines(user+"\n")

def appendToFile(file_name, list):
    with open("data/"+file_name, "a") as fp:
        for user in list:
            fp.writelines(user+"\n")

def readFile(file_name):
    result = []
    with open(file_base_dir+file_name, "r") as fp:
        for l in fp:
            result.append(l.rstrip())
    return result
        
## check if name_2 follows name_1
## requires screen_names
def isFollowedBy(sn_1, sn_2):
    return api.get_friendship(source_screen_name=sn_1,target_screen_name=sn_2)[1].following

def checkIfFollows(screen_name, list):
    for name in list:
        if not isFollowedBy(name, screen_name):
            return False
    return True

def checkIfLikes(screen_name, list):
    return

def checkTags(screen_name, tags):
    if len(tags) < number_of_tags: #respect the requirment
        return False

    for tag in tags:
        try:
            #check if tag exist
            api.get_user(screen_name=tag)
        except tweepy.errors.NotFound:
            logging.error("Tagged user don't exist!")
            return False
        #check if tag follows screen_name    
        if not isFollowedBy(screen_name, tags) :
            return False
    
    return True

def getRepliesToTweet(tweets, tweet_id):
    replies = []
    while True:
        try:
            tweet = tweets.next()
            if(tweet.in_reply_to_status_id == tweet_id ):
                replies.append(tweet)
        except tweepy.errors.TooManyRequests as e:
            logging.error("Twitter api rate limit reached:{}".format(e))
            writePlain("bkp_"+candidates_file, replies)
            time.sleep(60)
        except tweepy.errors.TweepyException as e:
            logging.error("Tweepy error occured:{}".format(e))
            writePlain("bkp_"+candidates_file, replies)
            break
        except StopIteration:
            break
        except Exception as e:
            logging.error("Failed while fetching replies {}".format(e))
            writePlain("bkp_"+candidates_file, replies)
            break
    return replies

def getValidReplies(replies, candidates):
    result_dict = {}
    for tweet in replies:
        data = [ tweet.author.screen_name ]
        if not checkIfFollows(data[0], to_follow) :
            print(data[0]+" dont follows the required user/users")
            continue
        if not checkIfLikes(data[0], tweet_id):
            print(data[0]+" dont liked the required tweet/tweets")
            continue    
        if data[0] in candidates and data[0] not in dict.keys():
            try:
                tmp = tweet.text.split(" ", 1) #remove @mention
                tmp = tmp[1].split("#", 1) #get discord name
                discord_name = tmp[0]+"#" #save it
                tmp = tmp[1].split(" ") #get discord number
                discord_name += tmp[0] #save it
                data.append(discord_name)
                data.append(tmp[1]) # wallet addr
                if not checkTags( tmp[2:2+number_of_tags] ) :
                    continue
            except IndexError:
                logging.error("Tweet format not correct")
                logging.error(tweet.text)
                continue
            result_dict[data[0]] = data[1:3]
    
    return result_dict

def getReplies(candidates, _screen_name, tweet_id, key_word):
    query = 'to:{} {}'.format(_screen_name, key_word)

    tweets = tweepy.Cursor(api.search_tweets, until=giveaway_end, since_id=tweet_id, count=200, q=query).items()
    
    replies = getRepliesToTweet(tweets, tweet_id)
    
    candidates = getValidReplies(replies, candidates)
    
    print( "There are " + str( len( candidates ) ) + " candidates!" )

    writeDict(candidates_file, candidates)

def iterRetweet(id, l, next_page):
    try:
        page = client.get_retweeters(id=id, pagination_token=next_page)
    except tweepy.errors.TooManyRequests as e:
            logging.error("Twitter api rate limit reached:{}".format(e))
            writeFile("bkp_"+retweet_file, l)
            time.sleep(60*15)
    else:    
        if 'next_token' in page[3].keys():
                for user in page[0]:
                    l.append(user.username)
                return iterRetweet(id, l, page[3]['next_token'])
        return l

    iterRetweet(id, l, next_page)

def getReetwitters(tweet_id):
    result = []
    while True:
        try:
            page = client.get_retweeters(id=tweet_id)
        except tweepy.errors.TooManyRequests as e:
            logging.error("Twitter api rate limit reached:{}".format(e))
            writeFile("bkp_"+retweet_file, result)
            time.sleep(60*15)
        else:    
            for user in page[0]:
                result.append(user.username)

            if "next_token" in page[3].keys():
                result = iterRetweet(tweet_id, result, page[3]['next_token'])

            break

    writeFile(retweet_file, set(result))

def getLast100(func, unwrap1, unwrap2):
    data = func(id=tweet_id)
    l = []
    for d in unwrap1(data):
        l.append(unwrap2(d))
    return l

def infiniteUpdate(file_name, func, unwrap1, unwrap2):
    l = getLast100(func, unwrap1, unwrap2)    

    print("Append to file...")
    writeFile(file_name, l)

    print("Go to sleep for 1 minute")
    time.sleep(sleep_time)
    print("Awake...")

    while True:
        l1 = readFile(file_name)
        l2 = getLast100(func, unwrap1, unwrap2)
        l3 = difference(l2, l1)
        if(len(l3) != 0):
            print("Append to file...")
            appendToFile(file_name, l3)
        print("Go to sleep for 1 minute")
        time.sleep(sleep_time)
        print("Awake...")