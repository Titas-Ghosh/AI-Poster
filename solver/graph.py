"""Dictionary loading and adjacency graph construction for the word ladder."""

from collections import defaultdict
from pathlib import Path


class WordGraph:
    """Graph where words are nodes and edges connect words differing by one letter."""

    def __init__(self, dictionary_path: str = "data/dictionary.txt"):
        self.words: set[str] = set()
        self.graph: dict[str, list[str]] = defaultdict(list)
        self.words_by_length: dict[int, set[str]] = defaultdict(set)
        self._load_words(dictionary_path)
        self._build_graph()

    def _load_words(self, path: str) -> None:
        """Read words from file, keep only lowercase alphabetic 3-5 letter words."""
        filepath = Path(path)
        if not filepath.exists():
            raise FileNotFoundError(f"Dictionary file not found: {path}")

        with open(filepath, "r", encoding="utf-8") as f:
            for line in f:
                word = line.strip().lower()
                if 3 <= len(word) <= 5 and word.isalpha():
                    self.words.add(word)
                    self.words_by_length[len(word)].add(word)

    def _build_graph(self) -> None:
        """Build adjacency list using pattern-based bucketing.

        For each word, generate wildcard patterns by replacing each character
        with '_'. Words sharing a pattern are neighbors (differ by one letter).
        """
        buckets: dict[str, list[str]] = defaultdict(list)

        for word in self.words:
            for i in range(len(word)):
                pattern = word[:i] + "_" + word[i + 1:]
                buckets[pattern].append(word)

        # Words in the same bucket are mutual neighbors
        for bucket_words in buckets.values():
            for i, w1 in enumerate(bucket_words):
                for w2 in bucket_words[i + 1:]:
                    self.graph[w1].append(w2)
                    self.graph[w2].append(w1)

    def get_neighbors(self, word: str) -> list[str]:
        """Return all words that differ from the given word by exactly one letter."""
        return self.graph.get(word, [])

    def has_word(self, word: str) -> bool:
        """Check if a word exists in the dictionary."""
        return word in self.words
