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
```

## Working rule: raw data is never modified

`data/raw/` is a byte-exact reproduction of the three source archives — 272
files, nothing added, nothing renamed, nothing written back. The manifest lives
beside the directory rather than inside it, and `dvc add` leaves every file
read-only. Notebooks open `data/raw/` for reading only; everything derived from
it is written to `data/derived/`.

## Getting the data

The raw data is not in this repository. It comes from three ZIP archives in the
course Teams folder *SPO-14560 Project Seminar I - General*
(`Anaropia.zip`, `PsychoPy.zip`, `LimeSurvey.zip`). With those in place:

```bash
conda env create -f environment.yml && conda activate boredom
python src/00_unpack_raw.py --source /path/to/folder/with/the/zips
dvc add data/raw          # only when the hashes change
```

### Pulling the raw data from the university cloud

The raw data lives in the University of Konstanz Nextcloud, not in this
repository. The DVC remote that points at it is deliberately kept in
`.dvc/config.local`, which is not committed: the storage is access-controlled, so
publishing its address would buy nothing and would expose an account path.

To set it up on a fresh machine, in the repository root:

```bash
pip install dvc-webdav
dvc remote add --local -d ukn \
    "webdavs://cloud.uni-konstanz.de/remote.php/dav/files/<USERNAME>/Balance%20and%20VR/dvc-storage"
dvc remote modify --local ukn user <USERNAME>
dvc remote modify --local ukn password <APP-PASSWORD>
```

`<APP-PASSWORD>` is an app password generated in Nextcloud under
*Settings → Security → Devices & sessions*, not the account password. It is
stored only in `.dvc/config.local`.

Then `dvc push` uploads the raw data and `dvc pull` fetches it.

`src/00_unpack_raw.py` is idempotent and resumable, and writes
`data/raw_manifest.csv` with the SHA-256 of every extracted file.
`data/raw.dvc` records the content hash of the whole directory, so the raw
data can be verified without being published.

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
