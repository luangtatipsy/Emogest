from typing import Tuple

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split


class Dataset:
    def __init__(
        self, df: pd.DataFrame, y_column: str, test_size: float
    ) -> None:
        self.df = df
        self.y_column = y_column

        self.training_set, self.test_set = self.split(test_size)

    def split(self, test_size: float) -> Tuple[pd.DataFrame, pd.DataFrame]:
        training_set, test_set = train_test_split(
            self.df,
            test_size=test_size,
            stratify=self.df[self.y_column],
            random_state=0,
        )
        return training_set, test_set
