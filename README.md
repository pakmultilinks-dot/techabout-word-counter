# Word Counter

A small Python script that reads a plain-text file and shows the 20 most
frequent words in it. Built for TechAbout task 2 (ZR-26-00754).

## What it does

Given a `.txt` file, it counts every word and prints the top 20, with options:

- Case-insensitive counting ("Tech" and "tech" are the same word)
- Unicode-aware word splitting; punctuation and symbols are separators
- `--top N`: show a different number of words (default 20)
- `--min-length N`: ignore very short words
- `--stop-words` / `--stop-words-file`: exclude common words from the ranking
- Ties are broken alphabetically so output is deterministic

Output formats: `text` (default), `csv`, `json`.

## Usage

```bash
python word_counter.py sample.txt
python word_counter.py sample.txt --top 10
python word_counter.py sample.txt --min-length 3 --stop-words the,and,of
python word_counter.py sample.txt --format json --output result.json
```

## Sample output

`sample/` contains the visible text of the public TechAbout homepage
(`techabout-homepage.txt`, saved 8 Oct 2026) and the word-count output in
all three formats:

- `output.txt`: top 20 words (1,369 total words, 663 unique)
- `output.csv`: spreadsheet-friendly table
- `output.json`: machine-readable result

## Tests

```bash
python test_word_counter.py
```

14 tests covering case-insensitivity, punctuation handling, apostrophes,
hyphens, digits, unicode words, min-length and stop-word filters, ranking
order, ties, empty input, and all three output formats.

## Files

| File | Purpose |
|---|---|
| `word_counter.py` | The script |
| `test_word_counter.py` | 14 unit tests |
| `sample/techabout-homepage.txt` | Public sample text used for the demo |
| `sample/output.txt` / `.csv` / `.json` | Sample output in three formats |
