import main

file_name = "retweet_"+str(main.tweet_id)

main.infiniteUpdate(file_name, main.api.get_retweets, lambda x: x, lambda x: x.user.screen_name)