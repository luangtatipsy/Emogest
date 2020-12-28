import os
from datetime import datetime
from typing import List

import tweepy  # https://github.com/tweepy/tweepy


class TwitterApiWrapper(object):
    def __init__(
        self,
        consumer_key: str,
        consumer_secret: str,
        access_key: str,
        access_secret: str,
    ) -> None:
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_key, access_secret)

        self.api = tweepy.API(auth, wait_on_rate_limit=True)
        self._date_format = "%Y-%m-%d"

    def query_by_username(
        self, username: str, batch: int, get_all: bool = False
    ) -> List[str]:
        all_tweets = []

        tweets = self.api.user_timeline(
            screen_name=username, count=batch, tweet_mode="extended"
        )
        all_tweets.extend(tweets)

        if get_all:
            # save the last_seen_id tweet less one
            last_seen_id = all_tweets[-1].id - 1
            while len(tweets) > 0:
                tweets = self.api.user_timeline(
                    screen_name=username,
                    count=batch,
                    max_id=last_seen_id,
                    tweet_mode="extended",
                )

                all_tweets.extend(tweets)
                # update the last_seen_id tweet less one
                last_seen_id = tweets[-1].id - 1

        return [tweet.full_text for tweet in all_tweets]

    def query_by_keyword(
        self,
        keyword: str,
        count: int,
        batch: int = 100,
        lang: str = "th",
        exclude_retweet: bool = True,
    ) -> List[str]:

        exclude_retweet = " -filter:retweets" if exclude_retweet else ""

        query_str = f"{keyword}{exclude_retweet}"

        all_tweets = []

        tweets = self.api.search(
            q=query_str, count=batch, lang=lang, tweet_mode="extended"
        )
        all_tweets.extend(tweets)

        # save the last_seen_id tweet less one
        last_seen_id = all_tweets[-1].id - 1

        while len(all_tweets) < count:
            tweets = self.api.search(
                q=query_str,
                count=batch,
                lang=lang,
                max_id=last_seen_id,
                tweet_mode="extended",
            )

            all_tweets.extend(tweets)
            # update the last_seen_id tweet less one
            last_seen_id = tweets[-1].id - 1

            print(f"{len(all_tweets)} tweets downloaded so far")

        return [tweet.full_text for tweet in all_tweets]
