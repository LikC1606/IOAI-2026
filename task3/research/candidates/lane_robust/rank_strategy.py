"""Standalone bounded-rank policy for the PotatoPlayer contract.

The submission wrapper can copy this class body into the official starter.
It intentionally keeps every comparison as a bounded public sign vote, which
prevents one private/public order inversion from permanently deleting the
hidden word.
"""

import numpy as np


class RankSoftPlayer:
    def __init__(self, words, embeddings):
        self.words = words
        self.emb = embeddings
        self.word_to_index = {w.casefold(): i for i, w in enumerate(words)}
        self.sim = self.emb @ self.emb.T
        self.n = len(words)
        self.reliability = 0.65
        self.champion_weight = 3.0
        self.new_game()

    def new_game(self):
        self.logp = np.zeros(self.n, dtype=np.float32)
        self.used = np.zeros(self.n, dtype=bool)

    def respond(self, message):
        i1 = self.word_to_index[message["word1"].casefold()]
        i2 = self.word_to_index[message["word2"].casefold()]
        verdict = str(message["verdict"]).casefold()
        if verdict in ("first", "second"):
            better, worse = (
                (i1, i2) if verdict == "first" else (i2, i1)
            )
            margin = self.sim[:, better] - self.sim[:, worse]
            # Sign-only likelihood: public rank matters, but its fragile
            # magnitude cannot make a single contradiction irreversible.
            hi = 0.5 + 0.25 * self.reliability
            lo = 0.5 - 0.25 * self.reliability
            self.logp += np.log(np.where(margin >= 0.0, hi, lo))
        self.logp[self.used] = -1.0e9
        champion = self.word_to_index[message["winner_word"].casefold()]
        score = self.logp + self.champion_weight * self.sim[champion]
        score[self.used] = -1.0e9
        pick = int(np.argmax(score))
        self.used[pick] = True
        return self.words[pick]


if __name__ == "__main__":
    # Tiny contract smoke test; the official starter performs the full check.
    import json
    from pathlib import Path

    root = Path(__file__).resolve().parents[2]
    words = json.loads((root / "input/competition/vocabulary.json").read_text())
    emb = np.load(root / "input/competition/public_embeddings.npy")
    player = RankSoftPlayer(words, emb)
    player.new_game()
    out = player.respond(
        {
            "turn": 1,
            "word1": "lamp",
            "word2": "potato",
            "winner_word": "potato",
            "verdict": "second",
        }
    )
    assert out in words
    print("rank strategy OK:", out)
