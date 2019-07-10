from apscheduler.schedulers.blocking import BlockingScheduler
import tweepy, sys, json

reload(sys)
sys.setdefaultencoding("utf-8")

consumer_key='j86YoD0MYmULND8wXgMZ0FTUu'
consumer_secret='JqQgppcb4snuRf0CZeytQNSWuApckjF0gdPcd1zV9TB1gneyOg'
access_token_key='965076683673014272-V1tUrg5seD4PJLMp59J9ZaMcZi0ujY9'
access_token_secret='MMiFIWuTJAxbzEn7p4ZRYFk9ZsKni5DmImMcY2Xiai102'

var = tweepy.OAuthHandler(consumer_key, consumer_secret)
var.set_access_token(access_token_key, access_token_secret)
myApi = tweepy.API(var)


def query():
    print "Hello Team"
    geo = "39.8282,-98.5795,2500mi"
    tweets = myApi.search(x="playstation", count=500, geocode= geo , resultType="recent")
    for tweet in tweets:
        print tweet.created_at, tweet.user.screen_name, tweet.text
        with open("output.txt", 'a+') as files:
            files.write(tweet.text)
            files.write("\n")
    print "----------------------------------------------------------"

scheduler = BlockingScheduler()
scheduler.add_job(query, 'interval', seconds=10)
scheduler.start()