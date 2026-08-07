# Technical report (baseline version). This solution treats Potato Contact as a
# sequential semantic comparison search over the 1,602 legal vocabulary words.
# The judge retains the winner of the current champion/proposal comparison and
# returns a verdict, so the player carries a boolean feasible set through turns.
#
# For each `first` or `second` verdict, the implementation intersects the set
# with the corresponding public-embedding half-space: a possible secret should
# be at least as similar to the retained word as to the rejected word. `same`
# leaves the set unchanged. Already proposed words are removed so every response
# remains a fresh legal guess.
#
# The next proposal is the surviving vocabulary word with greatest public cosine
# similarity to the current winner. This is a cheap champion-neighbor walk: the
# full public similarity matrix is computed once in `__init__`, while each turn
# is a vectorized masked argmax. The public matrix is only a proxy because the
# official judge uses a separate private embedding space; this baseline therefore
# records a high public score but makes no claim that its ordering transfers.
#
# On `test_public.json`, the unchanged starter solved 119 of 120 games and scored
# 92.58/100. The turn histogram had 62 wins by turn 10 (the full-reward region),
# median winning/miss turn 10, and one unsolved secret (`kettle`). The official
# leaderboard score for this first submission is pending; the expected public to
# private gap is a central diagnostic rather than a tuning target.
#
# The 600-second grader budget is spent almost entirely in one-time loading and
# the 1602-by-1602 public dot-product matrix; gameplay itself is sub-second on
# CPU. No external data, model, network, or non-standard dependency is used.
# Later candidates test soft verdict likelihoods and balanced query selection;
# they are not included here until they pass exact contract and runtime checks.

# ─── IOAI 2026 — Potato Contact starter ────────────────────────────────────────
# This ONE file does two jobs. Which job runs depends on where it runs.
#
#   1. On Kaggle (`kaggle kernels push`), /kaggle/working exists, so the block at
#      the bottom base64-encodes THIS ENTIRE FILE into submission.csv. That is
#      all the kernel does. It trains nothing and predicts nothing: the CSV is
#      only a transport envelope for your source code.
#
#   2. Inside the grader, this file is NOT run as a program. It is IMPORTED as a
#      Python module, so your `if __name__ == "__main__":` block never runs
#      there. The grader calls these two names directly, by exact spelling:
#
#          load_public_data() -> (words, embeddings)    # called once per round
#
#          class PotatoPlayer:
#              def __init__(self, words, embeddings)    # once per round
#              def new_game(self)                       # before each game
#              def respond(self, message) -> str        # RETURN a word each turn
#
#      There is no stdin, no stdout protocol, and no JSON on the wire.
#      `respond()` RETURNS a plain str; it does not print anything.
#
# Edit the BODY of PotatoPlayer. Keep those four signatures intact: renaming
# either name, or changing the number of arguments, fails every game in a round.
#
# Run this file locally (`python ioai-starter.py`) to check the contract and
# self-score. Do it before every submission: a kernel push succeeds regardless
# of your interface, so a mistake only shows up after you have spent one.
# ───────────────────────────────────────────────────────────────────────────────

import json
import os
import sys
from pathlib import Path

import numpy as np


def load_public_data():
    """Return (words, embeddings). The grader calls this once per round.

    words      : list[str], length 1602
    embeddings : np.ndarray (1602, 2560), L2-normalized, row i is words[i]

    The grader imports this file from a temporary directory and sets
    POTATO_DATA_DIR, so the data is found by environment variable or by
    searching /kaggle/input rather than by a relative path. Keep that search
    intact: a hard-coded path that works in your notebook will not exist inside
    the grader.
    """
    candidates = []
    env_dir = os.environ.get("POTATO_DATA_DIR")
    if env_dir:
        candidates.append(Path(env_dir))
    candidates += sorted(Path("/kaggle/input").rglob("vocabulary.json"))
    candidates.append(Path(__file__).resolve().parent)
    candidates.append(Path("dataset"))
    candidates.append(Path("data"))

    for candidate in candidates:
        directory = candidate.parent if candidate.is_file() else candidate
        vocabulary = directory / "vocabulary.json"
        embeddings = directory / "public_embeddings.npy"
        if vocabulary.is_file() and embeddings.is_file():
            words = json.loads(vocabulary.read_text())
            matrix = np.load(embeddings).astype(np.float32, copy=False)
            norms = np.linalg.norm(matrix, axis=1, keepdims=True)
            norms[norms == 0] = 1.0
            return words, matrix / norms
    raise FileNotFoundError("could not find vocabulary.json + public_embeddings.npy")


