from newmm_tokenizer.tokenizer import word_tokenize


def tokenize(text: str, remove_entities: bool = False):
    tokens = word_tokenize(text=text, keep_whitespace=False)
    if remove_entities:
        tokens = [token for token in tokens if not token.strip().startswith("EG")]

    return tokens
