# Stem Agent

A prototype exploring how a generic agent can specialize into a Deep Research agent through initialization from examples and controlled configuration evolution.

## Core idea

AgentConfig is the key artifact: the agent's "genome". The system initializes it from examples, evaluates executions, mutates one field at a time, and accepts changes only when they improve measured performance.

## Project Goal

This project explores whether an AI agent can improve itself through a controlled evolution loop, without manual intervention.

The focus isn't on building the best agent, but on observing how and when self-improvement works, where it fails, and why.

## Current Status

## Phase 0 Completed — Foundations & Contracts

## Phase 1 Completed - Generic Stem Agent

## Phase 2 Completed - Evaluation of Performance

## Phase 3 Completed - Evolution, the Core of the Project

## Phase 4 In Progress - The Study, Research, and Analysis of the Stem Agent System

# Completed
- Reorganized file structure for the research side of the project
- Saved the findings we discovered while developing from the actual experiments
- Completed experiment #1, experiment #2, experiment #3 (more in /outputs directory)

# Next
- Write the cross-run analysis of the experiments

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

## Experiments

Experiments are located in `/outputs/experiments/`, with raw logs in `/outputs/logs/` and cross-run analysis in `/outputs/analysis/`.