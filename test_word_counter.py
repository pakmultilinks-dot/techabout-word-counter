"""Tests for word_counter.py"""
import json
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(__file__))
from word_counter import count_words, tokenize, top_words, to_csv, to_json, to_text

SAMPLE = "Tech tech TECH! AI, ai. don't stop: don't-stop. 123 test test."


class TestWordCounter(unittest.TestCase):
    def test_case_insensitive(self):
        counter = count_words(SAMPLE)
        self.assertEqual(counter["tech"], 3)
        self.assertEqual(counter["ai"], 2)

    def test_punctuation_is_separator(self):
        counter = count_words(SAMPLE)
        self.assertNotIn("tech!", counter)
        self.assertEqual(counter["stop"], 2)

    def test_apostrophe_kept_as_one_word(self):
        counter = count_words(SAMPLE)
        self.assertEqual(counter["dont"], 2)

    def test_hyphen_splits(self):
        counter = count_words(SAMPLE)
        self.assertEqual(counter["stop"], 2)  # "stop" and "don't-stop" -> stop

    def test_digits_count_as_words(self):
        counter = count_words(SAMPLE)
        self.assertEqual(counter["123"], 1)

    def test_min_length_filter(self):
        counter = count_words(SAMPLE, min_length=3)
        self.assertNotIn("ai", counter)
        self.assertIn("tech", counter)

    def test_stop_words_excluded(self):
        counter = count_words(SAMPLE, stop_words={"tech", "ai"})
        self.assertNotIn("tech", counter)
        self.assertNotIn("ai", counter)
        self.assertIn("test", counter)

    def test_top_n_limit(self):
        counter = count_words(SAMPLE)
        ranked = top_words(counter, 3)
        self.assertEqual(len(ranked), 3)

    def test_ranking_order_count_then_alpha(self):
        counter = count_words("b a b a c")
        ranked = top_words(counter, 3)
        self.assertEqual(ranked[0], ("a", 2))
        self.assertEqual(ranked[1], ("b", 2))  # tie -> alphabetical
        self.assertEqual(ranked[2], ("c", 1))

    def test_empty_text(self):
        counter = count_words("")
        self.assertEqual(len(counter), 0)
        self.assertEqual(top_words(counter, 20), [])

    def test_tokenize_unicode(self):
        words = tokenize("Café naïve résumé")
        self.assertEqual(words, ["café", "naïve", "résumé"])

    def test_text_output_format(self):
        ranked = top_words(count_words(SAMPLE), 3)
        out = to_text(ranked, 12, 6, 3)
        self.assertIn("Top 3 most frequent words", out)
        self.assertIn("tech", out)

    def test_csv_output(self):
        ranked = top_words(count_words(SAMPLE), 2)
        lines = to_csv(ranked).strip().splitlines()
        self.assertEqual(lines[0], "rank,word,count")
        self.assertEqual(len(lines), 3)

    def test_json_output(self):
        ranked = top_words(count_words(SAMPLE), 2)
        data = json.loads(to_json(ranked, 12, 6, 2))
        self.assertEqual(data["top_n"], 2)
        self.assertEqual(len(data["words"]), 2)
        self.assertEqual(data["words"][0]["rank"], 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
