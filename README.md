# Boredom & Postural Control in VR

Analysis code for a Project Seminar I paper (SPO-14560, M.Sc. Sports Science
for Health, University of Konstanz).

**Research question.** Does experimentally induced boredom affect the power of
visually evoked postural sway (`PeriodicPower` of anterior–posterior centre-of-mass
sway) during continuous pseudorandom visual-scene tilt in virtual reality?

## Study in one paragraph

Fourteen participants stood in a VR headset for two ~17-minute sessions while
listening to a podcast, once in a high-boredom (HB) and once in a low-boredom
(LB) condition, in counterbalanced order. Each session contained four 210-s
measurement blocks (`t1`–`t4`). Within a block the first 50 s are quiet stance;
from 50 s the visual scene tilts continuously in pitch (0.5° peak-to-peak,
20-s period, 8 cycles). Body sway is reconstructed from VR shoulder and hip
markers at ~90 Hz; there is no force plate in this dataset.

## Repository layout

```
data/
  raw/               # 272 files, 0.91 GB — DVC-tracked, read-only, never edited
  raw_manifest.csv   # SHA-256 of every raw file
  derived/           # analysis-ready tables, committed (see data/derived/SOURCE.md)
notebooks/    # 01_qc, 02_prepare, 03_analysis
src/          # scripts run outside the notebooks
figures/
ANALYSIS_PLAN.md   # the test, fixed in writing before it was run
```

## Pipeline

| step | reads | writes |
|---|---|---|
| `src/00_unpack_raw.py` | the three source archives | `data/raw/`, `data/raw_manifest.csv` |
| `notebooks/01_qc.ipynb` | `data/raw/vr/`, `balance_data_2026.csv` | `qc_trial_inventory.csv`, `qc_exclusions.csv` |
| `notebooks/02_prepare.ipynb` | the above + `data/raw/limesurvey/` | `analysis_long.csv`, `analysis_long_codebook.csv` |
| `notebooks/03_analysis.ipynb` | `analysis_long.csv` | tables and figures |

`analysis_long.csv` has one row per participant × condition × block. Every missing
value of the primary outcome in it is matched against `qc_exclusions.csv`, and
`02_prepare.ipynb` stops if any gap is not explained by a rule.

## The analysis was fixed before it was run

`ANALYSIS_PLAN.md` names one primary outcome, one confirmatory test and one alpha
level, states what the design can and cannot detect at this sample size, and marks
everything else as secondary or exploratory. It was committed before
`03_analysis.ipynb` existed; the git history of the two files is the evidence, and
any later departure is recorded in the plan's *Deviations* section rather than by
editing it.

`02_prepare.ipynb` computes no comparison between conditions, for the same reason.

## Working rule: raw data is never modified

`data/raw/` is a byte-exact reproduction of the three source archives — 272
files, nothing added, nothing renamed, nothing written back. The manifest lives
beside the directory rather than inside it, and `dvc add` leaves every file
read-only. Notebooks open `data/raw/` for reading only; everything derived from
it is written to `data/derived/`.

## Getting the data

The raw data is not stored in this repository and is not mirrored anywhere else.
It stays where the study keeps it: the course folder *Balance and VR* on the
University of Konstanz Nextcloud, as three archives — `Anaropia.zip` (VR
tracking), `PsychoPy.zip` (event logs) and `LimeSurvey.zip` (questionnaires).
Anyone with access to the course folder can reproduce `data/raw/` exactly:

```bash
conda env create -f environment.yml && conda activate boredom
python src/00_unpack_raw.py --source /path/to/folder/with/the/zips
dvc status               # confirms the tree matches data/raw.dvc
```

There is no DVC remote on purpose. Mirroring 0.9 GB into a second location would
duplicate data the course already stores and would not make anything more
verifiable: `data/raw.dvc` pins the md5 of the whole directory and
`data/raw_manifest.csv` carries the SHA-256 of each of the 272 files, so an
unpacked copy can be checked against this repository byte for byte. DVC is used
here for integrity and immutability, not for distribution.

`src/00_unpack_raw.py` is idempotent and resumable, and writes
`data/raw_manifest.csv` with the SHA-256 of every extracted file.

## Note on participant data

Participants are identified only by the self-generated pseudonymous code used
throughout the study. The code-to-name list stays in the course Teams folder and
is never copied here. Raw data — which also carries age, sex and questionnaire
responses — is DVC-tracked and not published; only the derived sway parameters,
body height and body weight are in this repository.

## Analysis boundary

The MATLAB pipeline that turns raw VR tracking into sway parameters
(`getFRF.m`, `pcl_ICfit_ml.m` and the surrounding LA toolbox) was run by the
course supervisor and is **not** re-executed here. It is documented in the
Methods section; this repository starts from its output tables.
