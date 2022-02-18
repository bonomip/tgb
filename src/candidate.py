import main
import json
import os

files = [   main.file_base_dir+main.like_file,
            main.file_base_dir+main.retweet_file ]

for file in os.listdir(main.file_base_dir):
    i = len(main.followers_base_file)
    if file[0:i] == 'followers_' :
        files.append(main.file_base_dir+file)

def readFile(file_name):
    result = []
    with open(file_name, "r") as fp:
        for l in fp:
            result.append(l.rstrip())
    return result

def intrsct(l1, l2):
    return set(l1).intersection(l2)

def intersect(l1, l2, l3, l4):
    return intrsct( intrsct(l1, l2), intrsct(l3, l4) )

def writeDict(file_name, d):  
    with open(main.file_base_dir+file_name, 'w') as cf:
        cf.write(json.dumps(d))

def candidates(files):
    lists = [ ]

    for file in files:
        lists.append(readFile(file))

    result = lists.pop()

    for l in lists:
        result = intrsct(result, l)
    
    return result

candidates = candidates(files)

candidates = main.getReplies(candidates, main.owner_tweet, main.tweet_id, main.giveaway_keyword)

candidates_name = list(candidates.keys())

print("There are "+str(len(candidates_name))+" candidates")

writeDict(main.candidates_file, candidates)





