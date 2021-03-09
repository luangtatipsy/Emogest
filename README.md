# Emogest
Preliminary ML model suggesting emojis given a short text. This project's objective is to demonstrate how to retrieve tweets from Twitter API and leverage the collected tweets as a dataset creating a preliminary text classification model in any certain tasks. For this demonstration, I selected the "Emoji Suggestion" task because it is one of the fastest tasks to auto-generate annotation for the collected tweets.

## Prerequisite
- Git
- Python 3.8.7
## Setup
0. Clone the repository
```sh
git clone https://github.com/luangtatipsy/emogest.git
cd emogest
```
1. Create and activate a virtual environment for Python _(recommended)_. If you do not prefer using a virtual environment, skip to step 4.
```sh
python -m venv env
source env/bin/activate
```
2. Update pip to latest version
```sh
python -m pip install --upgrade pip
```
3. Install requirements
```sh
python -m pip install -r requirements.txt
```

## Creating a dataset
This project dataset is collected at December 28, 2020 for each the following Emoji character [`labels.py`](https://github.com/luangtatipsy/emogest/blob/main/emogest/data/labels.py). for more detail please see the [documentation](https://github.com/luangtatipsy/emogest/blob/main/datasets/README.md)

## Training a Word Embedding Model
[`train-embedding.ipynb`](https://github.com/luangtatipsy/emogest/blob/main/train-embedding.ipynb) notebook is used to train the word embedding model with the collected data. The trained word embedding model will be used for vectorizing as a feature vector for training a classification model. Pre-trained word embedding model can be download [here](https://www.dropbox.com/s/25813myjjbe6mrm/tweet_embedding_256.model)

## Training a Classification Model
Gradient boosting classifier is selected for this task. A [`train-embedding.ipynb`](https://github.com/luangtatipsy/emogest/blob/main/train-embedding.ipynb) notebook is used to train the classifier with approximate 6-7 hour training time. Pre-trained classification model can be download [here](https://www.dropbox.com/s/t75hnpht8v3oljd/emoji_xgb.pipeline)

## Analyzing Results 
According to the result on [`result-analysis.ipynb`](https://github.com/luangtatipsy/emogest/blob/main/result-analysis.ipynb), According to the result on the script, at first sight, the model accuracy is around 20% which is not acceptable. Intuitively, it is because there are so many classes of Emoji to be classified (53 Emojis). Furthermore, tweets are not a sequence of words that express users' perspectives directly, there are Irony and pecky sentences that confuse the model. At the same time, several Emojis are close to each other by the meaning such as "😀" and "😁", "🥰" and  "😍", etc. It depends on the users' decision.

## Discussion
As the result analysis above I did not mention about the word embedding model yet, for the experiments, the word embedding model is quite well. It can appropriately query similar words by the meaning. For example, a word to be queried is "น่ารัก", and the model return top 3 similar words: "หล่อ", "สวย", and "เท่".

## License
This repository is distributed under [MIT License](https://github.com/luangtatipsy/intel-image-classification/blob/master/LICENSE)
