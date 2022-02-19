import utils
import random
import main

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

candidates = utils.readDict(main.candidates_file)
candidates_name = list(candidates.keys())

winners = extraction(main.number_of_winners, candidates_name)
random.shuffle(winners)

if(main.split):
    utils.writeOutWinners("__Winners1__", winners[0:utils.number_of_winners2], candidates)
    utils.writeOutWinners("__Winners2__", winners[utils.number_of_winners2:utils.number_of_winners], candidates)
else:
    utils.writeOutWinners("__Winners__", winners, candidates)