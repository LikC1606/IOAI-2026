# Potato Contact: A Beginner's Guide

This guide helps you start the task even if embeddings and NumPy are new to
you.

You do not necessarily need to train a neural network. You do not need an online API. The provided
`ioai-starter.py` is already a complete working solution. Your main goal is to
understand it and improve one part of it.

The official task rules are on the competition's **Overview** tabs, especially
**Evaluation** (the grader contract and the metric) and **Kaggle CLI
Submission** (how to submit).

You can read this guide in two ways:

- If embeddings are new to you, read Sections 1–7 in order.
- If you already know embeddings and NumPy, start with Sections 8–10.
- Use the glossary in Section 16 whenever you meet an unfamiliar term.

English may not be your first language. You do not need to know the meaning of
every word in the vocabulary. The algorithm works with vectors. Knowing common
word meanings is useful for intuition and debugging, but it is not required
for every calculation.

## 1. The task in one minute

The judge chooses one hidden English word from a list of 1602 words.

The judge does not tell you the word. Instead, it compares two words and tells
your program which one is closer in meaning to the hidden word.

For example, imagine that the hidden word is `tiger`:

```text
cat vs bicycle  -> cat is closer
cat vs lion     -> lion is closer
lion vs forest  -> lion is closer
```

After each answer, your program proposes one new word. If your proposal is
exactly the hidden word, you win that game.

You have at most 30 proposals. Earlier answers receive a better score.

## 2. What you receive

The competition data contains:

```text
ioai-starter.py
vocabulary.json
public_embeddings.npy
test_public.json
potato_doc.md
```

The important files are:

- `ioai-starter.py`: a complete starter solution, and the local practice judge;
- `vocabulary.json`: every word you are allowed to propose;
- `public_embeddings.npy`: one public embedding for every vocabulary word;
- `test_public.json`: 120 words with answers, for local self-scoring;
- `potato_doc.md`: this learning guide.

The official judge uses a different, private embedding space. You cannot read
it. This is intentional.

## 3. Libraries you need

The starter solution uses two kinds of Python library.

### Python standard library

These modules come with Python:

```python
import json
import os
import sys
from pathlib import Path
```

They are used for files, paths, and reading the vocabulary.

### NumPy

NumPy works with vectors and matrices:

```python
import numpy as np
```

NumPy is available in the official judge. You may safely use it.

Do not assume that large extra libraries such as PyTorch, TensorFlow,
scikit-learn, or pandas are installed. They are not needed for this task.

## 4. What is an embedding?

An embedding is a list of numbers that represents an item. Here, each item is
a word.

A very small imaginary embedding may look like this:

```text
cat      -> [0.8, 0.7, 0.1]
dog      -> [0.7, 0.8, 0.1]
airplane -> [0.1, 0.0, 0.9]
```

`cat` and `dog` have similar lists. `airplane` has a different list. A real
embedding model learns these numbers from a large amount of text.

The provided Potato embeddings have 2560 numbers per word, not 3. You should
not try to understand the meaning of each individual number. The useful
information is the relationship between complete vectors.

Embeddings are not perfect definitions. A model may connect words because
they appear in similar contexts, belong to the same topic, or have related
uses. Different embedding models can disagree.

## 5. The embedding matrix

Load the data with:

```python
import json
import numpy as np

with open("data/vocabulary.json") as file:
    words = json.load(file)

embeddings = np.load("data/public_embeddings.npy")
```

You can inspect the sizes:

```python
print(len(words))
print(embeddings.shape)
```

The result is:

```text
1602
(1602, 2560)
```

This means:

- there are 1602 rows;
- there are 2560 numbers in each row;
- `embeddings[i]` is the vector for `words[i]`.

The order is important:

```python
i = 10
print(words[i])
print(embeddings[i])
```

Never sort `words` without applying exactly the same change to the rows of the
embedding matrix.

## 6. Measuring similarity

The starter uses **cosine similarity**.

For two vectors `a` and `b`, cosine similarity is:

```text
                 a dot b
cosine(a, b) = -------------
                |a| times |b|
```

You do not need to calculate the formula by hand. NumPy can do it.

First normalize every vector so its length is 1:

```python
norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
norms[norms == 0] = 1.0
normalized = embeddings / norms
```

