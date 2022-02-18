import json
import random
import main

from candidate import candidates

def writeOut(file_name, l, d):
    with open(main.file_base_dir+file_name, "w") as fp:
        for user in l:
            key = user
            line = key + " " + ' '.join(map(str, d[key]))
            fp.writelines(line+"\n")

def readDict(file_name):  
    with open(main.file_base_dir+file_name) as f:
        data = f.read()
    return json.loads(data)

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

candidates = readDict(main.candidates_file)
candidates_name = list(candidates.keys())

winners = extraction(main.number_of_winners, candidates_name)
random.shuffle(winners)

if(main.split):
    writeOut("__Winners1__", winners[0:main.number_of_winners2], candidates)
    writeOut("__Winners2__", winners[main.number_of_winners2:main.number_of_winners], candidates)
else:
    writeOut("__Winners__", winners, candidates)