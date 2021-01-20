import tweepy, asyncio
# import time
import os

def create_api():
    consumer_key = os.environ.get('TW_CONSUMER_KEY')
    consumer_secret = os.environ.get('TW_CONSUMER_SECRET')
    access_token = os.environ.get('TW_ACCESS_TOKEN')
    access_token_secret = os.environ.get('TW_ACCESS_SECRET')

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    try:
        api.verify_credentials()
    except Exception as e:
        print("Error Creating API")
        raise e
    else:
        print("------")
        print("Twitter API created.")
        print("")
        print("------")
    return api

class TweetListener(tweepy.StreamListener):

    def __init__(self, d_msg = None, loop = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.d_msg = d_msg
        self.loop = loop

    def on_status(self, tweet):
        if self.d_msg:
            self.send_msg(tweet._json)
        else:
            print(tweet)

    def on_error(self, status_code):
        print(status_code)

    def send_msg(self, msg):
        future = asyncio.run_coroutine_threadsafe(self.d_msg(msg), self.loop)
        future.result()

if __name__ == '__main__':
    twitter_api = create_api()
    twitter_stream = tweepy.Stream(auth = twitter_api.auth, listener = TweetListener())
    twitter_stream.filter(follow=['978760100977500161'], is_async=True)
