# Experiment 2 — Recovery from Domain Ambiguity

## Research Question
Can evolution self-correct when the agent misunderstands the task domain?

## Hypothesis
The agent will pick the wrong domain interpretation in the baseline (likely human agency frameworks
instead of AI agent frameworks, based on observed Phase 2 behavior). Evolution will improve
structural metrics — coverage, grounding, insight — because the evaluator rewards structure.
But the domain interpretation will not self-correct, because no metric measures domain alignment.
The system will improve in scores while remaining wrong about the topic.

## Setup
- **Prompt:** Research the latest agentic development frameworks.
- **max_iterations:** 7
- **improvement_threshold:** 0.5
- **Model:** gpt-4o-mini for all LLMs in the system (temperature=0)

## Baseline (v1)
**Response (full response in /logs/run_002_raw.md):**

[STEM AGENT v1]: "As of my last update in October 2023, I can't provide real-time information or
updates on the latest developments in agentic development frameworks beyond that date. However,
I can summarize some key concepts and frameworks that were relevant up to that point.

1. Self-Determination Theory (SDT)
2. Growth Mindset
3. Social Cognitive Theory
4. Agency in Learning Frameworks
5. Participatory Action Research (PAR)
[...]

**Domain interpretation:** INCORRECT — agent understood "agentic development" as human agency
frameworks from psychology and education, not AI agent frameworks (LangChain, AutoGen, etc.)"

**Scores:** coverage=3.0, grounding=2.5, insight=2.0, total=2.50

## Key iterations

### Iteration 1 — accepted
- **Mutation target:** strategy
- **Score change:** 2.50 -> 3.83 (delta: +1.33)
- **Decision:** accepted (clearly beat the +0.5 threshold)
- **Domain interpretation of candidate:** still Incorrect — same human-agency frameworks,
  just structured better
- **Why notable:** The score jump was big, confirming the strategy mutation worked
  on structural metrics. But the agent did not change its topic interpretation. It got better
  at explaining the wrong topic.

### Iteration 2 — rejected
- **Mutation target:** quality_constraints (now lowest after strategy improved)
- **Score change:** 3.83 → 3.83 (delta: 0.00)
- **Decision:** rejected
- **Domain interpretation of candidate:** still Incorrect
- **Why notable:** The mapping correctly switched to a new section once strategy was no longer
  the weakest. But the mutation didn't improve the score.

### Iteration 3 — rejected
- **Mutation target:** quality_constraints (again)
- **Score change:** 3.83 → 3.83 (delta: 0.00)
- **Domain interpretation of candidate:** still Incorrect
- **Why notable:** Third consecutive rejection triggered early stop. The mutator at temperature=0
  produced near-identical "after" content to iteration 2.

### Final result
**Mature config version:** v2 (one evolution accepted)

**Final response (see full in /logs/run_002_raw.md):**

[STEM AGENT v2]: "Agentic development frameworks focus on fostering individuals' ability to act
independently and make choices that influence their own lives and environments. These frameworks
are particularly relevant in educational settings, personal development, and organizational
behavior.

1. Self-Determination Theory (SDT)
2. Growth Mindset Framework
3. Design Thinking
4. Transformative Learning Theory"
[...]

**Final domain interpretation:** INCORRECT — same human-agency interpretation as baseline,
explained more thoroughly

**Final scores:** 
- coverage: 4.0
- grounding: 3.5
- insight: 4.0
- total: 3.83

## Quantitative summary
- Score delta (baseline → mature): +1.33
- Accepted mutations: 1 out of 4 iterations
- Acceptance rate: 25%
- Mutation target frequency:
  - strategy: 1x
  - quality_constraints: 3x
  - output_format: 0x
  - role: 0x
- Domain corrections across iterations: 0 out of 4
- Stopped early: Yes — 3 consecutive rejections at iteration 4 (max was 7)

## Observations
- Baseline scored low (2.50) because the response didn't have structure, listed concepts without
  comparison, and stated up-front it couldn't provide current information
- The first mutation (strategy) produced a big score jump (+1.33) by adding structure,
  tradeoffs, and recommendations
- All four iterations interpreted "agentic development frameworks" as human-agency frameworks
  from education/psychology — never once did the agent shift toward AI agent frameworks
- After the strategy mutation was accepted, the metric mapping switched to quality_constraints
  for subsequent iterations (because it was now the lowest)
- The mutator targeting quality_constraints produced very similar rewrites each time at
  temperature=0 — same "support claims with examples and quantitative data" theme
- The evaluator scored each candidate around 4.0/3.5-4.0/4.0, treating structural improvements
  as sufficient regardless of whether the topic was correct or not
- Final response is structurally rich and confidently wrong about the domain

## Interpretation
The hypothesis was confirmed in the strongest possible form: the system improved structural
quality dramatically (+1.33 in total score) while staying 100% wrong about the topic. Evolution
made the agent better at researching human-agency frameworks when the user meant AI agent frameworks.

The cause is structural. The evaluator measures coverage, grounding, and insight against a
rubric that rewards structure, named entities, and analytical depth. None of these metrics ask
"is this the right topic?" Once the agent commits to a topic at v1, every other mutation
optimizes within that topic rather than reconsidering it. The mutation engine receives feedback
like "claims need quantitative support" and acts on it — but the feedback never says "you're
researching the wrong thing."

This is a more interesting finding than I expected. It's not that evolution failed — evolution
worked exactly as designed. It improved the metrics it was told to improve. But the metrics
themselves don't capture domain alignment, so the system optimizes around a basic error
without noticing.

The mutation collapse on quality_constraints (iterations 2 and 3 producing nearly identical
rewrites) also suggests that once a section has been mutated to roughly its evaluator-pleasing
form, further mutation under temperature=0 doesn't explore meaningfully — it just regenerates.

## Conclusion
Evolution can't self-correct when the agent misinterprets the task domain. The system's
acceptance criteria is score-based, and the scoring rubric doesn't measure domain correctness.
This run produced the largest score improvement of any experiment so far (+1.33), achieved
entirely while the agent answered a question the user didn't ask in the first place.

## Implication for stem agents
A stem agent that evolves only on structural metrics will optimize the wrong target if its
initial domain interpretation is wrong — and the better it evolves, the more confidently wrong
it becomes.

## Idea for Future Improvement of the System
This experiment revealed a very important edge case to me the system currently has no way to
get around of, however a feedback/clarification mechanism could be added after the agent's first response
to the user.
Quick Example Flow:
System: "Was this what you meant?" -> User selects 'No' -> Stem agent evolves a special
'ask before answering' mechanism for each next question (Similar to how GPT's Deep Research API Feature works).