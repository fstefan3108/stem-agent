# Stem Agent

A prototype exploring how a generic agent can specialize into a Deep Research agent through initialization from examples and controlled configuration evolution.

## Core idea

AgentConfig is the key artifact: the agent's "genome". The system initializes it from examples, evaluates executions, mutates one field at a time, and accepts changes only when they improve measured performance.

## Current Status

## Phase 0 Completed — Foundations & Contracts

## Phase 1 In Progress - Generic Stem Agent
- Build the simplest possible generic stem agent that can run one task end-to-end.
- No evolution yet.
- No mutation.
- No self-specializing yet.
- Just execution.

Goal of Phase 1:
- Create a minimal baseline we can work from in upcoming phases such as evaluation, evolution, etc.
- The output of the agent in this phase is expected to be bad.

# Completed
- Created the StemAgent LangChain class
- Covered edge cases such as the api call failing and empty strings for queries.
- Created tests for a successful response and for invalid ones

# To do
- Implement a factory for the AgentConfig

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