Then the dot product is the cosine similarity:

```python
similarity = normalized[i] @ normalized[j]
```

Usually:

- a larger value means more similar;
- a smaller value means less similar;
- the exact number is less important than comparing two numbers.

`ioai-starter.py` contains the corresponding calculations for the full
embedding matrix. You can use the formulas above to understand what those
lines of code mean.

## 7. Finding word indices

It is useful to map a word to its row number:

```python
word_to_index = {
    word.casefold(): index
    for index, word in enumerate(words)
}
```

Then:

```python
index = word_to_index["potato"]
vector = normalized[index]
```

`casefold()` makes matching case-insensitive. For example, `"Potato"` and
`"potato"` are treated as the same word.

## 8. Public and private embeddings

The public embeddings let you experiment with semantic relationships between
the vocabulary words. The official judge uses private embeddings produced
separately. Therefore, a similarity value calculated from the public file is
not an official judge value, and the two spaces may disagree.

This difference is part of the task. The private embeddings are not available
to participants, and your program must not use internet access or external
data during judging.

The **Evaluation** tab defines exactly what information the judge returns after
each proposal. Read it carefully before changing the starter.

## 9. The part of the starter you should edit

In `ioai-starter.py`, find:

```python
class PotatoPlayer:
```

The main method is:

```python
def respond(self, message):
    ...
    return next_word
```

`next_word` must be one word from `vocabulary.json`, and it must be
**returned**, not printed.

You may change the code inside this class and its constants. Deciding how to
use the judge's answers and the public data is the main challenge of the task.
This guide intentionally does not prescribe a strategy.

### Keep the names and signatures exactly as they are

The grader **imports your file as a Python module** and looks these names up by
exact spelling. It does not run your file as a program, so the
`if __name__ == "__main__":` block at the bottom never executes during grading.

```python
load_public_data() -> (words, embeddings)   # called once per round

class PotatoPlayer:
    def __init__(self, words, embeddings)   # exactly two arguments
    def new_game(self)                      # called before each game
    def respond(self, message) -> str       # called each turn
```

Renaming `load_public_data` or `PotatoPlayer`, or changing how many arguments
`__init__` takes, fails every game in the round. Everything else in the file is
yours to change.

`__init__` runs once per round, so put slow precomputation there. `new_game()`
runs before each game; reset per-game state there and keep what `__init__` built.

## 10. The message your player receives

On every turn, `respond` receives a Python dictionary like this:

```python
message = {
    "turn": 7,
    "word1": "house",
    "word2": "book",
    "winner_word": "house",
    "verdict": "first",
}
```

Meaning:

- `turn`: current turn number;
- `word1`, `word2`: words compared by the judge;
- `verdict`: `first`, `second`, or `same`;
- `winner_word`: the word kept for the next comparison.

The first comparison is always:

```text
lamp vs potato
```

These two words come from the judge. They are not your first proposal.

## 11. A small NumPy reference

You do not need every NumPy feature. These operations are enough for many
solutions.

### Create an array

```python
values = np.zeros(1602)
mask = np.ones(1602, dtype=bool)
```

### Select one row

```python
row = embeddings[25]
```

### Select many rows

```python
indices = np.array([2, 10, 25])
rows = embeddings[indices]
```

### Boolean selection

```python
selected = values[mask]
```

Boolean arrays can select the positions where their value is `True`.

### Sort indices by descending value

```python
ranked = np.argsort(-values)
```

### Sum values

```python
total = np.sum(values)
```

### Matrix multiplication

```python
result = matrix @ vector
```

### Avoid changing an original array

```python
copy = original.copy()
```

NumPy usually applies an operation to a complete array. This is called
vectorization. It is normally faster than a Python loop over all 1602 words.

The examples in this section demonstrate NumPy syntax only. They are not a
suggested solution strategy.

## 12. Running the local test

Run your solution file directly:

```bash
python ioai-starter.py
```

It does two things. First it checks that the grader could use your file, that
`load_public_data` and `PotatoPlayer` exist with the right signatures. Then it
plays the 120 words in `test_public.json` and prints a score.

The local judge uses the public embeddings. Your official score will be much
lower, because the private embedding space is different.

The local test is useful for:

