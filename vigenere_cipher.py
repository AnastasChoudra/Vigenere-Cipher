"""Vigenère cipher module with CLI support."""

from itertools import cycle
import argparse
from typing import Iterable


def _validate_keyword(keyword: str) -> str:
    if not isinstance(keyword, str) or not keyword:
        raise ValueError("Keyword must be a non-empty string")
    if not keyword.isalpha() or not all(c.isascii() for c in keyword):
        raise ValueError("Keyword must contain only ASCII letters")
    return keyword.lower()


def _shift_char(character: str, key_char: str, encode: bool = True) -> str:
    base = ord("A") if character.isupper() else ord("a")
    ch_idx = ord(character) - base
    key_idx = ord(key_char) - ord("a")
    if encode:
        new_idx = (ch_idx + key_idx) % 26
    else:
        new_idx = (ch_idx - key_idx) % 26
    return chr(base + new_idx)


def vigenere(message: str, keyword: str, encode: bool = True) -> str:
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
    return vigenere(message, keyword, encode=True)


def vigenere_decode(message: str, keyword: str) -> str:
    return vigenere(message, keyword, encode=False)


def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Vigenère cipher tool")
    grp = p.add_mutually_exclusive_group(required=True)
    grp.add_argument("--encode", "-e", action="store_true", help="Encode the message")
    grp.add_argument("--decode", "-d", action="store_true", help="Decode the message")

    p.add_argument("--keyword", "-k", required=True, help="Alphabetic keyword")
    p.add_argument("--message", "-m", help="Message to process; if omitted reads stdin")
    return p


def main(argv=None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    if args.message is None:
        import sys

        message = sys.stdin.read()
    else:
        message = args.message

    try:
        if args.encode:
            out = vigenere_encode(message, args.keyword)
        else:
            out = vigenere_decode(message, args.keyword)
    except ValueError as exc:
        print(f"Error: {exc}")
        return 2

    print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
