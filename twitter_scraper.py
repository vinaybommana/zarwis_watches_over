import tweepy
import sys
import jsonpickle
import fileinput
from datetime import datetime
# import io
import codecs
# import csv
# import os
# Replace the API_KEY and API_SECRET with your application's key and secret.
APP_KEY = 'BlHVe4NazxtdbPgx386iUV6MZ'
APP_SECRET = 'f2Hhq39zzPeIaU3mQZgqki2he4ncTXEE8dOglTJtDOl193LK3l'

auth = tweepy.AppAuthHandler(APP_KEY, APP_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

if (not api):
    print("Can't Authenticate")
    sys.exit(-1)

# csv_file = csv.writer(open("output.csv", "w"))
# csv_file.writerow(["Name", "Screen Name", "Id", "Friends Count"])
# this is what we're searching for
maxTweets = 100
# Some arbitrary large number
tweetsPerQry = 100
list_of_names = []
tags = []
tweets_text = []
time_zone_list = list()
user_ids = []


# 1. Chess <brown>
# 2. hockey
# 3. Tennis <browinsh red>
# 4. Cricket <green>
# 5. Badminton
# 6. Athletics <yellow>
# 7. soccer <red>
# 8. volleyball <grey>
# 9. baskeyball
# 10. swimming <blue>

games = [
    "Chess",
    "Hockey",
    "Tennis",
    "Cricket",
    "Badminton",
    "Athletics",
    "Soccer",
    "Volleyball",
    "BasketBall",
    "Swimming"
]


def read_file(input_file):
    with fileinput.input(files=(str(input_file))) as f:
        for line in f:
            tags.append(line)


def main():
    # only a single main function is not cool
    read_file(sys.argv[1])
    for searchitem in games:
        for value in tags:
            value = value.strip()
            values = value.split("\t")
            search_item = searchitem
            start_date = values[0]
            end_date = values[1]
            startDateTime = datetime.strptime(start_date, '%Y-%m-%d')
            endDateTime = datetime.strptime(end_date, '%Y-%m-%d')
            startDateTime = startDateTime.date()
            endDateTime = endDateTime.date()
            sinceId = None
            max_id = -1

            tweetCount = 0
            print("Downloading max {0} tweets".format(maxTweets))
            while tweetCount < maxTweets:
                try:
                    if (max_id <= 0):
                        if (not sinceId):
                            new_tweets = api.search(q=search_item,
                                                    count=tweetsPerQry,
                                                    since=str(startDateTime),
                                                    until=str(endDateTime),
                                                    show_user=True)
                        else:
                            new_tweets = api.search(q=search_item,
                                                    count=tweetsPerQry,
                                                    since_id=sinceId,
                                                    since=str(startDateTime),
                                                    until=str(endDateTime),
                                                    show_user=True)
                    else:
                        if (not sinceId):
                            new_tweets = api.search(q=search_item,
                                                    count=tweetsPerQry,
                                                    since=str(startDateTime),
                                                    until=str(endDateTime),
                                                    max_id=str(max_id - 1),
                                                    show_user=True)
                        else:
                            new_tweets = api.search(q=search_item,
                                                    count=tweetsPerQry,
                                                    since=str(startDateTime),
                                                    until=str(endDateTime),
                                                    max_id=str(max_id - 1),
                                                    since_id=sinceId,
                                                    show_user=True)
                    if not new_tweets:
                        print("No more tweets found")
                        break
                    for tweet in new_tweets:
                        Tweet = jsonpickle.encode(tweet._json, unpicklable=False)
                        Tweet = jsonpickle.decode(Tweet)
                        time_zone_list.append(Tweet['user']['time_zone'])
                    tweetCount += len(new_tweets)
                    print("Downloaded {0} tweets".format(tweetCount))
                    max_id = new_tweets[-1].id
                except tweepy.TweepError as e:
                    # Just exit if any error
                    print("some error : " + str(e))
                    break

                with codecs.open(str(search_item) + ".txt", "w", "utf-8") as o:
                    o.write("count" + "\t\t" + "time_zone\n")
                    for timezone in time_zone_list:
                        # print(type(line))
                        if timezone is not None:
                            o.write(timezone + "\n")

        # users_and_their_tweets = dict(zip(user_ids, tweets_text))
        # print(users_and_their_tweets)

        print("Downloaded {0} tweets, Saved to {1}".format(tweetCount,
                                                           str(search_item) + ".txt"))


if __name__ == '__main__':
    main()