- syntax errors;
- invalid words;
- a wrong class or method name;
- crashes;
- infinite loops;
- comparing strategies on public examples.

It cannot tell you the exact official score.

**Run it before every submission.** Pushing a Kaggle kernel does not check any
of this: the kernel only base64-encodes your file into `submission.csv`, so it
reports `COMPLETE` even when your interface is wrong. The mistake then only
appears after `kaggle competitions submit`, which costs one of your submissions.

## 13. Submitting on Kaggle

Your submission is a Kaggle notebook that runs `ioai-starter.py` with your
edits. The notebook does not play any games: it only base64-encodes your source
into `submission.csv`. The grader then decodes that source and plays the hidden
games with it.

Before submitting:

1. Run `python ioai-starter.py` locally and confirm the contract check passes.
2. Push the notebook with `kaggle kernels push`.
3. Check that `submission.csv` has the header `id,program_b64` and two rows.
4. Submit with `kaggle competitions submit`.

The exact commands are on the **Kaggle CLI Submission** tab.

Your `PotatoPlayer` is built **once per round** and reused for all 120 games in
that round, with `new_game()` called between them. Anything you store on `self`
in `__init__` stays available across games; anything you reset in `new_game()`
does not.

## 14. Printing and debugging

Your `respond()` method **returns** a word. It does not print it:

```python
return next_word          # correct
print(next_word)          # wrong: the grader ignores what you print
```

The grader captures and discards anything your program prints, so a leftover
`print("my debug message")` is harmless. It simply cannot be seen during
grading. To see debug output, run the file locally instead:

```bash
python ioai-starter.py
```

## 15. Common mistakes

### Proposing a word outside the vocabulary

Wrong:

```python
return "a-word-not-in-the-list"
```

Always return `words[index]` or verify membership with `word_to_index`.

### Mixing word indices and words

Many NumPy operations return row indices, not words. Convert an index back to
a vocabulary word explicitly:

```python
index = 25
word = words[index]
```

### Comparing embeddings without normalization

Raw dot products depend on vector length. Use the normalized matrix supplied
by `load_public_data()`.

### Renaming the class or changing `__init__`

The grader looks up `load_public_data` and `PotatoPlayer` by exact spelling and
always calls `PotatoPlayer(words, embeddings)` with both arguments. Renaming
either, or changing the argument count, fails the whole round. Running
`python ioai-starter.py` catches this before you spend a submission.

### Printing the answer instead of returning it

`respond()` must `return` the word. The grader ignores standard output.

### Adding a slow Python loop over all word pairs

Use NumPy matrix operations when possible. A deeply nested Python loop over
all 1602 by 1602 pairs on every turn may be too slow.

### Using a library that the judge does not provide

The safe assumption is Python standard library plus NumPy. Test every import
before depending on it.

### Reading a file with a fixed absolute path

Do not use a path from your own computer. The grader runs your file from a
temporary directory, so keep the search that `load_public_data()` already does.



## 16. Glossary

| Term | Simple meaning |
|---|---|
| hidden word / secret | The word your program must discover |
| vocabulary | The complete list of allowed words |
| embedding | A numeric vector representing a word |
| vector | An ordered list of numbers |
| matrix | A rectangular table of numbers |
| dimension | One position in a vector |
| cosine similarity | A measure of how similar two vector directions are |
| private judge | The official checker using hidden embeddings |
| grader | The program that imports your file and plays the hidden games |
| contract | The names and signatures your file must define for the grader |
| round | One set of 120 hidden games, scored as a single leaderboard entry |

## 17. Final checklist

Before submitting, check:

- [ ] `python ioai-starter.py` runs and prints `contract OK`.
- [ ] My file still defines `load_public_data()` and `PotatoPlayer`.
- [ ] `PotatoPlayer.__init__` still takes `(self, words, embeddings)`.
- [ ] `PotatoPlayer.respond` **returns** one vocabulary word.
- [ ] I use only files provided to participants.
- [ ] My program does not require internet access.
- [ ] `submission.csv` has the header `id,program_b64` and exactly two rows.
- [ ] Both rows carry the same base64 payload.

You do not need to understand every detail before you begin. First make sure
that you can run the starter and its local test. Then study the starter code,
form your own ideas, and test them carefully.
