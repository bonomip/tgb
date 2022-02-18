import tweepy
import time
import math
import logging
#remove this and use your own keyz
import keys

# GIVAWAY DATA
owner_tweet = "charlieesposito"
tweet_id = 1477616556813299717
giveaway_keyword = "s8per"
number_of_tag = 0 ## @crysto @culo @gay
giveaway_end = "2022-02-19"
number_of_winners = 1 #sum of all the winners of all categories
split = False # there are more categories
number_of_winners2 = 3 # winners of second categories
######
###### MESSAGE FORMAT 
######       NAMI_WALLET_ADRESS DISCORD_USER_NAME TAG_1 ... TAG_N KEYWORD
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

# PARAMETERS
sleep_time = 60
api_cool_down = 60*15

#remove from l1 the elemnts of l2
def difference(l1, l2):
    l3 = [x for x in l1 if x not in l2]
    return l3

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
        

#SETUP ENDPOINT
auth = tweepy.OAuthHandler(api_key, api_key_secret, "oop")
api = tweepy.API(auth)
auth.set_access_token(api_token, api_token_secret) 
client = tweepy.Client(bearer_token=bearer_token)

#GET FOLLOWERS FUNCTION
def getFollowers(_screen_name):

    count = api.get_user(screen_name=_screen_name).followers_count
    
    users = tweepy.Cursor(api.get_followers, screen_name=_screen_name, count=200).items()

    followers = []

    step_size = 2400.0
    step_time = 20.0
    single_entry_time = step_time / step_size
    n_step = math.ceil(count / step_size) - 1
    total_estimated_time = ( (n_step * api_cool_down) + count * single_entry_time) / 60.0
    total_estimated_time = round(total_estimated_time, 1)
    print(_screen_name+" has "+str(count)+" follower. Estimated processing time: "+str(total_estimated_time)+ " minutes")
    
    start = time.time()
    while True:
        try:
            user = next(users)
            followers.append(user.screen_name)
        except tweepy.errors.TooManyRequests as e:
            logging.error("Twitter api rate limit reached")
            print("Users processed in total: "+str(len(followers)))
            print("Users left to process: "+str(count-len(followers)))
            time.sleep(api_cool_down)
        except tweepy.errors.TweepyException as e:
            logging.error("Tweepy error occurred:{}".format(e))
        except StopIteration:
            break


    finish = time.time()
    elapsed = (finish - start)
    print("finised in "+str(elapsed / 60)+" minutes")
    
    writeFile(followers_base_file+_screen_name, followers)
    return followers

def getReplies(candidates, _screen_name, tweet_id, key_word):
    query = 'to:{} {}'.format(_screen_name, key_word)

    tweets = tweepy.Cursor(api.search_tweets, until=giveaway_end, since_id=tweet_id, count=200, q=query).items()
    
    reply = []
    while True:
        try:
            tweet = tweets.next()
            if(tweet.in_reply_to_status_id == tweet_id ):
                reply.append(tweet)
        except tweepy.errors.TooManyRequests as e:
            logging.error("Twitter api rate limit reached:{}".format(e))
            time.sleep(60)
        except tweepy.errors.TweepyException as e:
            logging.error("Tweepy error occured:{}".format(e))
            break
        except StopIteration:
            break
        except Exception as e:
            logging.error("Failed while fetching replies {}".format(e))
            break
    
    dict = {}
    for tweet in reply:
        data = tweet.text.split()[0:3+number_of_tag]
        data[0] = tweet.author.screen_name
        if data[0] in candidates and data[0] not in dict.keys():
            #-----------------TODO!!!!!!!!!!!!!!
            ## do check on message validity such tags checks and wallet checks
            dict[data[0]] = data[1:3] ##only wallet_addr and discord_name

    return dict

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