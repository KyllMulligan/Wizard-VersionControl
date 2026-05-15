# HexShard Online PoC Implementation Plan

> **For Hermes:** Use subagent-driven-development skill to implement this plan task-by-task.

**Goal:** Implement a minimal functional client/server loop demonstrating player movement on a hexagonal grid, traversing from 'Shard Zero' into connected shard environments, and establishing the fundamental data flow (Input $\rightarrow$ Server State Update $\rightarrow$ Client Render).

**Architecture:** The system must utilize an Outbox Relay pattern to guarantee state persistence while maintaining low-latency gameplay. Player visibility relies on proximity checks across simulated shards.

**Tech Stack:** JavaScript/HTML Canvas or Three.js (Client), Python/websockets (Server), PostgreSQL conceptual model for durability.

---
### Directory Structure & Core Components:
├── client/
│   └── main.js          # Client rendering loop and input handler
├── server/
│   ├── auth_service.py  # Handles user authentication, session codes, and name registry
│   ├── shard_zero_state.py # Manages state for the central hub (Shard Zero)
│   └── hexagon_math.py  # Utility functions for hex coordinates
├── tests/
│   └── test_movement.py  # Unit tests for movement and state sync cycle
└── README.md            # Project documentation

## Development Workflow (The PoC Phases)

### Phase 1: Core Grid Movement & State Sync (COMPLETED!)
**Focus:** Prove a player character can move smoothly between adjacent hexagons starting from 'Shard Zero', confirming reliable position updates via the simulated network state sync cycle (`shard_zero_state`).

### Phase 2: Authentication and Naming (COMPLETE!)
**Focus:** Implement robust, session-based identity management. Players must log in using a generated code and be able to reserve a unique name ('Sacred Name'). This confirms the *identity* layer is stable before we deal with world traversal.
*(Dependencies added: `server/auth_service.py`)*

### Phase 3: Shard Transition & Persistence (NEXT FOCUS)
**Goal:** Implement the logic for transitioning players from the central hub ('Shard Zero') into a dedicated, separate shard instance while maintaining visibility to nearby shards. This is where we prove the core scalability concept.

**Task 3.1: The Shard Connection Logic (Server)**
*   Modify `shard_zero_state.py` and add methods in `auth_service.py`.
*   When a player moves far enough from Shard Zero, the server must trigger a "Transition Event."
*   The transition event should move the player's record to a new simulated shard state (e.g., `ShardA`, `ShardB`).

**Task 3.2: Inter-Shard Visibility and Data Flow**
*   Update the client's understanding of data reception: The client must now receive *two types* of updates:
    1.  **Local:** Updates from the player's current shard instance.
    2.  **Remote/Visible:** Updates for entities (players) hosted on nearby, but separate, shards that are within range.
*   Update `shard_zero_state.py` to use `get_nearby_visible_players` and broadcast these remote entity updates to the client's render loop.

**Task 3.3: Persistence Integration (The Outbox Test)**
*   Simulate a player leaving Shard Zero and moving deep into an instance (`ShardA`).
*   This move must trigger the *Outbox Relay* pattern simulation: The final state update for that move must be logged as PENDING in an outbox table representation, ensuring durability even if the system crashes.

---
**COMMIT INSTRUCTIONS:** Continue to follow the TDD cycle, committing after each completed task and updating this README.md document.