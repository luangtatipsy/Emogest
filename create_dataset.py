import calendar
import os
import time
from datetime import datetime

import emoji
import pandas as pd
from dotenv import load_dotenv

from emogest.data.labels import EMOJIS
from emogest.utils.dataframe import append_row, create_dataframe, dump_dataframe
from emogest.utils.logs import create_log_file, write_log_file
from emogest.utils.twitter_api import TwitterApiWrapper

load_dotenv()


if __name__ == "__main__":
    # Twitter API credentials
    consumer_key = os.environ.get("TWITTER_API_KEY")
    consumer_secret = os.environ.get("TWITTER_API_KEY_SECRET")
    access_key = os.environ.get("TWITTER_ACCESS_TOKEN")
    access_secret = os.environ.get("TWITTER_ACCESS_TOKEN_SECERT")

    num_tweets = 10000  # Number of tweets by an emoji
    current_year = datetime.now().year
    column_name = "tweet"

    timestamp = str(time.time()).replace(".", "_")
    log_file_path = os.path.join("logs", f"{timestamp}.txt")
    output_file_path = os.path.join("datasets", "raw_data.csv")

    api = TwitterApiWrapper(consumer_key, consumer_secret, access_key, access_secret)
    print(f"API Crawler has been intialized")
    print()

    df = create_dataframe(columns=[column_name])

    create_log_file(path=log_file_path)

    print(f"Start querying {datetime.now()}")
    for ej in EMOJIS:
        print(f"start collecting tweets which contain {ej}...")

        tweets = api.query_by_keyword(keyword=ej, count=num_tweets, batch=50)

        df = append_row(df, rows={column_name: tweets})
        dump_dataframe(df, output_file_path)

        write_log_file(path=log_file_path, log=ej)
        print(f"tweets which contain {ej} have been collected")
        print()
        print(f"Finished querying {datetime.now()}")
