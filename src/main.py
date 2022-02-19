import tweepy
import time
import logging
import utils

#remove this and use your own keyz
import keys

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

# check if name_2 follows name_1, requires screen_names
def isFollowedBy(sn_1, sn_2):
    return api.get_friendship(source_screen_name=sn_1,target_screen_name=sn_2)[1].following

def checkIfFollows(screen_name, list):
    for name in list:
        if not isFollowedBy(name, screen_name):
            return False
    return True

def checkTags(screen_name, tags):
    if len(tags) < utils.number_of_tags: #respect the requirment
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
            utils.writePlain("bkp_"+utils.candidates_file, replies)
            time.sleep(60)
        except tweepy.errors.TweepyException as e:
            logging.error("Tweepy error occured:{}".format(e))
            utils.writePlain("bkp_"+utils.candidates_file, replies)
            break
        except StopIteration:
            break
        except Exception as e:
            logging.error("Failed while fetching replies {}".format(e))
            utils.writePlain("bkp_"+utils.candidates_file, replies)
            break
    return replies

def getValidReplies(replies, candidates):
    result_dict = {}
    for tweet in replies:
        data = [ tweet.author.screen_name ]
        if not checkIfFollows(data[0], utils.to_follow) :
            print(data[0]+" dont follows the required user/users")
            continue
        if not utils.checkIfLikes(data[0], utils.tweet_id):
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
                if not checkTags( tmp[2:2+utils.number_of_tags] ) :
                    continue
            except IndexError:
                logging.error("Tweet format not correct")
                logging.error(tweet.text)
                continue
            result_dict[data[0]] = data[1:3]
    
    return result_dict

def getReplies(candidates, _screen_name, tweet_id, key_word):
    query = 'to:{} {}'.format(_screen_name, key_word)

    tweets = tweepy.Cursor(api.search_tweets, until=utils.giveaway_end, since_id=tweet_id, count=200, q=query).items()
    
    replies = getRepliesToTweet(tweets, tweet_id)
    
    candidates = getValidReplies(replies, candidates)
    
    print( "There are " + str( len( candidates ) ) + " candidates!" )

    utils.writeDict(utils.candidates_file_name, candidates)

def iterTweetsInfo(func, id, l, next_page):
    try:
        page = func(id=id, pagination_token=next_page)
    except tweepy.errors.TooManyRequests as e:
            logging.error("Twitter api rate limit reached:{}".format(e))
            utils.writeFile("bkp_"+utils.retweet_file_name, l)
            time.sleep(60*15)
    else:    
        if 'next_token' in page[3].keys():
            for user in page[0]:
                l.append(user.username)
            return iterTweetsInfo(func, id, l, page[3]['next_token'])
        return l

    iterTweetsInfo(id, l, next_page)

def getTweetsInfo(func, tweet_id, file_name):
    result = []
    while True:
        try:
            page = func(id=tweet_id)
        except tweepy.errors.TooManyRequests as e:
            logging.error("Twitter api rate limit reached:{}".format(e))
            utils.writeFile("bkp_"+file_name, result)
            time.sleep(60*15)
        else:    
            for user in page[0]:
                result.append(user.username)

            if "next_token" in page[3].keys():
                result = iterTweetsInfo(func, tweet_id, result, page[3]['next_token'])

            break

    utils.writeFile(file_name, set(result))