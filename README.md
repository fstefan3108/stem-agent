# Stem Agent

A prototype exploring how a generic agent can specialize into a Deep Research agent through initialization from examples and controlled configuration evolution.

## Core idea

AgentConfig is the key artifact: the agent's "genome". The system initializes it from examples, evaluates executions, mutates one field at a time, and accepts changes only when they improve measured performance.

## Current Status

## Phase 0 Completed — Foundations & Contracts

## Phase 1 Completed - Generic Stem Agent

## Phase 2 - Evaluation of Performance COMPLETED

# Added:
- EvaluatorService - the main service for evaluating agent's responses and performance. It grades
the agent's answer based on strictly defined metrics, rules and guidelines. The llm does the intelligent
grading, then outputs a structured EvaluationResult.

Current Limitation: Both the evaluator and the stem agent itself seem to not realise when they misinterpet
what the user is actually asking about. Might improve with an inclusion of a web search tool later on.

- Updated the dataset to be a dataset of scoring examples used to tell the evaluator how to properly
score agent's answers.
- Created tests for the evaluator and covered identified edge cases.
- Minor code optimizations such as moving prompts outside of service classes, etc.

# Next:
- Start Phase 3

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