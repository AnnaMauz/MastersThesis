import csv
import instaloader

outputfile = "posts.txt"

from datetime import datetime
import instaloader

L = instaloader.Instaloader(download_pictures=False, download_videos=False, download_video_thumbnails = False, download_geotags=False, download_comments = False, save_metadata=False)
L.login("username", "password")

#posts = instaloader.Hashtag.from_name(L.context, "hashtag").get_posts()
posts = instaloader.Profile.from_username(L.context, "username").get_posts()

SINCE = datetime(2020, 5, 20)  # further from today, inclusive
UNTIL = datetime(2021, 5, 20)  # closer to today, not inclusive

k = 0  # initiate k
#k_list = []  # uncomment this to tune k

for post in posts:
    postdate = post.date

    if postdate > UNTIL:
        continue
    elif postdate <= SINCE:
        k += 1
        if k == 50:
            break
        else:
            continue
    else:
        L.download_post(post, "folder")

        # if you want to tune k, uncomment below to get your k max
        #k_list.append(k)
        k = 0  # set k to 0
