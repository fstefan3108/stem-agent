# Stem Agent

A prototype exploring how a generic agent can specialize into a Deep Research agent through initialization from examples and controlled configuration evolution.

## Core idea

AgentConfig is the key artifact: the agent's "genome". The system initializes it from examples, evaluates executions, mutates one field at a time, and accepts changes only when they improve measured performance.

## Current Status

## Phase 0 Completed — Foundations & Contracts

## Phase 1 Completed - Generic Stem Agent

## Phase 2 Completed - Evaluation of Performance

## Phase 3 In Progress - Evolution, the Core of the Project

# Completed:
- Created the MutationEngine component - successfully mutates a section of a prompt that scored
the lowest during evaluation. 
- Created the prompt for the llm prompt section rewriting
- Created the tests for the MutationEngine component and installed safeguards in the entire class

# Next:
- Implement the Evolution Orchestrator component that will run the current agent confguration and
the new configuration on the same task, then keep the configuration that scored better

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
5. Evolution loop
6. Safeguards and stopping
7. Measurement and write-up