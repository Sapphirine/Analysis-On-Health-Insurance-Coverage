__author__ = 'Yingqi'
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler, Stream
import time, multiprocessing
access_token = "3636436889-3Lr0mBhiSgFmFu0FJRbqMcOyhFbKCkvuDov01ae"
access_token_secret = "Q2VMkILEZvJQPQlPJB4ocRwbqNY44wwzrcBV7rbzgITmW"
consumer_key = "zx3QhGvre6ZKWT6oFOBHjntTi"
consumer_secret = "ZLxQSJacJM8HGt3naGHRhPrH63QXKPz1shjxo4Z8i306X2UesG"


class StdOutListener(StreamListener):
    def on_data(self, data):
        with open("health.txt", "a") as file:
            file.write(data)
        return True

    def on_error(self, status_code):
        print(status_code)


if __name__ == "__main__":
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token,access_token_secret)
    stream = Stream(auth, l)
    track_list = ['health insurance']
    p = multiprocessing.Process(target=stream.filter(track=track_list))
    p.start()
    time.sleep(1800)
    p.terminate()