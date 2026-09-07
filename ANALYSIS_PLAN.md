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

### Deviations

*(none)*
