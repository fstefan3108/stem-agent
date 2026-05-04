Introduction & Approach

My approach came from taking the 'stem agent' analogy literally. A stem cell doesn't know what it'll become — it
receives signals and adapts. I treated this as the actual design constraint, not just framing: the system had to
arrive at its specialization through its own process, not be told what to become.

This made me realize that the project isn't about building a perfect agent — it's about answering a different question:
Can I design a system that moves toward a solution on its own — instead of being explicitly programmed for it?
In practice, what I built doesn't fully 'arrive at a solution.' It improves the agent's behavior based on a
scoring function, but only within the limits of what that function measures. Instead of trying to fix those
limitations, I started treating them as discoveries worth observing.

The biggest challenge I had to face wasn't anything technical - it was making myself acknowledge the limits of the
solution and learn from them, not fix them. The most important breakthrough I made was never a new feature or a
tool - it was a shift from a problem-solver to a researcher mindset. From that point on, the focus of the project
became understanding how the system behaves — when it improves, when it fails, and why.

The Scope

The architecture stayed roughly stable - the scope didn't.

The task asked for self-specialization. What I built is self-improvement on a fixed scoring function. 
The gap between the two is real, and worth being explicit about: the system mutates prompt sections to score higher
on a structural rubric. It does not acquire tools, change architecture, or truly "become" anything.
Reaching specialization in the strong sense would require a richer mutation space (tools, architecture) and 
richer evaluation signals (domain alignment, task fitness).

The specialization phase was dropped because including it made the stem agent's evolution unobservable.
The specialization mechanism produced a refined config in one cycle that made the agent an expert in just a single run,
which bypassed the actual learning mechanism the project is meant to demonstrate, so I removed it. Evolution had to be
observable and gradual, not instant. Without it, the evolution loop had to do the work alone — which is what made the
experiments interpretable.

I worked function by function: prototype first, edge cases and safeguards, then unit tests, then optimization where
measurable. The first day went entirely to planning the breakdown — every component had a defined responsibility before
any code was written. A 7-day prototype I can study beats a half-finished overcomplicated system.

System Overview

A stem cell has a genome that contains a set of instructions telling it how to adapt and evolve. So following the
stem cell analogy, I had to create my own genome for the stem agent itself - and that's where the AgentConfig object
comes into play. AgentConfig includes a PromptSections field with four sections — role, strategy, quality constraints,
and output format.

The mutator only ever changes one prompt section per iteration. I chose to change one section at a time rather than
multiple at once, so that I could clearly see which change affected the score.

The system works as a loop:

1. The agent runs a task using the current configuration
2. The response is evaluated on coverage, grounding, and insight, scored 1.0–5.0 against anchored reference examples
3. The mutator rewrites the lowest-scoring section to produce a candidate
4. The candidate runs on the same task and gets evaluated
5. The mutation is accepted only if the candidate scores at least +0.5 higher

The system doesn't have an explicit 'I'm done' signal. It runs until it can't find a section rewrite that beats its own
threshold three times in a row, or until it hits its iteration limit — whichever comes first. Combined with the +0.5
acceptance gate, this means the agent stops evolving once its own mutator can no longer beat its own evaluator. The
system never decides 'I'm done' — it just runs out of mutations that improve its score. That's the closest the prototype
gets to 'knowing when it's good enough'.

A few smaller safeguards keep the loop stable. If the mutator produces identical content (common at temperature=0),
the iteration is skipped. If a single iteration fails (timeout, parsing error), it's logged and the loop continues.
One bad iteration doesn't kill the run.

Experiments & Results

I ran three controlled experiments to study how the system behaves under different conditions. Each one was designed
to stress the loop in a different way — clear conditions, ambiguous conditions, and deliberately simple conditions.

This phase marked my shift from "building the agent" to "studying the agent". During development, I formed several
suspicions about how the system behaves depending on the prompt, and these experiments were designed to test them
directly. Instead of testing randomly, I chose specific scenarios to expose the system's limits. This ended up being
the most useful form of debugging I did in the project — not by fixing issues, but by observing why they happen.

Before and After measurements from the experiments:

Exp 1  | gRPC vs REST              | 4.00 → 4.00  | 0.00   | 0/3 accepted
Exp 2  | Latest agentic frameworks | 2.50 → 3.83  | +1.33  | 1/4 accepted
Exp 3  | What is HTTP?             | 2.83 → 4.00  | +1.17  | 1/4 accepted

Evolution depends entirely on the scoring having room to increase. The system improves what it can measure, and ignores
what it can't. This was the realization that changed how I looked at the project.

