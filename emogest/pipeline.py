import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, ClassifierMixin, TransformerMixin

from emogest.preprocessing import preprocess as e_preprocess
from emogest.tokenizer import tokenize as e_tokenize


class ThaiPreprocessor(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None, **fit_params):
        return self

    def preprocess(self, text: str) -> str:
        return e_preprocess(text)

    def transform(self, X) -> pd.Series:
        return pd.Series(X).apply(self.preprocess)


class ThaiTokenizer(BaseEstimator, TransformerMixin):
    def __init__(self, remove_entities: bool = False, keep_whitespace: bool = False):
        self.remove_entities = remove_entities
        self.keep_whitespace = keep_whitespace

    def fit(self, X, y=None, **fit_params):
        return self

    def tokenize(self, text):
        tokens = e_tokenize(
            text,
            remove_entities=self.remove_entities,
            keep_whitespace=self.keep_whitespace,
        )

        return tokens

    def transform(self, X) -> pd.Series:
        return pd.Series(X).apply(self.tokenize)


class MeanEmbeddingVectorizer:
    def __init__(self, w2v_model):
        self.word2vec = dict(zip(w2v_model.wv.index2word, w2v_model.wv.syn0))
        self.dim = w2v_model.vector_size

    def fit(self, X, y=None, **fit_params):
        return self

    def transform(self, X) -> np.ndarray:
        return np.array(
            [
                np.mean(
                    [self.word2vec[word] for word in words if word in self.word2vec]
                    or [np.zeros(self.dim)],
                    axis=0,
                )
                for words in X
            ]
        )
