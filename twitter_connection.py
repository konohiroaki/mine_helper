import twitter


class TwitterApi:
    CONSUMER_KEY = "tgWsIgfeeYGRVquKZ2kryIC3b"
    CONSUMER_SECRET = "JE70Us5NuuFLbYRWqGaOBWqF2hfs6QRaEWSH9Z98O4iru059Q8"
    ACCESS_TOKEN_KEY = "737989501239230464-d1ft11Et4IlSjd9LCRzG8cZ1VrvcJf2"
    ACCESS_TOKEN_SECRET = "aAOY13lXBa6NDuWLuIHIgI3Ws6V4hUbWkvtXQp60fTax2"

    def tweet(self, file):
        api = twitter.Api(consumer_key=self.CONSUMER_KEY,
                          consumer_secret=self.CONSUMER_SECRET,
                          access_token_key=self.ACCESS_TOKEN_KEY,
                          access_token_secret=self.ACCESS_TOKEN_SECRET)
        api.PostUpdate("", file)
