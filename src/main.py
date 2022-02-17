import tweepy
import time
import math
#remove this and use your own keyz
import keys

# GIVAWAY DATA
#this would be the tweet id 
# used to retreive data of likes and retweet
#change it !!!!!!!!!!
tweet_id = 1494358929975001089

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
    with open("data/"+file_name, "w") as fp:
        for user in list:
            fp.writelines(user+"\n")

def appendToFile(file_name, list):
    with open("data/"+file_name, "a") as fp:
        for user in list:
            fp.writelines(user+"\n")

def readFile(file_name):
    result = []
    with open("data/"+file_name, "r") as fp:
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
        except tweepy.errors.TooManyRequests:
            print("Too Many Request, wait 15 minutes...")
            print("Users processed in total: "+str(len(followers)))
            print("Users left to process: "+str(count-len(followers)))
            time.sleep(api_cool_down)
            user = next(users)
        except StopIteration:
            break
        followers.append(user.screen_name)
        
    finish = time.time()
    elapsed = (finish - start)
    print("finised in "+str(elapsed / 60)+" minutes")
    
    writeFile("followers_"+_screen_name, followers)
    return followers

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