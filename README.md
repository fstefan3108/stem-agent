# Stem Agent

A prototype exploring how a generic agent can specialize into a Deep Research agent through initialization from examples and controlled configuration evolution.

## Core idea

AgentConfig is the key artifact: the agent's "genome". The system initializes it from examples, evaluates executions, mutates one field at a time, and accepts changes only when they improve measured performance.

## Current Status

## Phase 0 Completed — Foundations & Contracts

## Phase 1 Completed - Generic Stem Agent

## Phase 2 Completed - Evaluation of Performance

## Phase 3 Completed - Evolution, the Core of the Project

# Completed
- MutationEngine: rewrites the lowest-scoring prompt section based on rule-based metric->section mapping
- Mutator prompt for targeted, single-section LLM rewrites
- EvolutionEngine: orchestrates the full loop — baseline evaluation, candidate generation, comparison against current config on the same task, accept/reject by improvement threshold
- EvolutionRecord audit trail for every accepted and rejected mutation
- Safeguards: no-op mutation detection, consecutive rejection early stopping, per-iteration error isolation
- Tests for MutationEngine and EvolutionEngine covering routing, acceptance, rejection, no-op handling, and loop bounding

# Next
# The Analysis, Study, and Research of the Developed System
Up until now, I've been mostly focused on developing the Stem Agent as best as I can, keeping in
mind that the core requirement of the project is to analyze and study the agent's behaviour, not
make it as perfect as possible.
So now comes the research part of the system, I will be experimenting with the behaviour of the stem agent that
has a core evolution mechanism, and write up a thorough research on the whole system.
- Run experiments across multiple prompts to gather evolution traces
- Write up findings (4-page doc): approach, results, surprises, limitations
- Polish README with usage instructions

## Development Approach

Each component is developed in this order:

1. Analyze before coding
2. Build minimal working prototype
3. Cover edge cases
4. Add tests
5. Optimize only if needed
6. Update readme

## Planned phases

1. Skeleton & schemas
2. Generic stem executor
3. Initialization from examples (Dropped)
4. Evaluation system
5. Evolution loop with Safeguards
6. Experimental study (running 3-4 prompts, capturing logs)
7. Write-up (4 pages)
8. README polish + setup instructions