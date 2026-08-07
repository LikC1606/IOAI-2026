# Task 3 Competition Data Provenance

## Source and purpose

`input/competition/` contains organizer-supplied Task 3 data downloaded for the
formal competition run and retained only to reproduce v1-v8. It is not original
participant work and is not granted an unrestricted redistribution license.

The competition rules permit use for participation, solution development and
evaluation, and official-forum discussion. They require reasonable controls to
prevent access by people who have not accepted the rules and prohibit publishing
or redistributing Competition Data to unauthorized people.

## Retained organizer files

| File | Bytes | SHA-256 |
|---|---:|---|
| `ioai-2026-task-3-westlake-nlp-48.zip` | 9,199,364 | `461d2c54839aa35bffc05720f78f50682fecced481f730bbcb36c10f6888bbf0` |
| `public_embeddings.npy` | 16,404,608 | `21a9b583399ca67525b8287345874f2af2c589e74c9a733ce488abf118583a93` |
| `vocabulary.json` | 16,183 | `f2432b7efcca4a7718e3aba2ae89076bb80ab8ebb1913882d87c6b4989fce898` |
| `test_public.json` | 1,525 | `e134fa0420ca6387bf28019789d96c5ee1ccffc26c55350c27d76c3a3fb88bed` |
| `ioai-starter.py` | 14,549 | `ee24748c472a875b5d1f4d006e42c2815ef47603920a024687cd9911eda93727` |
| `potato_doc.md` | 14,543 | `2aaa98e763d2acc6ae17e69905ba335ad3f9f192217277ad865bb9dba170f211` |

The Python bytecode under `input/competition/__pycache__/` is a locally
generated derivative, not an additional organizer source.

## Access and reacquisition

Keep this repository private while these files are present. Access should be
limited to the participant, organizers/Jury, and other people already authorized
under the competition rules. An authorized reviewer can reacquire the source
archive with the authenticated Kaggle CLI after accepting the competition rules:

```bash
kaggle competitions download -c ioai-2026-task-3-westlake-nlp-48
```

Availability after the event is controlled by Kaggle and the organizer.

## Before any public release

Remove the entire `task3/input/competition/` directory, including the ZIP,
extracted inputs, and derived bytecode. Then regenerate `task3/MANIFEST.sha256`
and run `python verify_repository.py` from the repository root. Local
reproduction that depends on those inputs will no longer work until an
authorized reviewer reacquires them.
