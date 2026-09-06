# Provenance of data/derived

These tables were **not** produced by the code in this repository. They are the
output of the MATLAB pipeline run by the course supervisor and are the starting
point of the analysis here (see *Analysis boundary* in the top-level README).

Source: course Teams folder `SPO-14560 Project Seminar I - General`.

| file | source path | SHA-256 | bytes |
|---|---|---|---|
| `balance_data_2026.csv` | `4_Data_Analysis/Balance Analysis/balance_data_2026.csv` | `d125552c27d70bc4…` | 12,719 |
| `VR-App_output.csv` | `4_Data_Analysis/Balance Analysis/VR-App_output.csv` | `62fad60a7c125fc0…` | 98,016 |
| `TrialOrder_Part2.xlsx` | `4_Data_Analysis/Balance Analysis/TrialOrder_Part2.xlsx` | `542721852b9f32a4…` | 19,453 |

**`balance_data_2026.csv`** — Wide analysis table, one row per participant: ID, height, weight, then 6 sway parameters x 8 conditions (HB_t1..LB_t4). Output of run_VRApp_analysis_2026.m.

**`VR-App_output.csv`** — Append-only log written per trial by pcl_BApp_analysis.m. 387 rows / 107 unique fname; carries model parameters absent from the wide table (sim Err, dt, Kp, Kd, Glp, J, mgh, b). De-duplicated in 02_prepare.

**`TrialOrder_Part2.xlsx`** — Per-participant body height/weight and the file index used for each of the 8 conditions; values may carry an _INCOMPLETE suffix that is part of the filename.

Full hashes:
```
d125552c27d70bc46b9b2df6ebc2b92981fa49c4b860f3576a30af1db6edf33a  balance_data_2026.csv
62fad60a7c125fc097fbd05139840dca4298be1ed8088a6ab35affae0656df5f  VR-App_output.csv
542721852b9f32a44b58f0d96e9033bd96afa23f98d973b9ee520f24f751bc22  TrialOrder_Part2.xlsx
```
