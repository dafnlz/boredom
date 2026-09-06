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

## derived/

`balance_data_2026.csv`, `VR-App_output.csv` and `TrialOrder_Part2.xlsx` come from
the supervisor's MATLAB pipeline — see `derived/SOURCE.md`. The two `qc_*.csv`
files are produced by `notebooks/01_qc.ipynb`:

| file | produced by | content |
|---|---|---|
| `qc_trial_inventory.csv` | `01_qc` | one row per raw recording: duration, marker heights, zero fractions |
| `qc_exclusions.csv` | `01_qc` | what is dropped from the analysis set and why |

## Note on write protection

`dvc add` links the files into the DVC cache and makes them read-only, which is
what keeps the raw data from being edited by accident. Re-running the unpack
script on an unchanged tree is a no-op and needs no special handling; if the
archives really do change, run `dvc unprotect data/raw` first.

## Reproducing

```bash
python src/00_unpack_raw.py --source /path/to/folder/with/the/zips
dvc add data/raw          # only if hashes changed
```
