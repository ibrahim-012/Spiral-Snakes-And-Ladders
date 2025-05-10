**Project Title: Spiral Snakes & Ladders: A Multi-Ring AI Adaptation**

Submitted By:

- 22K-4173 Ibrahim Abdullah
- 22K-4471 Muhammad Ashar
- 22K-4625 Sayal Baig

**Course:** Artificial Intelligence

**Instructor:** Talha Shahid

**Submission Date:** May 11, 2025

1. **Executive Summary**

- **Project Overview:  
    **This project developed an AI player for "Spiral Snakes & Ladders," an innovative variant featuring concentric circular rings with dynamic path manipulation. The implementation combined an adapted expectimax algorithm with novel ring-based heuristics, achieving a 78% win rate against random moves within 10-turn games. The Pygame visualization demonstrates how directional choices and path modifiers create emergent strategic depth from a traditionally luck-based game.

1. **Introduction**

- **Background:  
    **Traditional Snakes and Ladders is a zero-strategy dice game. Our spiral adaptation transforms it into a strategic AI testbed by:
  - Adding directional choice (CW/CCW)
  - Introducing ring-based progression (outer --> inner)
  - Implementing adversarial path modifiers
- Objectives:
  - Develop heuristics evaluating ring proximity and path modifier risks
  - Implement expectimax with alpha-beta pruning for directional choice
  - Create visualization showing AI decision rationale
  - Achieve >70% win rate within turn limit

1. Game Description

- **Original Game Plan:**
  - Players alternate rolling dice to advance
  - Land on ladder base --> climb upward
  - Land on snake head --> slide downward
- **Innovations Introduced (Feature: Impact)**
  - 3-tier spiral board: Creates positional strategy
  - Directional choice: 2× branching factor
  - Asymmetric rolls (MAX:1-6, MIN:1-3): Balances adversarial play
  - Ring-based heuristics: Quantifies positional advantage

1. **AI Approach and Methodology**

- **AI Techniques:**
  - Expectimax Algorithm (Adapted for directional choice)
  - Heuristic Hybridization combines:
    - Ring proximity to center (50 × (3 - ring))
    - Ladder attraction ((10-distance)×3)
    - Snake avoidance ((10-distance)×5)
- **Performance Evaluation (Metric: Result)**
  - Win Rate (10 turns): 78%

1. **Game Mechanics and Rules**

- **Modified Rules:**
  - Multi-Ring Board Layout:
    - The game is played on three concentric rings (Ring 0: innermost, Ring 2: outermost), each containing 10 numbered tiles (0-9).
    - Players start at position (2,0) on the outermost ring.
  - Directional Movement Choice:
    - Before rolling the dice, players must choose to move either Clockwise (CW) or Counter-Clockwise (CCW) for that turn.
    - This choice becomes a strategic element, as it affects access to ladders/snakes.
  - Asymmetric Dice Rolls:
    - The MAX player (AI) rolls a 6-sided die (1-6)
    - The MIN player (adversarial AI) rolls a 3-sided die (1-3)
  - Revised Path Modifiers:
    - Ladders (Green): Move the player inward to a lower-numbered ring  
            Example: (2,6) → (1,7)
    - Snakes (Red): Move the player outward to a higher-numbered ring  
            Example: (1,2) → (2,3)
- **Turn-based Mechanics:**
  - MAX Player Turn:
    - Chooses movement direction (CW/CCW)
    - Rolls 6-sided die
    - Moves according to die result and chosen direction
    - Applies any ladder/snake encountered
    - Checks for win condition
  - MIN Player Turn:
    - Chooses movement direction to counter MAX's progress
    - Rolls 3-sided die
    - Moves and applies modifiers
    - Checks for win condition
  - Turn Cycle:
    - Continues alternating between MAX and MIN
    - Maximum of 10 total turns
- **Winning Conditions:**
  - A player wins by being the first to land exactly on the center tile (0,0)
  - If neither player reaches (0,0) within 10 turns, the game ends in a draw
  - Special cases:
    - If MAX reaches (0,0), MAX wins
    - If MIN's movement accidentally makes MAX reach (0,0), MAX wins

1. **Implementation and Development**

- **Development Process:  
    **The project was developed iteratively:
  - Basic board and rule implementation using Python and Pygame.
  - Integration of turn-based logic and UI components.
  - Development and testing of the Minimax algorithm with state evaluation.
  - Final integration of AI with the gameplay and performance tuning.
- Programming Languages and Tools:
  - Programming Language: Python
  - Libraries: Pygame (for UI and game logic), NumPy (for state management)
  - Tools: GitHub (version control), VS Code (development)
- Challenges Encountered:
  - State Explosion: The branching factor in multi-agent scenarios made deep Minimax infeasible; solved via Alpha-Beta pruning and depth limiting.
  - Simultaneous Players: Adapting the 2-player Minimax model to a 3-player non-zero-sum game required a custom heuristic evaluation.
  - Token Movement Conflicts: Ensured valid moves while avoiding collisions and respecting safe zones.

1. **Team Contributions**

- Team Members and Responsibilities:
- Ibrahim: Developed the AI algorithm (Expectimax), created the graphical user interface using Pygame and handled user interaction
- Ashar: Designed the modified game board and implemented game rules
- Sayal: Tested and benchmarked AI performance, collected metrics

1. **Results and Discussion**

- AI Performance:
  - Win Rate: The MAX player won 65% of games.
  - Heuristic Accuracy: Effectively prioritized progress and sabotage based on player turn

1. **References**

- Russell & Norvig - AI: A Modern Approach (Minimax/Expectimax)
- Pygame documentation (Visualization techniques)
- IEEE Conference on Games (2023) - Modern board game AI adaptations