# Stem Agent

A prototype exploring how a generic agent can specialize into a Deep Research agent through initialization from examples and controlled configuration evolution.

## Core idea

AgentConfig is the key artifact: the agent's "genome". The system initializes it from examples, evaluates executions, mutates one field at a time, and accepts changes only when they improve measured performance.

## Current Status

## Phase 0 Completed — Foundations & Contracts

Defined the core system contracts for the stem agent prototype:

- Implemented schema “genome” models:
  - PromptSection
  - AgentConfig
  - EvaluationResult
  - EvolutionRecord
  - TaskExample

- Added validation rules and safeguards for:
  - prompt mutation integrity
  - configuration consistency
  - evaluation scoring bounds
  - evolution trace constraints
  - dataset example structure

- Wrote contract/unit tests (51 passing) covering valid behavior, edge cases, and failure conditions.

Outcome:
The project now has a validated foundation for initialization, execution, evaluation, and evolution before implementing the runtime agent loop.

Next:
- Phase 1

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
3. Initialization from examples
4. Evaluation system
5. Evolution loop
6. Safeguards and stopping
7. Measurement and write-up