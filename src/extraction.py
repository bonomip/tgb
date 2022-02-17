import random

number_of_winners = 60 #sum of all the winners of all categories
split = True # there are more categories
number_of_winners2 = 10 # winners of second categories

files = [   "data/followers_TrippiesSales",
            "data/likes-1494358929975001089",
            "data/retweet-1494358929975001089" ]

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

def writeOut(file_name, l):
    with open("data/"+file_name, "w") as fp:
        for user in l:
            fp.writelines(user+"\n")

def candidates(files):
    lists = [ ]

    for file in files:
        lists.append(readFile(file))

    result = lists.pop()

    for l in lists:
        result = intrsct(result, l)
    
    return result

def extraction(n, l):
    #if there are less candidates respect to the winners
    tmp = list(l)
    
    if(n >= len(tmp)):
        return tmp
        
    indexes = random.sample(range(0, len(tmp)), n)
    winners = []
    for index in indexes:
        winners.append(tmp[index])
        
    return winners

candidates = candidates(files)

print("There are "+str(len(candidates))+" candidates")
winners = extraction(number_of_winners, candidates)
random.shuffle(winners)

if(split):
    writeOut("__Winners1__", winners[0:number_of_winners2])
    writeOut("__Winners2__", winners[number_of_winners2:number_of_winners])
else:
    writeOut("__Winners__", winners)



