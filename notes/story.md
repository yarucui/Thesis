# Thesis story and narrative arc

## The hook (one sentence)
When researchers measure the gap between LLM advice and human preferences,
they are mostly measuring their measurement instrument — not the model's beliefs.

## The problem with existing work
Most LLM alignment studies use forced-choice prompts. These produce near-zero
entropy outputs (models always commit to one option), while human preferences
on the same decision scenarios are genuinely split. The resulting "alignment gap"
has been attributed to model training, RLHF artifacts, or framing effects.

We show this attribution is wrong.

## Our decomposition

### Driver 1 — Output format (large, Δ ≈ 0.23)
Verbalized sampling (asking the model to output P(A) directly) recovers
94-101% of human entropy across all four models. The gap collapses when you
change from forced-choice to distribution output.
→ The measurement instrument drives most of the gap.

### Driver 2 — Task structure (large, Δ ≈ 0.54)
Short-term vs. long-term trade-offs show much smaller gaps than
aggressive-vs-conservative trade-offs. LLMs are better calibrated to human
preferences for some task types than others.
→ Task structure matters more than model identity.

### Driver 3 — Domain (moderate, Δ ≈ 0.18)
Health domain posts show smaller LLM-human gaps than other domains.
(Underpowered: n=48, interpret with caution.)

### Driver 4 — Role framing (small but significant, Δ ≈ 0.01-0.03)
Oracle framing (descriptive: "what would advice-givers recommend?") produces
smaller gaps than personal framing ("what would you choose?"). Effect is real
(all three framing comparisons p_fdr < 0.01) but practically negligible
compared to output format.
→ Framing matters — but previous work overstated it.

## The 2x2 mechanism map

```
                    | Single-token output    | Distribution output
Prescriptive role   | Baseline (step5)       | Direction 1 (VS/DV)
Descriptive role    | Direction 2 (framing)  | Direction 1 (HighT)
```

The output-format axis dominates. The role-framing axis is real but minor.

## Story arc by chapter
1. Intro: the misattribution problem → our decomposition approach
2. Related work: alignment measurement, framing effects, Reddit corpora
3. Methods: pipeline, dataset, two experiments
4. D1 results: format is the dominant driver (entropy recovery)
5. D2 results: framing is real but small; task structure matters more
6. Discussion: mechanism map, evaluation implications, limitations
7. Conclusion: reframe how alignment evaluation should be done
