# Experiment 1 — Convergence on a Clear Task

## Research Question
Can evolution improve outputs under ideal conditions?

## Hypothesis
The system will produce a large initial improvement, then hit a wall. Most changes after the first
acceptance will get rejected because the score gains stop beating the threshold. Mutations will
mostly target `strategy` because of how the metric-to-section mapping works.

## Setup
- **Prompt:** Compare the architectural tradeoffs between gRPC and REST for backend microservices.
- **max_iterations:** 7
- **improvement_threshold:** 0.5
- **Model:** gpt-4o-mini for all llm's in the system (temperature=0)

## Baseline (v1)
**Response (see the full agent's response in /logs/run_001_raw.md):**

[STEM AGENT v1]: "When comparing gRPC and REST for backend microservices, several architectural tradeoffs come into play. Here’s a breakdown of the key differences:

### 1. **Protocol and Data Format**
- **gRPC**: Uses HTTP/2 as its transport protocol, which allows for multiplexing multiple requests over a single connection. It uses Protocol Buffers (protobuf) for serialization, which is more efficient than JSON in terms of size and speed.
- **REST**: Typically uses HTTP/1.1 and JSON for data interchange. JSON is human-readable but can be larger and slower to parse compared to protobuf.

### 2. **Performance**
- **gRPC**: Generally offers better performance due to its binary serialization and support for streaming. The use of HTTP/2 allows for lower latency and better resource utilization.
- **REST**: While REST can be performant, especially with caching strategies, it may not match the efficiency of gRPC in high-throughput scenarios."
[...]

[EVALUATION v1]
- coverage: 4.0 
- grounding: 4.0
- insight: 4.0

**Scores:**
- coverage: 4.0
- grounding: 4.0
- insight: 4.0
- total: 4.0

## Key iterations

### Iteration 1 — rejected
- **Mutation target:** strategy
- **Score change:** 4.00 → 4.00 (delta: 0.00)
- **Decision:** rejected (didn't beat threshold)
- **Why notable:** First mutation expanded the strategy section heavily. The candidate response
  was longer and more structured but scored the same as the original config. The evaluator couldn't make
  a difference between baseline and candidate response.

## Final result
**Mature config version:** v1 (no mutation was accepted)

The system didn't evolve. The final agent is the same as the initial baseline agent. All three candidate
configs produced responses that were rejected because their scores didn't exceed the 0.5 threshold.
Early stop triggered after 3 consecutive rejections, while the max was 7 possible evolutions/iterations.

**Final scores (same as baseline):**
- coverage: 4.0
- grounding: 4.0
- insight: 4.0
- total: 4.0

## Quantitative summary
- Score difference (baseline -> mature): 0.00 (no change)
- Accepted mutations: 0 out of 3 iterations
- Acceptance rate: 0%
- Mutation target frequency:
  - strategy: 3x
  - quality_constraints: 0x
  - output_format: 0x
  - role: 0x
- Stopped early: Yes — 3 consecutive rejections at iteration 3 (max was 7)

## Observations
- Agent was given a clear task of comparing tradeoffs for a very clear and specific domain
- Gave a well structured and detailed response even in the initial version
- Each evaluation returned the same scores on all three key aspects, on each iteration
- No mutation was accepted as each change scored the same on the same task
- The final version of the agent remained the same as the initial version
- Baseline scored 4.0/4.0/4.0, hitting the quality ceiling immediately
- All three mutation attempts targeted the strategy section (mapping always picked the same one
  because all three metrics were tied)
- Mutator at temperature=0 produced near-identical "after" content across all three iterations,
  despite seeing different "before" content each time
- The evaluator gave 4.0/4.0/4.0 to all three candidates
- Early stop triggered at iteration 3 — the loop didn't need all 7 iterations to settle
- The final agent is identical to the baseline

## Interpretation
The hypothesis was both right and partly wrong. I expected the system to make a big initial
jump and then hit a wall, but what actually happened was even more compressed — the system never made
any jumps at all, because the baseline was already at the quality ceiling the evaluator
was already capable of measuring.

This points to a real limitation: the evaluator measures structural patterns (sections, tradeoffs,
recommendations) and gpt-4o-mini's already produce that structure on a clear task by default.
The evaluator can't tell the difference between "good response" and "good response with extra
words added", so improvement gets reported as zero, and the threshold discards every change.

The mutation collapse is also worth noting. With temperature=0, the mutator produced basically
the same rewrite 3 times in a row even though each iteration showed it different prior context.

This shows that evolution in our system isn't continuous — it either improves quickly or not at all.

## Conclusion
Evolution didn't improve outputs in this experiment. The cause was not that evolution had failed —
rather it was that the baseline already satisfied the evaluator's measurable range, leaving no room
for the system to improve. This is a clean result, but not in the way I fully expected.

The task was too simple for the agent to leave room for evolution.

## Implication for stem agents
Score-driven evolution is limited by the evaluator's reasoning: when the baseline version of the agent can
produce ceiling-grade output on a task by default, there's nothing for the agent to evolve to.

