# Stem Agent

A prototype exploring how a generic agent can specialize into a Deep Research agent through initialization from examples and controlled configuration evolution.

## Current status

Phase 0: project skeleton and folder structure with key files identified from day 1 planning and architecting.

## Core idea

AgentConfig is the key artifact: the agent's "genome". The system initializes it from examples, evaluates executions, mutates one field at a time, and accepts changes only when they improve measured performance.

## Current Status

Phase 0 in progress.

Completed:
- Project structure and repository setup
- PromptSection schema with validation
- Contract tests for prompt section behavior

Next:
- AgentConfig schema
- EvaluationResult schema
- EvolutionRecord schema

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