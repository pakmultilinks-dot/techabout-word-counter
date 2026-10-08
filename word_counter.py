#!/usr/bin/env python3
"""
Word Counter
============

Reads a plain-text file and shows the 20 most frequent words in it.

Counting rules:
  - Case-insensitive: "Tech" and "tech" count as the same word.
  - A word is a run of letters and digits (unicode-aware); punctuation,
    whitespace, and symbols are separators, not words.
  - Words shorter than --min-length (default 1) are ignored.
  - Words in --stop-words (a comma-separated list, or a file with one word
    per line via --stop-words-file) are excluded from the ranking.

Output formats: human-readable text (default), CSV, or JSON.

Usage:
    python word_counter.py sample.txt
    python word_counter.py sample.txt --top 10
    python word_counter.py sample.txt --min-length 3 --stop-words the,and,of
    python word_counter.py sample.txt --format json --output result.json

TechAbout Python Developer task 2 - Word Counter (ZR-26-00754).
"""

import argparse
import csv
import io
import json
import re
import sys
from collections import Counter

# letters and digits, unicode-aware; apostrophes inside words are kept
# (e.g. "don't" stays one word) and then stripped of the apostrophe.
WORD_RE = re.compile(r"[^\W_]+(?:'[^\W_]+)*", re.UNICODE)


def tokenize(text):
    """Split text into lowercase words."""
    words = []
    for match in WORD_RE.finditer(text.lower()):
        word = match.group(0).replace("'", "")
        if word:
            words.append(word)
    return words


def load_stop_words(args):
    stop = set()
    if args.stop_words:
        stop.update(w.strip().lower() for w in args.stop_words.split(",") if w.strip())
    if args.stop_words_file:
        try:
            with open(args.stop_words_file, "r", encoding="utf-8") as fh:
                stop.update(line.strip().lower() for line in fh if line.strip())
        except FileNotFoundError:
            print("Error: stop-words file not found: %s" % args.stop_words_file,
                  file=sys.stderr)
            sys.exit(1)
    return stop


def count_words(text, min_length=1, stop_words=None):
    """Return a Counter of words in text, honoring filters."""
    stop_words = stop_words or set()
    counter = Counter()
    for word in tokenize(text):
        if len(word) < min_length:
            continue
        if word in stop_words:
            continue
        counter[word] += 1
    return counter


def top_words(counter, n=20):
    """Return the top n (word, count) pairs, ties broken alphabetically."""
    ranked = sorted(counter.items(), key=lambda kv: (-kv[1], kv[0]))
    return ranked[:n]


def to_text(ranked, total_words, unique_words, n):
    lines = []
    lines.append("Top %d most frequent words" % n)
    lines.append("Total words: %d | Unique words: %d" % (total_words, unique_words))
    lines.append("")
    width = max((len(w) for w, _ in ranked), default=4)
    for i, (word, count) in enumerate(ranked, 1):
        lines.append("%2d. %-*s  %d" % (i, width, word, count))
    return "\n".join(lines)


def to_csv(ranked):
    buf = io.StringIO()
    writer = csv.writer(buf)
    writer.writerow(["rank", "word", "count"])
    for i, (word, count) in enumerate(ranked, 1):
        writer.writerow([i, word, count])
    return buf.getvalue()


def to_json(ranked, total_words, unique_words, n):
    return json.dumps({
        "top_n": n,
        "total_words": total_words,
        "unique_words": unique_words,
        "words": [{"rank": i, "word": w, "count": c}
                  for i, (w, c) in enumerate(ranked, 1)],
    }, indent=2, ensure_ascii=False)


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Show the most frequent words in a text file.")
    parser.add_argument("text_file", help="Path to the plain-text file")
    parser.add_argument("--top", type=int, default=20,
                        help="How many words to show (default: 20)")
    parser.add_argument("--min-length", type=int, default=1,
                        help="Ignore words shorter than this (default: 1)")
    parser.add_argument("--stop-words", default="",
                        help="Comma-separated words to exclude, e.g. the,and,of")
    parser.add_argument("--stop-words-file", default="",
                        help="File with one stop word per line")
    parser.add_argument("--format", choices=["text", "csv", "json"],
                        default="text", help="Output format (default: text)")
    parser.add_argument("--output", default="",
                        help="Write output to this file instead of stdout")
    args = parser.parse_args(argv)

    if args.top < 1:
        print("Error: --top must be at least 1", file=sys.stderr)
        return 1

    try:
        with open(args.text_file, "r", encoding="utf-8") as fh:
            text = fh.read()
    except FileNotFoundError:
        print("Error: file not found: %s" % args.text_file, file=sys.stderr)
        return 1
    except UnicodeDecodeError:
        with open(args.text_file, "r", encoding="utf-8", errors="replace") as fh:
            text = fh.read()

    stop_words = load_stop_words(args)
    counter = count_words(text, args.min_length, stop_words)
    ranked = top_words(counter, args.top)
    total_words = sum(counter.values())

    if args.format == "csv":
        out = to_csv(ranked)
    elif args.format == "json":
        out = to_json(ranked, total_words, len(counter), args.top)
    else:
        out = to_text(ranked, total_words, len(counter), args.top)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as fh:
            fh.write(out)
        print("Wrote top %d words to %s" % (len(ranked), args.output))
    else:
        print(out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