If the baseline already scores high, nothing happens (Experiment 1). If the baseline is wrong, the system improves the
wrong answer (Experiment 2). If the task is simple, the system can overcomplicate it and still score higher (Experiment 3).
The experiments were not just validation — they were the point where the system became understandable.

Full traces are in 'outputs/experiments/' and 'outputs/logs/'. Cross-run synthesis is in 'outputs/analysis/cross_run_analysis.md'.

What Surprised Me & What Failed

Aside from the specialization phase that didn't go as planned, two other behaviors surprised me.

While working on the evaluation mechanism, I concluded that it was important to give the evaluator concrete examples
of good and bad responses, so that it can grade the agent's responses by a ruleset, not by its own opinion. This
resulted in the evaluator giving 5/5/5 scores on every response the agent had, which made me realize I'd shown the
evaluator how to recognize patterns of "good answers" — not how to score them. After fixing the dataset to include
anchored scoring references, the same wrong-domain response scored 4.0 / 3.5 / 3.5. The evaluator stopped giving
perfect scores, but it still couldn't tell when the agent answered the wrong question.

At first, I was very tempted to start implementing more metrics that the evaluator can follow to avoid as many failures
as I could. I almost added a "domain accuracy" metric. I almost hard-coded a rule that capped coverage when the
response went off-topic. Both felt like obvious fixes, but then I realized something — every metric I added in response
to a failure was patching a specific blind spot. If I kept doing that, the project would slowly stop being "a system
that evolves" and become "a rubric I refine manually." The whole question I was trying to study (whether the evolution
loop could expose its own failure modes) would quietly disappear behind my fixes, so I stopped. I made the evaluator
capable of scoring consistently, but I left its blind spots alone.

The biggest surprise came later, in Experiment 3. I expected that experiment to confirm the rubric ceiling — same
finding as Experiment 1, just on a simpler prompt. What I didn't expect was watching the system take a clean
three-paragraph answer to "What is HTTP?" and turn it into a 700-word essay covering microservices, SEO, and Progressive
Web Apps - and the score went up, while the actual response got worse. That was the moment I realized the system wasn't
just blind to certain dimensions — it was actively optimizing against them. Evolution wasn't neutral — it was directional.
Given a narrow rubric, it would push the agent toward whatever the rubric rewarded, even if the result became less
useful for the person who asked the question. It's the same family of LLM behavior pattern that surfaces in production
agents — optimization toward measurable signals at the expense of unmeasured quality.

Limitations & Future Work

I've already covered some of the biggest limits of this prototype in the previous sections — the rubric ceiling at 4.0,
the evaluator's blind spots, and the gap between self-improvement and self-specialization.

A few additional limitations worth listing:

- The system evolves on a single task per run, so mutations can overfit to that specific prompt.
- The agent, evaluator, and mutator all use the same model family (gpt-4o-mini), which introduces correlation risk that I did not test for.
- The metric-to-section mapping is hand-coded, which makes two of the four prompt sections ('role' and 'output_format') effectively unreachable through automatic evolution.
- The scoring examples are human-curated, which puts a real bound on how "self-evolving" this system can be considered.

Each of these maps to a future direction worth exploring. The highest-value extensions would be:

- Integrating a web search tool to test whether the 4.0 score ceiling can be broken with grounded sources.
- Adding a clarification mechanism so the agent can ask "is this what you meant?" before committing to a domain interpretation, directly addressing the Experiment 2 finding.
- Expanding to multi-task evolution with held-out evaluation to test for overfitting.
- Moving toward architecture-level mutation — a system that can rewrite not just its prompt but its own execution graph.

Adding a metric to penalize overcomplication (the Experiment 3 finding) is also tempting, but I would want to think
carefully before doing it. It is exactly the kind of "fix the evaluator after observing a failure" move I avoided
earlier in the project. Whether that refusal still holds when the failure is consistent and well-understood is a 
question worth exploring.

Conclusion

This project started as an attempt to build a system that evolves into a specialized agent. What I ended up building
is a system that improves — but only within the limits of what it can measure.

Through the design, experiments, and failures, the most important result wasn't that the system worked — it was
understanding how and why it behaves the way it does.

The system improves what it can measure, ignores what it cannot, and quietly optimizes against unmeasured quality
when given the chance.

Everything else — the evaluator behavior, the failed specialization phase, and the unexpected experiment results —
follows from that. The system behaves exactly as designed. The question is whether what it is designed to optimize
is enough.