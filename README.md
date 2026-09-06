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
  raw/        # 272 files, 0.91 GB — DVC-tracked, not in git
  derived/    # analysis-ready tables (git-ignored until pseudonymised)
notebooks/    # 01_qc, 02_prepare, 03_analysis
src/          # scripts run outside the notebooks
figures/
```

## Getting the data

The raw data is not in this repository. It comes from three ZIP archives in the
course Teams folder *SPO-14560 Project Seminar I - General*
(`Anaropia.zip`, `PsychoPy.zip`, `LimeSurvey.zip`). With those in place:

```bash
conda env create -f environment.yml && conda activate boredom
python src/00_unpack_raw.py --source /path/to/folder/with/the/zips
dvc add data/raw          # only when the hashes change
```

`src/00_unpack_raw.py` is idempotent and resumable, and writes
`data/raw/manifest.csv` with the SHA-256 of every extracted file.
`data/raw.dvc` records the content hash of the whole directory, so the raw
data can be verified without being published.

## Note on participant data

Filenames and derived tables contain participant codes. Nothing that carries a
code is committed to this repository; the code-to-name list stays in the course
Teams folder and is never copied here.

## Analysis boundary

The MATLAB pipeline that turns raw VR tracking into sway parameters
(`getFRF.m`, `pcl_ICfit_ml.m` and the surrounding LA toolbox) was run by the
course supervisor and is **not** re-executed here. It is documented in the
Methods section; this repository starts from its output tables.
