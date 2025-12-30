"""Vigenère cipher helpers.

Improved implementation: unified function, preserves case, validates keyword, and includes basic examples/tests.
"""
from itertools import cycle
import string
from typing import Iterable


def _validate_keyword(keyword: str) -> str:
    """Return a lowercase keyword after validation.

    Keyword must be a non-empty alphabetic ASCII string.
    """
    if not isinstance(keyword, str) or not keyword:
        raise ValueError("Keyword must be a non-empty string")
    if not keyword.isalpha() or not all(c.isascii() for c in keyword):
        raise ValueError("Keyword must contain only ASCII letters")
    return keyword.lower()


def _shift_char(character: str, key_char: str, encode: bool = True) -> str:
    """Shift a single ASCII letter by key_char preserving case.

    If encode is True, shift forward (encrypt); if False, shift backward (decrypt).
    """
    base = ord("A") if character.isupper() else ord("a")
    ch_idx = ord(character) - base
    key_idx = ord(key_char) - ord("a")
    if encode:
        new_idx = (ch_idx + key_idx) % 26
    else:
        new_idx = (ch_idx - key_idx) % 26
    return chr(base + new_idx)


def vigenere(message: str, keyword: str, encode: bool = True) -> str:
    """Apply the Vigenère cipher to `message` using `keyword`.

    - `encode=True` for encryption, `False` for decryption.
    - Preserves letter case and leaves non-ASCII-letter characters unchanged.
    - Validates the keyword (must be alphabetic ASCII).
    """
    keyword = _validate_keyword(keyword)
    result = []
    key_iter = cycle(keyword)

    for ch in message:
        if ch.isalpha() and ch.isascii():
            k = next(key_iter)
            result.append(_shift_char(ch, k, encode))
        else:
            result.append(ch)

    return "".join(result)


def vigenere_encode(message: str, keyword: str) -> str:
    """Convenience wrapper to encrypt a message."""
    return vigenere(message, keyword, encode=True)


def vigenere_decode(message: str, keyword: str) -> str:
    """Convenience wrapper to decrypt a message."""
    return vigenere(message, keyword, encode=False)


if __name__ == "__main__":
    # Example: decrypt a known ciphertext
    vigenere_message = (
        "txm srom vkda gl lzlgzr qpdb? fepb ejac! ubr imn tapludwy mhfbz cza ruxzal wg zztcgcexxch!"
    )
    vigenere_keyword = "friends"
    print(vigenere_decode(vigenere_message, vigenere_keyword))

    # Example: encrypt and verify round-trip
    vigenere_message_for_v = (
        "thanks for teaching me all these cool ciphers! you really are the best!"
    )
    keyword_for_v = "besties"

    encrypted = vigenere_encode(vigenere_message_for_v, keyword_for_v)
    print(encrypted)

    assert vigenere_decode(encrypted, keyword_for_v) == vigenere_message_for_v
    print("Round-trip OK ✅")
