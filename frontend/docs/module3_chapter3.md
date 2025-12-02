# Planning and Decision-Making

## Learning Objectives

By the end of this chapter, you will be able to:
*   Articulate the fundamental concepts and importance of planning in autonomous robotic systems.
*   Differentiate between various approaches to path and motion planning for robots.
*   Understand how AI techniques enable robots to make complex decisions, particularly in uncertain environments.
*   Explore methods for high-level task planning and effective execution monitoring in robotics.

## Introduction to Robotic Planning

Robotic planning is the process of computing a sequence of actions or motions that a robot needs to execute to achieve a specific goal. Unlike simple reactive behaviors, planning involves reasoning about the robot's state, the environment, and the effects of potential actions before they are performed. Planning is essential for robots to:
*   Navigate safely and efficiently.
*   Manipulate objects effectively.
*   Perform complex multi-step tasks.
*   Operate autonomously in dynamic and partially unknown environments.

Planning problems can range from finding a collision-free path for a mobile robot (path planning) to generating a precise, dynamically feasible trajectory for a robotic arm (motion planning), or even deciding a high-level sequence of actions to assemble a product (task planning).

## Path Planning

**Path planning** is concerned with finding a continuous, collision-free path for a robot from a starting configuration to a goal configuration. It typically assumes a static environment and ignores dynamic constraints like velocity or acceleration limits.

### Configuration Space (C-space)
To simplify collision checking, the robot is often mapped into its **configuration space (C-space)**, where the robot is represented as a point, and obstacles are "grown" proportionally. Path planning then becomes a search for a collision-free path for a point in C-space.

### Common Path Planning Algorithms:

1.  **Graph Search Algorithms:**
    *   **Dijkstra's Algorithm:** Finds the shortest path between nodes in a graph.
    *   **A* Search Algorithm:** An extension of Dijkstra's that uses a heuristic to guide its search, making it more efficient for goal-directed paths. It's widely used in robotics and game AI.

2.  **Sampling-Based Algorithms:**
    These algorithms build a roadmap of the C-space by randomly sampling configurations and connecting them. They are particularly effective for high-dimensional spaces or complex environments where grid-based methods become computationally intractable.
    *   **Rapidly-exploring Random Tree (RRT):** Explores the C-space by growing a tree from the start configuration, biasing exploration towards unexplored regions.
    *   **Probabilistic Roadmaps (PRM):** Constructs a roadmap by sampling random configurations (nodes) and connecting them if a collision-free path exists between them. Queries then use graph search on this roadmap.

## Motion Planning

**Motion planning** extends path planning by considering the robot's dynamics and kinematic constraints (e.g., velocity, acceleration, joint limits) to generate a feasible trajectory. A trajectory specifies not just the path, but also the timing of movements.

Key aspects of motion planning include:
*   **Trajectory Generation:** Converting a path into a time-parameterized sequence of joint positions, velocities, and accelerations.
*   **Collision Avoidance:** Ensuring the robot avoids collisions throughout its movement, not just at static points.
*   **Dynamic Constraints:** Respecting motor torque limits, maximum joint speeds, etc.
*   **Optimization:** Optimizing trajectories for smoothness, minimum time, minimum energy, or minimum jerk.

## Decision-Making under Uncertainty

Robots often operate in environments where information is incomplete or noisy. AI techniques are crucial for making robust decisions under such **uncertainty**.

### Markov Decision Processes (MDPs)
**Markov Decision Processes (MDPs)** provide a mathematical framework for modeling sequential decision-making in stochastic (probabilistic) environments. An MDP consists of:
*   **States:** The possible situations the robot can be in.
*   **Actions:** The choices the robot can make.
*   **Transitions:** Probabilities of moving from one state to another given an action.
*   **Rewards:** Values received for being in a state or performing an action.
*   **Policy:** A mapping from states to actions, specifying what the robot should do in each state.

Solving an MDP means finding an optimal policy that maximizes the robot's cumulative reward over time.

### Reinforcement Learning (RL)
**Reinforcement Learning (RL)** is a powerful AI paradigm where an agent learns an optimal policy through trial and error, interacting with an environment to maximize a reward signal. RL is particularly effective for problems that are difficult to model explicitly with traditional planning methods. While briefly mentioned in AI Introduction, RL directly addresses decision-making by learning optimal behaviors.

## Task Planning

**Task planning** (or high-level planning) deals with abstract goals and actions, often involving logical reasoning. It determines *what* needs to be done, leaving *how* it's done to lower-level path and motion planners.

### Hierarchical Planning
Many complex robotic systems use **hierarchical planning**, where high-level task planners break down abstract goals into sub-goals, which are then handled by geometric (path/motion) planners.

### Execution Monitoring and Re-planning
Robots need to **monitor** the execution of their plans and detect deviations (e.g., unexpected obstacles, failed actions). If a deviation occurs, the robot must be able to **re-plan** to achieve its goal. This involves perceiving the new state, updating its model of the world, and generating a new plan.

## Interactive Quiz

<details>
  <summary>Which planning algorithm uses a heuristic to guide its search for the shortest path in a graph?</summary>
  <ul>
    <li>a) Dijkstra's Algorithm</li>
    <li>b) RRT</li>
    <li>c) A* Search Algorithm</li>
    <li>d) PRM</li>
  </ul>
  <p><b>Answer:</b> c) A* Search Algorithm</p>
</details>

<details>
  <summary>What is the primary difference between path planning and motion planning?</summary>
  <p><b>Answer:</b> Path planning finds a collision-free path, while motion planning additionally considers dynamic constraints (like velocity and acceleration) to generate a time-parameterized trajectory.</p>
</details>

<details>
  <summary>True or False: Reinforcement Learning is a technique used to make decisions in deterministic (predictable) environments, not uncertain ones.</summary>
  <p><b>Answer:</b> False. Reinforcement Learning is particularly well-suited for learning optimal policies in stochastic (uncertain) environments through trial and error.</p>
</details>

## Further Reading

*   [Robotics Motion Planning (CMU)](https://www.cs.cmu.edu/~maxim/classes/robotplanning/)
*   [Sampling-Based Motion Planning (MIT OpenCourseWare)](https://ocw.mit.edu/courses/electrical-engineering-and-computer-science/6-832-underactuated-robotics-spring-2009/lecture-notes/MIT6_832F09_lec07.pdf)
*   [Planning and Decision-Making for Robotics - Georgia Tech](https://www.udacity.com/course/planning-for-robotics-cs373)
*   [Reinforcement Learning: An Introduction (Richard S. Sutton and Andrew G. Barto)](http://incompleteideas.net/book/the-book-2nd.html)