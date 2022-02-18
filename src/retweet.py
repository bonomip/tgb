import main

main.infiniteUpdate(main.retweet_file, main.api.get_retweets, lambda x: x, lambda x: x.user.screen_name)