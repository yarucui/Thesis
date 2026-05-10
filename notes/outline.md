# Chapter outlines

## Ch 1 — Introduction (~1500 words)
- Hook: the measurement-artifact problem
- Gap: no decomposition of alignment gap by mechanism
- RQ1: does output format account for the gap?
- RQ2: does role framing modulate the gap?
- Contributions: pipeline + 2 experiments + significance tests + mechanism map
- Road map paragraph

## Ch 2 — Related work (~2000 words)
- LLM alignment measurement (RLHF, value alignment, benchmarks)
  - Key papers: Ouyang et al. 2022, Bai et al. 2022, Ganguli et al. 2022
- Framing effects in LLMs (persona, role, perspective)
  - Key papers: Argyle et al. 2023 (silicon sampling), Santurkar et al. 2023
- Crowdsourced decision corpora / Reddit as ground truth
  - Key papers: Reddit advice literature, Backstrom et al. 2013

## Ch 3 — Methodology (~2500 words)
- Dataset: 5 domain subreddits, 620 qualified posts, risky_ratio annotation
- Baseline (step5): forced-choice, 4 models × 10 samples × T=0.7
- Direction 1 (step6): VS / DV / HighT conditions, 150 ambiguous posts
- Direction 2 (step7): oracle / personal framing, 620 posts
- Statistical analysis: paired bootstrap + Mann-Whitney + BH-FDR

## Ch 4 — Direction 1 (~2000 words)
- Baseline entropy collapse (table: entropy by model)
- VS recovers entropy: Δ = -0.235 [−0.250, −0.220]***
- DV also recovers: Δ = -0.212***
- HighT smaller: Δ = -0.016**; VS vs HighT = -0.220***
- Figure: entropy per condition per model
- Interpretation: decoding is the culprit

## Ch 5 — Direction 2 (~2500 words)
- Framing results table (mean abs_gap by framing × model)
- oracle < advisor < personal ordering (all pairwise significant)
- Effect sizes vs. D1: framing is 6-11× smaller than format
- Domain moderation: health (careful with n=48)
- Trade-off moderation: short_term_vs_long_term *** (Δ = -0.540)
- Figure: abs_gap by framing × model

## Ch 6 — Discussion (~1500 words)
- Mechanism map (2×2 table as figure or box)
- Implications for how alignment benchmarks are designed
- Limitations
- Future work

## Ch 7 — Conclusion (~500 words)
- 3 paragraphs: summary / so what / call to action
