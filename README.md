# Stem Agent

A prototype exploring how a generic agent can specialize into a Deep Research agent through initialization from examples and controlled configuration evolution.

## Core idea

AgentConfig is the key artifact: the agent's "genome". The system initializes it from examples, evaluates executions, mutates one field at a time, and accepts changes only when they improve measured performance.

## Current Status

## Phase 0 Completed — Foundations & Contracts

## Phase 1 Completed - Generic Stem Agent

## Phase 2 - Specialization -> DROPPED
# Reasoning:
- I've observed that the specializaiton phase was unneccessary and even contradictory to our core concept
of the project. The main discovery from this unsuccessful phase is: *Specialization is part of evolution*
meaning that not only was specialization redundant, but it turned the agent from generic to an immediate
task-specific expert, making progress tracking too fast and unable to monitor. 
The main initial reason for a specialization phase was a mindset I had in the beginning that the agent
should be able to evolve and adapt to multiple tasks, but for the scope of this project we are keeping
it focused on one single specific task.

## NEW Phase 2 - Evaluation of Performance - IN PROGRESS

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