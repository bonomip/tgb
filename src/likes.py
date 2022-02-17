import main

file_name = "likes_"+str(main.tweet_id)

main.infiniteUpdate(file_name, main.client.get_liking_users, lambda x: x.data, lambda x: x.username)
