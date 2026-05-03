# Cross-Run Analysis — Stem Agent Evolution Behavior

## Overview
This analysis is the combined result from the first three experiments to show how the evolution system
behaves under different conditions:

- **Experiment 1** — clear, well-scoped task (gRPC vs REST). Tested evolution under ideal conditions.
- **Experiment 2** — ambiguous task with incorrect interpretation (agentic frameworks). Tested
  whether evolution can self-correct topic misses.
- **Experiment 3** — simple task where over-optimization is possible (what is HTTP). Tested
  whether the system can degrade quality on prompts that don't need elaboration.

---

## 1. What evolution actually optimizes
Across all experiments, the system kept improving responses based on:
- structure (sections, formatting, ordering)
- surface completeness (more topics, more bullets)
- perceived depth (named entities, comparisons, recommendations)

It didn't improve:
- correctness of understanding (Experiment 2 — wrong topic throughout)
- appropriateness to task complexity (Experiment 3 — bloated answer to a simple question)

**The system optimizes for the evaluator's scoring rules, not for the actual goal of the user's request.**
The narrower the scoring ruleset, the more aggressively evolution pushes against axes the scores ignore.

---

## 2. Dependence on baseline quality
Evolution behavior is strongly conditioned by where the baseline starts:

- **High baseline (Experiment 1):** baseline already at the rubric's measurable ceiling. No
  mutation could clear the +0.5 threshold. Zero acceptances.
- **Low baseline (Experiment 2):** large headroom. First mutation produced +1.33 jump,
  following mutations couldn't clear the threshold. One acceptance.
- **Medium baseline (Experiment 3):** moderate headroom. First mutation produced +1.17 jump,
  following mutations got rejected. One acceptance.

**Evolution only happens when the baseline leaves room within the scoring system.**
This is a real limit — the system doesn't "evolve indefinitely" because the rubric saturates,
and the threshold filters everything below the saturation point.

---

## 3. Failure to self-correct
Experiment 2 produced the cleanest negative finding of the project. The agent picked the wrong
domain at v1 (human agency frameworks instead of AI agent frameworks). Across all four iterations:

- domain interpretation: 0/4 corrections
- score progression: 2.50 -> 3.83 (+1.33)
- final response quality (per-rubric): high
- final response quality (per-task): wrong topic entirely

**The system assumes the baseline interpretation is correct and optimizes within it.**
There is no mechanism that asks "is this the right question?" — only "is this answered well
according to the rubric?"

---

## 4. Evaluator limitations
The evaluator showed concrete blind spots, each exposed by a different experiment:

- **Domain blindness (Experiment 2):** wrong-topic responses scored 4.0/3.5/4.0 — no metric
  measures whether the answer matches the question.
- **Length-vs-fit blindness (Experiment 3):** a 700-word response with sections about
  microservices and SEO scored identically to a clean 250-word baseline answering the same
  "what is HTTP" question.

**The evaluator defines the limits of evolution. Anything not measured cannot be improved —
and anything mis-measured will be optimized against.**

---

## 5. Mutation behavior
Eight of eleven mutations targeted `strategy`. Three targeted `quality_constraints`. Two of the
four mutable sections — `role` and `output_format` — were never targeted, because the
metric→section mapping doesn't route any score to them.

At temperature=0, the mutator produced near-identical "after" content across iterations even
when given different "before" content:

- Experiment 1: three strategy mutations all produced variants of "explore tradeoffs, recommendations, multiple perspectives"
- Experiment 2: three quality_constraints mutations all produced variants of "support claims with examples and quantitative data"
- Experiment 3: four strategy mutations all produced variants of "comprehensive analysis with comparative analysis and recommendations"

**Mutation diversity is low. The mutator tends to regenerate similar rewrites rather than exploring significantly different alternatives.

---

## 6. Evolution dynamics
A consistent shape emerged across all three experiments:

1. baseline produces some score
2. if there is headroom, one strong mutation jumps the score to the rubric ceiling
3. plateau — following mutations can't beat the threshold
4. three rejections in a row trigger an early stop

**Evolution isn't gradual. It is step-like and converges quickly** — typically within 3–4
iterations, far below `max_iterations=7`.

---

## 7. Implicit stopping
The system has no explicit "convergence detected, stop now" mechanism. Two interacting safeguards
produce one anyway:

- **Acceptance threshold (+0.5)** filters out marginal mutations
- **Consecutive rejection limit (3)** triggers early stop

All three experiments terminated cleanly via this combination. This addresses the task
description's question — *"how does it know when it's good enough to stop evolving?"* — without
explicit convergence detection. **The system "knows it's good enough" when its own mutator can
no longer find a section rewrite that beats the threshold against its own evaluator.**

This is an implicit stopping criterion that depends on evaluator consistency. If scores were
noisy across runs, the threshold would let through accepted-by-luck mutations.

---

## 8. Score does not equal usefulness
The most important finding, surfaced most clearly by Experiments 2 and 3:

- **Experiment 2:** high mature score (3.83) on a wrong-domain answer
- **Experiment 3:** high mature score (4.00) on a less useful answer than the baseline

Read as a real user, the Experiment 3 baseline ("HTTP, or Hypertext Transfer Protocol, is an
application-layer protocol used for transmitting hypertext over the internet...") is more useful
than the mature version (700 words with sections on microservices, SEO, and Progressive Web Apps).
The evaluator scored the mature version higher.

**Score improvement does not guarantee real-world usefulness.** This mirrors LLM behavior
patterns described in production systems — optimization toward measurable signals at the expense
of unmeasured quality.

---

## Final conclusion
The system successfully optimizes responses according to its scoring function. This is real and
measurable. It isn't the same thing as producing correct or useful outputs.

Evolution is bounded by:
- the evaluator's scoring ruleset — anything unmeasured won't improve
- the initial interpretation of the task — the system optimizes within the baseline's frame
- the mutation strategy space — only `strategy` and `quality_constraints` are reachable; the
  mutator at temperature=0 has low diversity

**The system improves what it can measure, ignores what it can't, and can optimize against unmeasured aspects of quality.
** Demonstrating this honestly was the goal of the experiments, and the three runs collectively provide that demonstration.