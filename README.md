## Problem

Gameplay and backend regressions are often discovered late when validation relies heavily on manual testing, increasing feedback time and making failures across game, API, and integration layers harder to isolate.

## Solution

Built a layered automated testing strategy covering deterministic gameplay rules with Unity Test Framework, backend/API validation, integration tests, and performance checks — all integrated into CI as automated quality gates.

## Quality Strategy

**EditMode → PlayMode → API → Integration → Performance → Exploratory Testing**

Each layer targets a different type of risk:

- **EditMode:** fast validation of deterministic game logic.
- **PlayMode:** gameplay behavior and Unity runtime interactions.
- **API:** backend contracts, error handling, and business rules.
- **Integration:** communication and state consistency across components.
- **Performance:** latency, throughput, and behavior under load.
- **Exploratory Testing:** experience, unexpected behavior, and risks that require human judgment.

## Impact

Earlier regression detection, faster developer feedback, repeatable validation, and better failure isolation before builds reach manual QA — allowing exploratory testing to focus on higher-risk and less deterministic behavior.

```text
Unity Game ──────► Backend API ──────► AI NPC
    │                   │
Unity Tests          Pytest
                        │
                    k6 Performance

         └──── GitHub Actions ────┘
                  Quality Gate
```
