# Analysis plan

**Status: written and committed before `03_analysis.ipynb` exists.**
Data collection finished in July 2026 and the dataset is fixed, so no participant can be
added and no interim look can influence stopping. What is still open is the choice of
test, and that is what this document closes. Anything not named here is exploratory and
will be labelled exploratory in the paper.

*Статус: написан и закоммичен до того, как появился `03_analysis.ipynb`. Сбор данных
завершён в июле 2026, набор зафиксирован — добавить участника или остановиться по
промежуточному результату невозможно. Открытым остаётся выбор теста, и его закрывает
этот документ. Всё, что здесь не названо, является поисковым и будет так помечено.*

---

## 1. Question

Does experimentally induced boredom change how strongly standing sway follows a moving
visual scene?

## 2. Design

Within-subject crossover. Each participant completed two sessions, one with a
high-boredom podcast (HB) and one with a low-boredom podcast (LB), order randomised.
Each session contained four 210 s balance blocks with the same pseudo-random visual
scene tilt. The analysis dataset is `data/derived/analysis_long.csv`, built by
`02_prepare.ipynb`; inclusion follows `data/derived/qc_exclusions.csv`, built by
`01_qc.ipynb`.

Analysis set: 13 participants, of whom **12 have data in both conditions**. One further
participant is retained but flagged for a calibration difference between sessions.

## 3. Primary outcome — one, fixed

**Periodic power (response sway power)** in the anterior-posterior direction, as defined
in `3_Raw_Data/Balance_Parameters.docx`: the sway power at the frequencies of the visual
stimulus.

Reason for choosing it over the other five available parameters: it is computed
deterministically from the recording. The model-fitted parameters, visual weight `W`
among them, come out of a stochastic `GlobalSearch` optimisation — re-running the
existing MATLAB pipeline on the *same* file returns bit-identical periodic and remnant
power but a visual weight that differs by up to 16% and a torque feedback gain by up to
300%. An outcome whose value depends on the random seed cannot carry a hypothesis test.

**Aggregation, fixed in advance:** the four blocks are averaged within each
participant × condition before testing. Testing blocks separately would create eight
comparisons where the design supports one.

## 4. Confirmatory test — one, fixed

Wilcoxon signed-rank test on the 12 within-participant differences
(HB mean − LB mean), two-sided, **α = .05**.

The rank test rather than a paired *t*-test because with n = 12 a normality check has
low power, and choosing the test after inspecting the differences is exactly the
researcher degree of freedom this plan exists to remove. The paired *t*-test will be
reported alongside as a sensitivity analysis; **the Wilcoxon result is the answer to the
research question regardless of which of the two is the smaller p-value.**

Reported with the test: the exact p-value (not a threshold), the median and range of the
differences, the matched-pairs rank-biserial correlation as effect size, and a
bootstrap confidence interval for the median difference.

## 5. Sensitivity to what this study can detect

With n = 12 paired observations, α = .05 two-sided and 80% power, the smallest detectable
effect is roughly **d_z ≈ 0.87** — a large effect. This study cannot distinguish a small
or moderate effect from no effect. That is stated in the Results, not only in the
Discussion, and a non-significant result will be reported as inconclusive rather than as
evidence of absence.

## 6. Manipulation check — pre-specified, reported before the primary test

The primary test is only interpretable if the HB podcast actually induced more boredom.
Wilcoxon signed-rank on the within-participant difference in state boredom change
(`state_delta`, HB − LB), two-sided, α = .05.

If the manipulation check fails, the primary test is still run and reported, and the
interpretation changes: the study then tests the effect of *podcast condition*, not of
*boredom*. The plan does not permit dropping participants to make the check pass.

## 7. Secondary analyses — named in advance, reported as secondary

1. Condition × block, to test whether an effect builds up over the session: linear mixed
   model with `condition`, `block` and their interaction as fixed effects, `period` as a
   covariate for order, and a random intercept per participant.
2. Remnant power (random sway power), same test as the primary outcome. It is the other
   deterministic parameter and speaks to overall sway rather than the visual response.

These are two tests, decided now. **No correction is applied and none is claimed** — they
are reported as secondary and their p-values are described as such.

## 8. Exploratory — everything else

The four remaining sway parameters, the trial-level 0–10 boredom rating as a continuous
predictor, and any subgroup or per-block look. Reported in one clearly marked section,
with no p-value presented as a finding.

## 9. Deviations

Any departure from this document is recorded in a "Deviations" section appended below,
with its date and its reason, rather than by editing the text above. The git history of
this file is the record.

