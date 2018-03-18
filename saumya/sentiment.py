import tweepy
from textblob import TextBlob

consumer_key = 'R2SeMmf4mAXFUA3JBWd45I161'
consumer_secret = 'TYIrhNAjMHk9pNAVufPGpQrMuF4fAHtdFzNOAS9i6zB3UVgVMa'
access_token = '975001553932312576-kFgutH9DIyGpUX1f0MNtz2ufJg0Dy00'
access_token_secret = 'KFfTyBzBEFISrFT8eGpmRwcd4iQNt8uZNM2YGQF3IlPBO'
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

list = []


def tweet_sentiment(date, stock):
    public_tweets = api.search(
        stock, lang='en', result_type='popular', until=date, count=5)
    for tweet in public_tweets:
        # print(tweet.text)
        text = api.get_status(
            tweet.id, tweet_mode='extended')._json['full_text']
        # user_id = api.get_status()
        tb = TextBlob(text)
        print(tb.sentiment.polarity)
        score = float(tb.sentiment.polarity) * \
            (1 - float(tb.sentiment.subjectivity))
        list.append(text + "," + str(score))


tweet_sentiment("2018-03-18", "NASA")
