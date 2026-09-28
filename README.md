# 🎮 Game QA Automation Lab

> A layered QA strategy for a 2D platformer combining **test automation,
> REST gameplay telemetry, AI-powered visual regression, and CI quality
> gates**.

## Overview

This project is a QA Automation Lab built around a simple 2D platformer
whose core gameplay is:

**Spawn → Move / Jump → Collect → Die → Respawn**

The goal is not to automate everything. Instead, the project applies
different testing techniques to problems where they provide clear QA
value.

The lab demonstrates four main engineering skills:

-   **Test Automation** --- Unity Test Framework, NUnit, and Pytest
-   **REST API Testing** --- FastAPI gameplay telemetry and automated
    API validation
-   **Artificial Intelligence** --- Computer Vision / YOLO for black-box
    visual gameplay validation
-   **Continuous Integration** --- GitHub Actions as a Quality Gate

------------------------------------------------------------------------

## QA Problem

Gameplay regressions are often discovered late through repetitive manual
validation.

For a game build, QA may repeatedly need to verify questions such as:

-   Did the player spawn correctly?
-   Is the expected gameplay element visible?
-   Did the player die and respawn correctly?
-   Are gameplay events being recorded correctly?
-   Where are players dying most frequently?

This project explores how these checks can be automated at different
layers without coupling every test to the game's internal
implementation.

------------------------------------------------------------------------

## Test Strategy

``` text
                         2D PLATFORMER
                               │
                  ┌────────────┴────────────┐
                  │                         │
                  ▼                         ▼
            GAME INTERNAL               GAME BUILD
                  │                      Game.exe
                  ▼                         │
        Unity Test Framework                ▼
          Component Tests          AI Visual Regression
                                    Python + YOLO + Pytest
                                              │
                                              ▼
                                        PASS / FAIL

                               GAMEPLAY EVENTS
                                      │
                                      ▼
                                   FastAPI
                                      │
                                      ▼
                               Telemetry Storage
                                      │
                                      ▼
                                Death Analytics
                                / Death Heatmap

                         ───────────────────────
                              GitHub Actions
                                  │
                                  ▼
                             QUALITY GATE
```

------------------------------------------------------------------------

## 1. Unity Component Automation

### Goal

Detect regressions in deterministic game rules quickly before relying on
a complete game build.

### Stack

-   Unity Test Framework
-   NUnit
-   PlayMode / component-level tests

### Current tests

-   [x] `StartsWithMaxHealth`
-   [x] `DamageReducesHealth`

These tests intentionally remain small. They validate component behavior
and are **not presented as end-to-end gameplay regression tests**.

------------------------------------------------------------------------

## 2. AI-Powered Visual Gameplay Regression

### QA problem

Some gameplay checks are valuable specifically against the **compiled
game**, where QA validates the product as a player would see it.

### Approach

The Windows game build is treated as a **black box**.

``` text
Game.exe
   │
   ▼
Screen Capture
   │
   ▼
YOLO / Computer Vision
   │
   ▼
Visual Game State
   │
   ▼
Python + Pytest
   │
   ▼
PASS / FAIL + Evidence
```

The visual test agent should not depend on internal Unity state such as:

-   `PlayerController`
-   `Health`
-   `Transform`
-   `TokenInstance`

Instead, it observes what is actually rendered by the executable.

### Initial POC

The first proof of concept is intentionally small:

1.  Start the game build.
2.  Capture the game screen.
3.  Detect the player visually.
4.  Return the bounding box and confidence.
5.  Save visual evidence.
6.  Determine PASS / FAIL.

### Planned visual regression scenarios

-   [ ] Player spawn detection
-   [ ] Death / respawn detection
-   [ ] Token detection / collection

The objective is **not to create an AI that completes the game**.
Computer Vision is used to observe relevant gameplay states for QA.

------------------------------------------------------------------------

## 3. Gameplay Telemetry REST API

### QA problem

Knowing that players die is useful, but QA and Game Design can gain more
value by answering:

> **Where are players dying most frequently?**

Repeated deaths in the same region can indicate an area worth
investigating for difficulty, level design, collision issues, or other
gameplay problems.

### Solution

The Unity game sends gameplay telemetry to a REST API built with
FastAPI.

Example:

``` http
POST /events
Content-Type: application/json
```

``` json
{
  "event": "player_died",
  "level": "SampleScene",
  "x": 18.4,
  "y": 2.1
}
```

### Initial gameplay events

``` text
level_started
token_collected
player_died
```

The main analytical use case is `player_died`, including the player's
position when the event occurred.

------------------------------------------------------------------------

## 4. REST API Test Automation

The telemetry API has its own automated regression suite using
**Pytest**.

### Planned API tests

-   [x] `POST /events` accepts a valid `player_died` event
-   [x] Event is persisted correctly
-   [x] Invalid events are rejected
-   [x] Death events can be retrieved
-   [x] Deaths can be filtered by level
-   [x] Death coordinates are preserved correctly

This layer demonstrates:

-   REST
-   HTTP methods
-   JSON
-   Status codes
-   Request / response validation
-   API contracts
-   FastAPI
-   Pytest

------------------------------------------------------------------------

## 5. Death Analytics

Recorded death coordinates can be aggregated to identify regions with a
high concentration of deaths.

