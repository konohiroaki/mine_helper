import twitter


class TwitterApi:
    CONSUMER_KEY = "CONSUMER_KEY"
    CONSUMER_SECRET = "CONSUMER_SECRET"
    ACCESS_TOKEN_KEY = "ACCESS_TOKEN_KEY"
    ACCESS_TOKEN_SECRET = "ACCESS_TOKEN_SECRET"

    def tweet(self, text, file):
        api = twitter.Api(consumer_key=self.CONSUMER_KEY,
                          consumer_secret=self.CONSUMER_SECRET,
                          access_token_key=self.ACCESS_TOKEN_KEY,
                          access_token_secret=self.ACCESS_TOKEN_SECRET)
        api.PostUpdate(text, file)
