from typing import List

from newmm_tokenizer.tokenizer import word_tokenize


def tokenize(
    text: str, remove_entities: bool = False, keep_whitespace: bool = False
) -> List[str]:
    tokens = word_tokenize(text=text, keep_whitespace=keep_whitespace)
    if remove_entities:
        tokens = [token for token in tokens if not token.strip().startswith("EG")]

    return tokens
