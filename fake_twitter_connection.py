import twitter


def tweet(file):
    api = twitter.Api(consumer_key='consumer_key',
                      consumer_secret='consumer_secret',
                      access_token_key='access_token_key',
                      access_token_secret='access_token_secret')
    api.PostUpdate("", file)
