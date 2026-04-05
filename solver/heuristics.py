"""Heuristic functions for word ladder search algorithms."""


def hamming_distance(word_a: str, word_b: str) -> int:
    """Return the number of positions where characters differ between two words.

    This is an admissible heuristic for the word ladder problem: you need
    at least one step per differing character, so it never overestimates.
    """
    if len(word_a) != len(word_b):
        raise ValueError(
            f"Words must be the same length: '{word_a}' ({len(word_a)}) "
            f"vs '{word_b}' ({len(word_b)})"
        )
    return sum(a != b for a, b in zip(word_a, word_b))
