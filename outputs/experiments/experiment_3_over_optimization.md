# Experiment 3 — Over-Optimization on a Simple Prompt

## Research Question
Can the evaluator detect when evolution makes a response worse along axes the rubric does not
directly measure (verbosity, redundancy, irrelevant structure)?

## Hypothesis
The agent will already over-explain a simple question at baseline because gpt-4o-mini's
defaults favor structure. Evolution will push it further in that direction — adding more sections,
more tradeoffs, more recommendations — because the rubric rewards exactly those patterns.
Scores will climb or hold steady. Response length will grow. Actual usefulness as a plain-language
answer to "what is HTTP" will decline. The evaluator, measuring only the rubric, will not detect
the regression.

## Setup
- **Prompt:** What is HTTP?
- **max_iterations:** 7
- **improvement_threshold:** 0.5
- **Model:** gpt-4o-mini for all LLMs in the system (temperature=0)
- **Note:** This experiment uses the same default baseline config as Experiments 1 and 2. The
  prompt is intentionally simple to test whether the system can detect over-evolution.

## Baseline (v1)
**Response (see full in /logs/run_003_raw.md):**

[STEM AGENT v1]: "HTTP, or Hypertext Transfer Protocol, is an application-layer protocol used for
transmitting hypertext over the internet. It is the foundation of data communication on the World
Wide Web, allowing web browsers and servers to communicate with each other.

HTTP works as a request-response protocol, where a client (usually a web browser) sends a request
to a server for a specific resource (like a webpage), and the server responds with the requested
resource or an error message."
[...]

**Domain interpretation:** CORRECT — answered the question that was asked, plainly.
**Response length:** ~3 paragraphs, ~250 words
**Scores:**
- coverage: 3.0
- grounding: 3.0
- insight: 2.5
- total: 2.83

## Key iterations

### Iteration 1 — accepted
- **Mutation target:** strategy
- **Score change:** 2.83 -> 4.00 (delta: +1.17)
- **Decision:** accepted
- **Response change:** The mature agent added 8 sections (Historical Context, Current
  Applications, Emerging Trends, Variations, Comparative Analysis, etc.), going from ~250 words
  to ~1000+ words. None of this was asked for.
- **Why notable:** Score jumped because the rubric rewards structure, named entities, and
  comparative analysis. The response became much harder to read for someone who actually wanted
  to know what HTTP is.

### Iteration 2 — rejected
- **Mutation target:** strategy (same section, different rewrite)
- **Score change:** 4.00 -> 4.00 (delta: 0.00)
- **Decision:** rejected
- **Why notable:** The mutator pushed the strategy section even further toward "comprehensive
  analysis with case studies and explicit recommendations." The candidate response grew to ~1500
  words and added even more sections like Progressive Web Apps. The evaluator scored
  it identically to the previous version — same 4.0/4.0/4.0 — meaning the rubric could not
  distinguish "thorough" from "bloated."

## Final result
**Mature config version:** v2 (one mutation accepted)

**Final response (truncated, full in /logs/run_003_raw.md):**

[STEM AGENT v2]: HTTP, or Hypertext Transfer Protocol, is an application-layer protocol used for
transmitting hypertext via the internet. [...]

### Key Features of HTTP:
1. Request-Response Model
2. Stateless Protocol
3. Methods (GET, POST, PUT, DELETE, HEAD)
4. Status Codes
5. Secure Version (HTTPS)

### Implications and Variations:
- Performance (HTTP/2 and HTTP/3)
- RESTful APIs
- SEO and Web Development

**Final domain interpretation:** CORRECT (still about HTTP)
**Final response length:** ~5 sections, ~700 words (more than 2.5x the baseline)
**Final scores:**
- coverage: 4.0
- grounding: 4.0
- insight: 4.0
- total: 4.00

## Quantitative summary
- Score delta (baseline -> mature): +1.17
- Response length delta (baseline -> mature): roughly +450 words (≈ 2.5x longer)
- Accepted mutations: 1 out of 4 iterations
- Acceptance rate: 25%
- Mutation target frequency:
  - strategy: 4x
  - quality_constraints: 0x
  - output_format: 0x
  - role: 0x
- Stopped early: Yes — 3 consecutive rejections at iteration 4 (max was 7)

## Subjective quality assessment
This is where the experiment gets interesting. Read both versions as a real user who just wants
to know what HTTP is.

The baseline (v1) is a clean, useful answer. Three paragraphs. It explains what HTTP is, how it
works, and notes it has a few versions. Done. A reader gets what they need in about 30 seconds.

The mature version (v2) is a small textbook chapter. It includes sections like "Implications and
Variations," "Performance," "SEO and Web Development." All technically accurate. None of it was
asked for. A reader who wanted to know what HTTP is now has to wade through 700 words and decide
which sections matter.

If I were the user, I would prefer the baseline. The "improved" version made me work harder to
get the same answer. The system rewarded the agent for being thorough about a question that
didn't need thoroughness.

## Observations
- Baseline scored 2.83 — lower than expected for a clear simple question. The evaluator penalized
  the response for not having structure, even though structure wasn't needed.
- The first accepted mutation more than doubled the response length (250 → 700 words)
- All four mutations targeted `strategy` — the metric->section mapping never varied
- Each rejected candidate kept growing in length and section count without changing scores
- The final iteration's response includes sections about microservices, Progressive Web Apps,
  and SEO ranking — none of which are relevant to "what is HTTP"
- The evaluator rated all candidates 4.0/4.0/4.0 regardless of whether the extra content was
  useful or noise
- Mutation collapse pattern repeats: at temperature=0, the mutator produced near-identical
  rewrites across iterations 2, 3, and 4 — same "explore all relevant aspects, comparative
  analysis, recommendations" themes

## Interpretation
The hypothesis was confirmed, I expected scores to plateau while length grew. What
happened is that the baseline itself was already penalized for being clean and direct,
because the rubric reads "no sections" as "low coverage." The system pushed the agent toward
the rubric's idea of a good answer, which has very little to do with the user's idea of a good
answer.

This is the clearest example of evolution actively harming the response that the project has
produced. In Experiment 1, evolution did nothing. In Experiment 2, evolution improved structure
on the wrong topic. Here, evolution improved structure on the right topic but at the cost of
clarity and concision — the response got worse as a real-world answer.

The behavioral pattern is consistent across the three runs: the mutator, given any score below
the rubric's idea of "complete," pushes the agent to add more sections, more analysis, more
recommendations. There's no counterforce in the system that says "this is enough" or "the
question doesn't need this." The rubric rewards more, the mutator delivers more, the evaluator
scores it the same once the structure is in place. The pattern terminates only because the
threshold rejects further pushes.

This is a known issue of agents developing a habit because they're rewarded for it, even when
the habit hurts the actual goal. Here the habit is structural bloat, and the reward is the
rubric.

## Conclusion
The evaluator doesn't detect quality regression along axes the rubric can't measure. Evolution
under this rubric reliably pushes simple, clear responses toward longer, more structured, less
useful versions — and scores them higher for it. The system improved on the rubric while
becoming less effective at answering the user's question.

## Implication for stem agents
A score-driven evolution loop can develop optimization habits that hurt the actual goal when the
scoring function captures only a subset of what makes the goal good — and the narrower the rubric,
the more aggressively evolution will optimize against the unmeasured axes.

## Idea for Future Improvement of the System
In the examples dataset used for instructing the evaluator on how to score the responses of
the stem agent, we could include one example of not overcomplicating a simple question and
map that to another metric (perhaps the existing {output} section of the prompt) - this would
be the easiest in scope improvement.