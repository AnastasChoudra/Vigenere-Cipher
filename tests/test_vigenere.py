import pytest
from vigenere_cipher import vigenere_encode, vigenere_decode, vigenere


def test_round_trip_simple():
    msg = "Hello World"
    kw = "key"
    enc = vigenere_encode(msg, kw)
    assert vigenere_decode(enc, kw) == msg


def test_case_preservation():
    msg = "AbC xYz"
    kw = "Key"
    enc = vigenere_encode(msg, kw)
    # Ensure case is preserved in encoded text
    assert enc[0].isupper() and enc[1].islower()
    assert vigenere_decode(enc, kw) == msg


def test_non_alpha_unchanged():
    msg = "hi! 123?"
    kw = "a"
    assert vigenere_encode(msg, kw) == msg


def test_keyword_validation():
    with pytest.raises(ValueError):
        vigenere("abc", "")
    with pytest.raises(ValueError):
        vigenere("abc", "k3y")


def test_known_example():
    # This ciphertext was produced by the original example (which uses the reversed
    # encode/decode convention), so we verify using encode=True to match that behavior.
    cipher = vigenere(
        "txm srom vkda gl lzlgzr qpdb? fepb ejac! ubr imn tapludwy mhfbz cza ruxzal wg zztcgcexxch!",
        "friends",
        encode=True,
    )
    assert "you were able to decode this" in cipher
