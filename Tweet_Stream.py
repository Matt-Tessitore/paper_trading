import sys
import json
from datetime import datetime
import settings # Load API Twitter variables
import tweepy

class Tweet_Stream(tweepy.StreamListener):
    def __init__(self, keyword):
       self.keyword = keyword
       self.out_file = open(keyword + "_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S"), "w")

    def on_data(self, data):
        json_data = json.loads(data)
        self.out_file.write(str(json_data))

    def on_error(self, status_code):
        print >> sys.stderr, "Encourated error with status code: ", status_code

        if status_code == 420:
            self.out_file.close()
            return False

    def on_timeout(self):
       print >> sys.stderr, "Twitter timeout"


# Create Twitter stream
def get_stream(keyword):
    api_token = get_api_token()
    stream = tweepy.Stream(auth = api_token, listener = Tweet_Stream(keyword))
    return stream

# Create OAuth token
def get_api_token():
    token = tweepy.OAuthHandler(settings.CONSUMER_KEY, settings.CONSUMER_SECRET)
    token.set_access_token(settings.ACCESS_TOKEN, settings.ACCESS_TOKEN_SECRET)
    return token

def track_user(keyword, stream):
    stream.filter(track=[keyword], async=True)

# Main program driver
if __name__ == '__main__':

    # Get user to follow on Twitter
    if len(sys.argv) == 1:
        print("Missing keyword to search over")
        exit()

    # Extract keyword from command line args
    keyword = sys.argv[1]

    # Create Twitter stream
    stream = get_stream(keyword)

    # Begin streaming tweets
    track_user(keyword, stream)