*Любое отступление от этого документа записывается в раздел «Deviations» ниже, с датой и
причиной, а не правкой текста выше. Историю ведёт git.*

### Clarifications

**7 September 2026 — added before any test was run.**
Section 3 says the four blocks are averaged within each participant × condition but
does not say what to do when a block is missing, and four blocks are missing for QC
reasons. Fixed now, before the primary test is executed: the mean is taken over the
blocks that are available, with no minimum number of blocks required. A sensitivity
analysis restricted to participants who have all four blocks in both conditions is
reported alongside the primary test.

Section 7 says the mixed model takes `block` as a fixed effect but does not say how
`block` is coded, and does not say whether the outcome is transformed. Fixed now,
also before any test was run: `block` enters as a linear term (1–4) so the
interaction tests whether an effect builds up across the session, which is the
question the model was named for; and the outcome enters the mixed model as its
natural logarithm, because it is a power measure bounded below by zero and
right-skewed. Neither choice touches the primary test: the Wilcoxon test is
rank-based, and a logarithm is monotonic, so it would return the same result either
way.

All of the above is recorded here rather than in the notebook, and this commit
precedes the commit that adds `03_analysis.ipynb`.

### Deviations

**9 September 2026 — a defect in the processing code, and which version of the
primary outcome the paper reports.**

While writing up I found that `getCOM`, the function that reconstructs the centre
of mass from the body markers, swaps the hip and shoulder channels on every trial.
The check that is supposed to decide whether to swap assigns the same value in both
of its branches (`4_Data_Analysis/Balance Analysis/pcl_vr_getData_ls.m`, lines
71-76; the same block is in `LA_toolbox_July24/VR_scripts/pcl_vr_getData.m`, lines
86-91), so the swap at line 101 is unconditional. In these recordings the shoulder
marker sits above the hip marker in all 104 usable files, so no swap should occur.
`balance_data_2026.csv` and `VR-App_output.csv` are the output of that code path,
so every value used in this analysis carries it.

To find out whether it mattered, `getCOM` and the periodic power calculation were
re-implemented in Python and run on the raw recordings. Kept as it is, the
re-implementation reproduces `balance_data_2026.csv` closely (r = .9995, median
deviation 0.02% across 95 trials), which is the evidence that it is faithful.
Without the swap, absolute periodic power is roughly half as large, while the
condition contrast is nearly unchanged.

**Both versions had therefore been computed before this entry was written.** The
choice of which one the paper reports cannot be presented as blind, and is not.
The rule adopted is:

> The confirmatory test reported in the paper uses the output of the study's own
> processing pipeline (`balance_data_2026.csv`). The Python re-derivation is
> reported as a sensitivity analysis.

The rule is stated in terms of provenance, not of outcome: the pipeline output is
what the study actually produced and what the supervisor can verify independently,
and no re-processing has been carried out by the person writing this. It also
happens to be the conservative choice — the pipeline version yields the **larger**
p-value of the two — so it cannot have been selected to favour a result.

The defect was reported to the supervisor on 8 September 2026. He confirmed it on
10 September and decided that this paper is written on the existing pipeline output,
with the code corrected afterwards for later cohorts. That settles the rule above
rather than changing it: the confirmatory test reported here is the one run on
`balance_data_2026.csv`, the Python re-derivation stays a sensitivity analysis, and
the defect is described in the paper. No re-processing is expected before the
deadline.

*Обе версии были посчитаны до того, как эта запись написана, поэтому выбор
первичной не выдаётся за слепой. Правило сформулировано по происхождению данных, а
не по результату: первичным берётся вывод самого исследования, перевывод на Python
идёт как проверка устойчивости. Побочное свойство правила — оно даёт бо́льшее из
двух p-значений, то есть не могло быть выбрано ради результата.*

**9 September 2026 — correction to a figure quoted in section 5.**
Section 5 states the smallest detectable effect as "roughly d_z ≈ 0.87". Solving it
exactly for n = 12, α = .05 two-sided and 80% power under the non-central t gives
**d_z = 0.89**. The original figure was an approximation and is left in place as written;
the paper quotes the computed value, which `src/paper_numbers.py` produces as `mde_d_z`.
The conclusion the figure supports — that this sample can only resolve a large effect —
is unchanged.

*Точное решение даёт 0,89 вместо приблизительных 0,87, названных в разделе 5. Вывод,
ради которого цифра приводилась, не меняется.*