# ─── Your solution — edit this class ──────────────────────────────────────────
# The grader constructs this ONCE per leaderboard round and reuses the same
# instance for all 120 games in that round, calling new_game() between games.
# Expensive precomputation belongs in __init__ so it happens once.
class PotatoPlayer:
    def __init__(self, words, embeddings):
        """Called once per round as PotatoPlayer(words, embeddings).

        Keep exactly these two parameters. The grader passes both positionally.
        """
        self.words = words                                  # 1602 words
        self.emb = embeddings                               # (1602, 2560), L2-normalized
        self.word_to_index = {w.casefold(): i for i, w in enumerate(words)}

        # Cosine similarity between every pair of words, computed once (~0.01s).
        # These are the PUBLIC embeddings. The judge uses a different, private
        # space, so this is an approximation - a good strategy tolerates
        # disagreement rather than trusting this ordering blindly.
        self.sim = self.emb @ self.emb.T

        self.new_game()

    def new_game(self):
        """Called by the grader before each of the 120 games.

        Reset per-game state here. Keep anything expensive from __init__.
        """
        self.candidates = np.ones(len(self.words), dtype=bool)
        self.proposed = set()

    def respond(self, message):
        """RETURN one vocabulary word as a str. Called once per turn, up to 30.

        `message` is a plain Python dict, already parsed:

            message = {
                "turn":        1..30,
                "word1":       the reigning champion (on turn 1: "lamp"),
                "word2":       your previous proposal (on turn 1: "potato"),
                "verdict":     "first" | "second" | "same",
                "winner_word": whichever of word1/word2 the judge kept,
            }

        "first" means word1 is closer to the hidden word, "second" means word2
        is. On "same" the judge keeps word1.

        The returned word must appear in `self.words` (matched case-insensitively).
        Returning anything else, or raising, fails the current game AND every
        remaining game in the round.
        """
        i1 = self.word_to_index[message["word1"].casefold()]
        i2 = self.word_to_index[message["word2"].casefold()]
        verdict = str(message["verdict"]).casefold()

        # Use the comparison to rule out words the answer cannot be: if word1
        # beat word2, the hidden word should be at least as close to word1.
        if verdict in ("first", "second"):
            better, worse = (i1, i2) if verdict == "first" else (i2, i1)
            self.candidates &= self.sim[better] >= self.sim[worse]

        for index in self.proposed:
            self.candidates[index] = False

        # Never propose nothing: if the filter eliminated everything, start over
        # from all unproposed words.
        if not self.candidates.any():
            self.candidates = np.ones(len(self.words), dtype=bool)
            for index in self.proposed:
                self.candidates[index] = False
            if not self.candidates.any():
                return self.words[0]

        champion = self.word_to_index[message["winner_word"].casefold()]
        alive = np.flatnonzero(self.candidates)
        pick = int(alive[np.argmax(self.sim[champion][alive])])
        self.proposed.add(pick)
        return self.words[pick]


# ─── Contract self-check — do not edit ────────────────────────────────────────
# Mirrors exactly what the grader does when it imports your file. Runs during
# your Kaggle kernel, so an interface mistake stops the push instead of costing
# you a submission.
def check_contract():
    """Raise SystemExit with a clear message if the grader could not run this file."""
    import inspect

    # globals() rather than sys.modules[__name__]: when this file is imported
    # by path (as the grader does) it may not be registered in sys.modules.
    module = sys.modules.get(__name__)
    namespace = vars(module) if module is not None else globals()

    loader = namespace.get("load_public_data")
    if not callable(loader):
        raise SystemExit(
            "CONTRACT ERROR: this file must define a function load_public_data(). "
            "The grader calls it as: words, embeddings = load_public_data()"
        )

    player_class = namespace.get("PotatoPlayer")
    if not isinstance(player_class, type):
        raise SystemExit(
            "CONTRACT ERROR: this file must define a class PotatoPlayer. "
            "The grader calls it as: player = PotatoPlayer(words, embeddings)"
        )

    for name in ("new_game", "respond"):
        if not callable(getattr(player_class, name, None)):
            raise SystemExit(
                f"CONTRACT ERROR: PotatoPlayer must define a method {name}(). "
                "The grader calls new_game() before each game and respond(message) each turn."
            )

    # __init__ must accept (self, words, embeddings) positionally.
    try:
        signature = inspect.signature(player_class.__init__)
        signature.bind(None, ["w"], np.zeros((1, 2), dtype=np.float32))
    except TypeError as error:
        raise SystemExit(
            f"CONTRACT ERROR: PotatoPlayer.__init__ must accept exactly two "
            f"arguments after self: (words, embeddings). Python says: {error}"
        ) from None

    print("contract OK: load_public_data() + PotatoPlayer(words, embeddings)")


