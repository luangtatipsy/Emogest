import argparse
import json
import os

import pandas as pd
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.layers import Input
from tensorflow.keras.models import Model

from emogest.datasets import Dataset
from emogest.models import CharCNN

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--path_to_input_file",
        type=str,
        default="prepared_data.csv",
        help="path to input CSV file",
    )

    parser.add_argument(
        "--x_column",
        type=str,
        default="tweet",
        help="column name of messages",
    )

    parser.add_argument(
        "--y_column",
        type=str,
        default="emoji",
        help="column name of label",
    )

    parser.add_argument(
        "--epochs",
        type=int,
        default=50,
        help="number of epochs",
    )

    parser.add_argument(
        "--batch_size",
        type=int,
        default=512,
        help="batch size",
    )

    dataset_dir = "datasets"
    model_dir = "models"

    args = parser.parse_args()
    path_to_input_file = args.path_to_input_file
    x_column = args.x_column
    y_column = args.y_column
    epochs = args.epochs
    batch_size = args.batch_size

    tweets = pd.read_csv(os.path.join(dataset_dir, path_to_input_file))

    dataset = Dataset(df=tweets, x_column=x_column, y_column=y_column, test_size=0.1)

    char_cnn = CharCNN(len(dataset.emojis))
    char_input = Input(
        shape=(dataset.max_sequence_len, len(dataset.chars)), name="char_cnn_input"
    )
    outputs = char_cnn(char_input)

    model = Model(inputs=char_input, outputs=outputs)
    model.compile(
        loss="sparse_categorical_crossentropy", optimizer="rmsprop", metrics=["acc"]
    )
    print(model.summary())

    early_stopping = EarlyStopping(
        monitor="loss", min_delta=0.03, patience=2, verbose=0, mode="auto"
    )

    print("Start fitting a model...\n")
    model.fit(
        dataset.generate_train_data(batch_size=batch_size),
        epochs=epochs,
        steps_per_epoch=dataset.training_set_size / batch_size,
        verbose=1,
        callbacks=[early_stopping],
    )

    print("Start evaluating the trained model...\n")
    results = model.evaluate(
        dataset.generate_test_data(batch_size=batch_size),
        steps=dataset.test_set_size / batch_size,
    )
    print(f"{results}\n")

    config_file_path = os.path.join(model_dir, "char_cnn_config.json")
    model_h5_file_path = os.path.join(model_dir, "char_cnn_model.h5")
    model_h5_weights_file_path = os.path.join(model_dir, "char_cnn_model_weights.h5")

    with open(config_file_path, "w") as f:
        json.dump(
            {
                "emojis": "".join(dataset.emojis),
                "char_to_idx": dataset.char_to_idx,
                "max_sequence_len": dataset.max_sequence_len,
            },
            f,
        )
    model.save(model_h5_file_path)
    model.save_weights(model_h5_weights_file_path)

    print(
        f"""
        The model files have been saved to...
        {model_h5_weights_file_path}
        {config_file_path}
        {model_h5_file_path}
        """
    )
