# Datasets

__TL;DR__: For a privacy reason, the dataset used in this project is not distributed to the public.

A dataset for this project is gathered by Twitter API using [Tweepy](https://github.com/tweepy/tweepy) library. The dataset contains 299,432 tweets, 5 percent of these tweets are separated into a test set, the rest are in a training set.

According to privacy concerns, the dataset is not distributed to the public, because there is so much sensitive information in the dataset consisting of person names, politics, financial numbers, and etc. It is hard to completely standardize or remove all of that information.


### Dataset Creation
In order to prepare a dataset for this project, follow the instructions below:

##### 0. Clone this repo
```sh
git clone https://github.com/luangtatipsy/emogest.git
cd emogest
```

##### 1. Activate virtual environment (optional)
This project requires Python 3.8+
```sh
python -m venv env
source env/bin/activate
```

##### 2. Install requirements
```sh
pip install -r requirements
```

##### 3. Create .env
- Register a new Twitter project to get keys and secrets. See [documentation](https://developer.twitter.com/en/docs/authentication/guides/authentication-best-practices)
- Imitate [`.env.template`](https://github.com/luangtatipsy/emogest/blob/main/.env.template) and store all corresponding environment variables to .env
```sh
echo "TWITTER_API_KEY=<your_api_key>" >> .env
echo "TWITTER_API_KEY_SECRET=<your_api_key_secret>" >> .env
echo "TWITTER_ACCESS_TOKEN=<your_access_token>" >> .env
echo "TWITTER_ACCESS_TOKEN_SECERT=<your_access_token_secret>" >> .env
```

##### 4. Create a raw dataset
The dataset file will be created by [`create_dataset.py`](https://github.com/luangtatipsy/emogest/blob/main/create_dataset.py) script. The script will query tweets by each pre-defined emoji placed under [`data/labels.py`](https://github.com/luangtatipsy/emogest/blob/main/data/labels.py) file. The dataset file will be saved under `datasets` directory.
```sh
python create_dataset.py --num_tweets 10000 --output_file_path raw_data.csv
```

##### 5. Prepare the dataset
Serve [`notebooks/preparation.ipynb`](https://github.com/luangtatipsy/emogest/blob/main/notebooks/preparation.ipynb) and execute all blocks (you might need to change the code as you need). A prepared dataset will be saved under `datasets` directory.