# ─── Local practice judge — do not edit ───────────────────────────────────────
# Drives your player exactly the way the grader does, but judges with the PUBLIC
# embeddings instead of the private ones. Scores here run much higher than the
# leaderboard; use it to catch crashes and protocol mistakes, not to predict rank.
START_WORD_1 = "lamp"
START_WORD_2 = "potato"
MAX_TURNS = 30
FREE_TURNS = 10
PENALTY = 0.02


def play_one_game(player, secret, words, embeddings, word_to_index):
    """Play a single game against the public-embedding judge. Returns the score."""
    player.new_game()
    secret_vector = embeddings[word_to_index[secret.casefold()]]
    word1, word2 = START_WORD_1, START_WORD_2

    for turn in range(1, MAX_TURNS + 1):
        first = float(secret_vector @ embeddings[word_to_index[word1.casefold()]])
        second = float(secret_vector @ embeddings[word_to_index[word2.casefold()]])
        if abs(first - second) <= 1e-12:
            winner_word, verdict = word1, "same"
        elif first > second:
            winner_word, verdict = word1, "first"
        else:
            winner_word, verdict = word2, "second"

        proposal = player.respond({
            "turn": turn,
            "winner_word": winner_word,
            "verdict": verdict,
            "word1": word1,
            "word2": word2,
        })

        if not isinstance(proposal, str):
            raise SystemExit(
                f"CONTRACT ERROR: respond() returned {type(proposal).__name__}, "
                "but it must RETURN a vocabulary word as a str."
            )
        if proposal.casefold() not in word_to_index:
            raise SystemExit(
                f"CONTRACT ERROR: respond() returned {proposal!r}, which is not in "
                "vocabulary.json. Every proposal must be a vocabulary word."
            )
        if proposal.casefold() == secret.casefold():
            return 1.0 - PENALTY * max(0, turn - FREE_TURNS)
        word1, word2 = winner_word, proposal

    return 0.0


def self_score():
    """Check the contract, then play the 120 public practice words and report."""
    check_contract()

    words, embeddings = load_public_data()
    word_to_index = {w.casefold(): i for i, w in enumerate(words)}
    player = PotatoPlayer(words, embeddings)

    secrets = _load_practice_words(words)
    scores = [
        play_one_game(player, secret, words, embeddings, word_to_index)
        for secret in secrets
    ]
    solved = sum(1 for score in scores if score > 0)
    print(
        f"self-score {100.0 * sum(scores) / len(scores):.2f} "
        f"({solved}/{len(scores)} solved) on {len(secrets)} public words"
    )
    print(
        "Reminder: the real judge uses a different, private embedding space, so "
        "your leaderboard score will be much lower. Use this to catch crashes, "
        "not to predict rank."
    )


def _load_practice_words(words):
    """Return the public practice words, falling back to a slice of the vocabulary."""
    for directory in (
        Path(os.environ.get("POTATO_DATA_DIR", "")),
        Path(__file__).resolve().parent,
        *(p.parent for p in sorted(Path("/kaggle/input").rglob("test_public.json"))),
    ):
        candidate = directory / "test_public.json"
        if candidate.is_file():
            return json.loads(candidate.read_text())
    print("test_public.json not found; practising on the first 20 vocabulary words")
    return words[:20]


# ─── Kaggle kernel envelope — do not edit ─────────────────────────────────────
def write_submission():
    """Base64-encode this file into submission.csv for the Kaggle kernel."""
    import base64
    import csv

    # Both rows carry the SAME payload. Kaggle scores the Public subset on
    # leaderboard-a and the Private subset on leaderboard-b; the grader rejects
    # a submission whose rows disagree.
    ROW_IDS = ("leaderboard-a", "leaderboard-b")
    MAX_SOURCE_BYTES = 512 * 1024

    source = Path(__file__).read_bytes()
    if len(source) > MAX_SOURCE_BYTES:
        raise SystemExit(
            f"source is {len(source)} bytes, over the {MAX_SOURCE_BYTES} limit"
        )
    payload = base64.b64encode(source).decode("ascii")

    out = Path("/kaggle/working/submission.csv")
    with out.open("w", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["id", "program_b64"])
        for row_id in ROW_IDS:
            writer.writerow([row_id, payload])
    print(f"wrote {out} ({len(payload)} base64 chars for {len(ROW_IDS)} rows)")


if __name__ == "__main__":
    # The grader NEVER reaches this block: it imports this file and calls
    # load_public_data() and PotatoPlayer directly. This block only runs when
    # you execute the file yourself.
    if Path("/kaggle/working").is_dir():
        # On Kaggle: verify the grader could use this file, then write the CSV.
        # Checking here means an interface mistake fails the push instead of
        # silently costing you one of your 15 submissions.
        check_contract()
        write_submission()
    else:
        # On your machine: check the contract and play scored practice games.
        self_score()
