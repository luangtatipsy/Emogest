import html

from th_preprocessor.preprocess import (
    insert_spaces,
    normalize_at_mention,
    normalize_email,
    normalize_emoji,
    normalize_haha,
    normalize_link,
    normalize_num,
    normalize_phone,
    normalize_text_pairs,
    remove_dup_spaces,
    remove_others_char,
    remove_tag,
)

# Add prefix 'ES' to all placeholders
REPLACE_LINK = " EGLINK "
REPLACE_EMAIL = " EGEMAIL "
REPLACE_AT_MENTION = " EGNAME "
REPLACE_HAHA = " EGHAHA "
REPLACE_NUMBER = " EGNUMBER "
REPLACE_PHONE = " EGPHONE "
REPLACE_DATE = " EGDATE "


def preprocess(text: str):
    text = text.lower()

    text = html.unescape(text)
    text = remove_tag(text)

    text = normalize_link(text, place_holder=REPLACE_LINK)
    text = normalize_at_mention(text, place_holder=REPLACE_AT_MENTION)
    text = normalize_email(text, place_holder=REPLACE_EMAIL)
    text = normalize_phone(text, place_holder=REPLACE_PHONE)
    text = normalize_text_pairs(text)
    text = normalize_haha(text, place_holder=REPLACE_LINK)
    text = normalize_num(text, place_holder=REPLACE_NUMBER)

    text = remove_others_char(text)

    text = insert_spaces(text)
    text = remove_dup_spaces(text)

    return text