Example endpoint:

``` http
GET /analytics/deaths?level=SampleScene
```

Example response:

``` json
{
  "total_deaths": 37,
  "hotspots": [
    {
      "x_start": 17,
      "x_end": 20,
      "deaths": 16
    }
  ]
}
```

### Planned output

A **Death Heatmap** showing where deaths are concentrated across the
level.

``` text
LEVEL
──────────────────────────────────────────►

     ☠

                  ☠
               ☠ ☠ ☠
                ☠ ☠        ← hotspot

                                  ☠
```

The heatmap is intended to support QA investigation rather than
automatically classify a region as a defect.

------------------------------------------------------------------------

## 6. Continuous Integration

GitHub Actions acts as the project's **Quality Gate**.

``` text
                    PUSH / PULL REQUEST
                            │
                            ▼
                      GitHub Actions
                            │
             ┌──────────────┼──────────────┐
             ▼              ▼              ▼
        Unity Tests      API Tests       Build
             │              │              │
             ▼              ▼              ▼
           PASS           PASS           PASS
             └──────────────┼──────────────┘
                            ▼
                       QUALITY GATE
                       PASS / FAIL
```

AI visual tests will be integrated into CI after the local POC is
reliable, since executing a graphical game build in CI may require
dedicated runner infrastructure.

### Planned CI evidence

-   Test results
-   Pytest reports
-   Logs
-   Game build artifacts
-   AI detection screenshots
-   Visual regression evidence

------------------------------------------------------------------------

## Repository Structure

``` text
game-qa-automation-lab/
│
├── unity-game/
│   ├── Assets/
│   └── Tests/
│
├── api/
│   ├── app/
│   └── tests/
│
├── ai-tests/
│   ├── detector/
│   ├── tests/
│   └── evidence/
│
├── analytics/
│   └── death-heatmap/
│
├── .github/
│   └── workflows/
│       └── quality-gate.yml
│
└── README.md
```

------------------------------------------------------------------------

## Roadmap

### Phase 1 --- Unity Automation

-   [x] Configure Unity Test Framework
-   [x] Configure Assembly Definitions
-   [x] Implement `StartsWithMaxHealth`
-   [x] Implement `DamageReducesHealth`

### Phase 2 --- REST API / Gameplay Telemetry

-   [ ] Create FastAPI application
-   [ ] Implement `POST /events`
-   [ ] Implement `player_died`
-   [ ] Send `level`, `x`, and `y`
-   [ ] Persist telemetry
-   [ ] Implement death event retrieval
-   [ ] Create Pytest API regression suite

### Phase 3 --- Death Analytics

-   [ ] Aggregate deaths by region
-   [ ] Implement `GET /analytics/deaths`
-   [ ] Identify death hotspots
-   [ ] Generate death heatmap

### Phase 4 --- AI Visual Regression

-   [ ] Generate Windows game build
-   [ ] Capture the executable screen
-   [ ] Detect the player
-   [ ] Configure / train YOLO
-   [ ] Generate bounding boxes and confidence
-   [ ] Implement spawn visual test
-   [ ] Implement death / respawn visual test
-   [ ] Implement token visual test
-   [ ] Integrate visual assertions with Pytest
-   [ ] Save screenshots as evidence

### Phase 5 --- CI

-   [ ] Create GitHub Actions workflow
-   [ ] Run Unity component tests
-   [ ] Run API tests
-   [ ] Generate game build
-   [ ] Publish test artifacts
-   [ ] Configure Quality Gate
-   [ ] Integrate AI visual tests when runner infrastructure is ready

### Phase 6 --- Portfolio Evidence

-   [ ] Architecture diagram
-   [ ] Test Strategy documentation
-   [ ] YOLO detection GIF / video
-   [ ] Death Heatmap
-   [ ] REST API documentation
-   [ ] Green CI pipeline
-   [ ] Example regression causing the Quality Gate to fail

------------------------------------------------------------------------

## Tech Stack

  Area                   Technology
  ---------------------- ------------------------------
  Game                   Unity / C#
  Component Testing      Unity Test Framework / NUnit
  API                    Python / FastAPI
  API Automation         Pytest
  AI / Computer Vision   YOLO
  Visual Test Agent      Python
  Analytics              Python
  CI                     GitHub Actions
  Version Control        Git / GitHub

------------------------------------------------------------------------

## What This Project Demonstrates

This project is designed to demonstrate more than tool usage.

It demonstrates the ability to:

-   Select the appropriate test layer for each risk.
-   Distinguish component testing from black-box gameplay regression.
-   Automate REST API validation.
-   Apply Computer Vision to an observable QA problem.
-   Collect gameplay telemetry for quality investigation.
-   Turn telemetry into actionable death analytics.
-   Integrate automated checks into a CI Quality Gate.
-   Preserve test evidence for debugging and reporting.

------------------------------------------------------------------------

## Portfolio Summary

> **Designed a layered QA strategy for a 2D platformer combining Unity
> component automation, REST gameplay telemetry, automated API testing,
> AI-powered black-box visual regression, death analytics, and CI
> quality gates.**

------------------------------------------------------------------------

## Status

🚧 **Work in progress**

Current focus:

**Gameplay Telemetry REST API → `player_died` event → death coordinates
→ automated API tests.**
