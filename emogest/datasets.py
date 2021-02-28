from typing import Tuple

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split


class Dataset:
    def __init__(
        self, df: pd.DataFrame, x_column: str, y_column: str, test_size: float
    ) -> None:
        self.df = df
        self.x_column = x_column
        self.y_column = y_column

        (
            self.chars,
            self.emojis,
            self.char_to_idx,
            self.emoji_to_idx,
            self.max_sequence_len,
        ) = self.generate_config(self.x_column, self.y_column)

        self.training_set, self.test_set = self.split(test_size)

        self.training_set_size = self.training_set.shape[0]
        self.test_set_size = self.test_set.shape[0]

    def generate_config(
        self, x_column: str, y_column: str
    ) -> Tuple[list, list, dict, dict, int]:
        chars = list(sorted(set(char for tweet in self.df[x_column] for char in tweet)))
        emojis = list(sorted(set(self.df[y_column])))

        char_to_idx = {char: idx for idx, char in enumerate(chars)}
        emoji_to_idx = {em: idx for idx, em in enumerate(emojis)}

        max_sequence_len = self.df[x_column].str.len().max()

        return chars, emojis, char_to_idx, emoji_to_idx, max_sequence_len

    def split(self, test_size: float) -> Tuple[pd.DataFrame, pd.DataFrame]:
        training_set, test_set = train_test_split(
            self.df,
            test_size=test_size,
            stratify=self.df[self.y_column],
            random_state=0,
        )
        return training_set, test_set

    def generate_train_data(self, batch_size: int = 512):
        while True:
            yield self._generate(self.training_set, batch_size)

    def generate_test_data(self, batch_size: int = 512):
        while True:
            yield self._generate(self.test_set, batch_size)

    def _generate(self, df: pd.DataFrame, batch_size: int):
        batch = df.sample(batch_size)

        X = np.zeros((batch_size, self.max_sequence_len, len(self.chars)))
        y = np.zeros((batch_size,))

        for r_i, idx in enumerate(batch.index):
            row = batch.loc[idx]

            y[r_i] = self.emoji_to_idx.get(row[self.y_column])
            for c_i, char in enumerate(row[self.x_column]):
                X[r_i, c_i, self.char_to_idx[char]] = 1

        return X, y
