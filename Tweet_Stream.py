import sys
import settings # Load API Twitter variables
import tweepy

class Tweet_Stream(tweepy.StreamListener):
    def on_status(selfself, status):
        print(status.text)

    def on_error(self, status_code):
        if status_code == 420:
            return False

# Create Twitter stream
def get_stream():
    api_token = get_api_token()
    stream = tweepy.Stream(auth = api_token, listener = Tweet_Stream())
    return stream

# Create OAuth token
def get_api_token():
    token = tweepy.OAuthHandler(settings.CONSUMER_KEY, settings.CONSUMER_SECRET)
    token.set_access_token(settings.ACCESS_TOKEN, settings.ACCESS_TOKEN_SECRET)
    return token

def track_user(keyword, stream):
    stream.filter(track=[keyword], async=True)

if __name__ == '__main__':

    # Get user to follow on Twitter
    if len(sys.argv) == 1:
        print("Missing keyword to search over")
        exit()

    # Extract keyword from command line args
    keyword = sys.argv[1]

    # Create Twitter stream
    stream = get_stream()

    # Begin streaming tweets
    track_user(keyword, stream)