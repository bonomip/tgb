import json

######
###### MESSAGE FORMAT 
######       DISCORD_USER_NAME NAMI_WALLET_ADRESS TAG_1 ... TAG_N KEYWORD
######
###### SHOULD ONLY REPLY ONCE WITH THE KEYWORD!!!
###### SHOULD ONLY USE ONE SPACE AS DELIMETER! NOT MULTIPLE SPACES!!!! 
######

# GIVAWAY DATA
owner_tweet = "BillyM2k" #of the tweet that should be retweeted and replied
tweet_id = 1494487272078540803  #of the tweet that should be retweeted and replied
to_follow = [ owner_tweet ]
to_like = [ tweet_id ]
giveaway_keyword = "s8per" ## required in reply tweet
number_of_tags = 0 # required in reply tweet
giveaway_end = "2022-02-19"

#WINNER EXTRACTION DATA
number_of_winners = 1 #sum of all the winners of all categories
split = False # there are more categories
number_of_winners2 = 3 # winners of second categories



#################################################
###### PROGRAM DATA #############################
#################################################



# File names
file_base_dir = "data/"
like_file_name = "like_"+str(tweet_id)
retweet_file_name = "retweet_"+str(tweet_id)
followers_base_file_name = "followers_"
candidates_file_name = "candidates_"+str(tweet_id)


###### READ

def readFile(file_name):
    result = []
    with open(file_base_dir+file_name, "r") as fp:
        for l in fp:
            result.append(l.rstrip())
    return result

def readDict(file_name):  
    with open(file_base_dir+file_name) as f:
        data = f.read()
    return json.loads(data)

##### WRITE

def writeOutWinners(file_name, l, d):
    with open(file_base_dir+file_name, "w") as fp:
        for user in l:
            key = user
            line = key + " " + ' '.join(map(str, d[key]))
            fp.writelines(line+"\n")

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
        
############## OTHERS

def intersect(l1, l2):
    return set(l1).intersection(l2)
    
