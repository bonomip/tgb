import main

main.infiniteUpdate(main.like_file, main.client.get_liking_users, lambda x: x.data, lambda x: x.username)
