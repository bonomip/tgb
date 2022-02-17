import main

screen_name = input()

print("Start saving follower of "+screen_name)
l1 = main.getFollowers(screen_name)
print("Finish")

print(len(l1))