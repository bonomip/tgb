import main
import utils

files = [   utils.file_base_dir+utils.like_file,
            main.file_base_dir+main.retweet_file ]

def candidates(files):
    lists = [ ]

    for file in files:
        lists.append(utils.readFile(file))

    result = lists.pop()

    for l in lists:
        result = utils.intersect(result, l)
    
    return result

main.getReplies(candidates(files), utils.owner_tweet, utils.tweet_id, utils.giveaway_keyword)





