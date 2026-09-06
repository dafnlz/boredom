# Data

```
data/
├── raw/        # DVC-tracked, not in git — see src/00_unpack_raw.py
├── derived/    # analysis-ready tables (git-ignored until pseudonymised)
└── README.md
```

## raw/

Produced by `src/00_unpack_raw.py` from three ZIP archives exported from the
course Teams folder *SPO-14560 Project Seminar I - General*:

| archive | goes to | content |
|---|---|---|
| `Anaropia.zip` | `raw/vr/` | VR tracking, one CSV per participant × condition × block, 64 columns, ~90 Hz |
| `PsychoPy.zip` | `raw/psychopy/` | PsychoPy event logs (`.csv`, `.log`, `.psydat`) |
| `LimeSurvey.zip` | `raw/limesurvey/` | questionnaire exports (SBPS, MSBS, check-up ratings) |

`raw/manifest.csv` lists every extracted file with its size and SHA-256.
It stays inside `raw/` because filenames contain participant codes.

`data/raw.dvc` is committed and records the content hash of the whole
directory, so the raw data can be verified without being published.

## Reproducing

```bash
python src/00_unpack_raw.py --source /path/to/folder/with/the/zips
dvc add data/raw          # only if hashes changed
```
