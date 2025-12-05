# Capstone Project: Build a Simulated Humanoid Robot Controller

This capstone project aims to guide you through building a basic controller for a humanoid robot in a physics simulation environment. You will explore concepts of kinematics, balance, and elementary control.

## 4-Part Project Structure

The project can be broken down into four logical phases:

### Part 1: Setup and Environment Initialization
*   **Goal:** Get a humanoid robot model loaded into a physics simulator and establish basic interaction.
*   **Key Tasks:**
    *   Choose and set up a physics simulator.
    *   Load a humanoid robot model (URDF file).
    *   Initialize the simulation environment (gravity, ground plane, time steps).
    *   Establish communication with the robot's joints and sensors.

### Part 2: Kinematics and Basic Movement
*   **Goal:** Understand the robot's geometry and enable direct control of its joint positions.
*   **Key Tasks:**
    *   Identify and map robot joints to control inputs.
    *   Implement forward kinematics to calculate end-effector (hands, feet) positions.
    *   Develop a method to set desired joint angles and observe the robot's posture.
    *   Implement inverse kinematics for simple pose targets (optional, advanced).

### Part 3: Balance and Locomotion Control
*   **Goal:** Enable the robot to maintain balance and perform rudimentary walking movements.
*   **Key Tasks:**
    *   Read sensor data (e.g., IMU for orientation, joint encoders).
    *   Implement a basic balance controller (e.g., maintaining Center of Mass over support polygon, simplified ZMP control).
    *   Generate simple gait patterns (pre-defined joint trajectories for walking).
    *   Apply control torques/forces to joints to execute gait and maintain balance.

### Part 4: Perception Integration and Task Execution (Optional / Advanced)
*   **Goal:** Incorporate sensor data for environment interaction and more adaptive behaviors.
*   **Key Tasks:**
    *   Integrate simulated camera or depth sensor data (e.g., object detection).
    *   Develop simple reactive behaviors based on perception (e.g., obstacle avoidance).
    *   Implement a high-level task that utilizes the robot's movement and balance capabilities (e.g., stand up from a fall, reach for an object).

---

## PyBullet vs. MuJoCo: Which is Easier for Students?

For students and beginners, **PyBullet** is generally much easier to get started with than MuJoCo.

*   **PyBullet (Recommended):**
    *   **Pros:** Easy installation (`pip install pybullet`), Python-native API, excellent documentation and examples, active community support, free to use. Handles URDF models well. Strong focus on robotics and reinforcement learning.
    *   **Cons:** Might be slightly less physically accurate or computationally efficient than MuJoCo for extremely high-fidelity contact simulations, but sufficient for most educational purposes.
*   **MuJoCo:**
    *   **Pros:** Highly optimized for control, superior contact dynamics, very fast simulations, now free to use (acquired by Google DeepMind).
    *   **Cons:** Steeper learning curve, XML-based model format can be complex, API is more low-level, setup historically more involved (though improving).

**Recommendation for students: Start with PyBullet.** Its Pythonic interface and wealth of examples make it ideal for learning robotics simulation without getting bogged down by complex setup or low-level details.

---

## File Structure with Key Files

A typical project structure for a PyBullet humanoid controller might look like this:

```
humanoid_controller/
├── main.py                     # Main script to run the simulation
├── robot_model/                # Directory for URDF and mesh files
│   └── humanoid.urdf           # Your humanoid robot's Universal Robot Description Format file
│   └── meshes/
│       └── ...                 # Mesh files (e.g., .stl, .obj) referenced by the URDF
├── controllers/
│   ├── balance_controller.py   # Python module for balance algorithms
│   └── gait_generator.py       # Python module for generating walking patterns
├── utils/
│   └── robot_utils.py          # Helper functions (e.g., kinematics calculations, sensor parsing)
├── config.py                   # Configuration parameters (e.g., joint limits, link lengths)
└── requirements.txt            # Python dependencies (pybullet, numpy, etc.)
```

---

## Starter Code: PyBullet Humanoid Simulation

This starter code will set up a PyBullet simulation, load a humanoid model, and allow you to interact with its joints.

```python
# humanoid_controller/main.py

import pybullet as p
import pybullet_data
import time
import numpy as np

# --- Configuration ---
GUI = True # Set to False for faster headless simulation
TIME_STEP = 1.0 / 240.0 # Simulation time step
GRAVITY = -9.81
ROBOT_START_POS = [0, 0, 1.0] # Initial position (x, y, z)
ROBOT_START_ORI = p.getQuaternionFromEuler([0, 0, 0]) # Initial orientation (roll, pitch, yaw)
DEFAULT_LINK_COLOR = [0.1, 0.1, 0.1, 1] # Dark gray, opaque

# --- Simulation Setup ---
def setup_simulation():
    if GUI:
        physicsClient = p.connect(p.GUI)
    else:
        physicsClient = p.connect(p.DIRECT)

    p.setAdditionalSearchPath(pybullet_data.getDataPath())
    p.setGravity(0, 0, GRAVITY)
    p.setTimeStep(TIME_STEP)

    # Load ground plane
    p.loadURDF("plane.urdf")

    # Load humanoid robot
    # Replace "your_humanoid.urdf" with the path to your robot's URDF file
    # Example: you might find humanoids in pybullet_data or external sources
    robotId = p.loadURDF("humanoid/humanoid.urdf", ROBOT_START_POS, ROBOT_START_ORI, useFixedBase=False)

    # Optionally set default color for links if not defined in URDF
    for joint_index in range(p.getNumJoints(robotId)):
        p.changeVisualShape(robotId, joint_index, rgbaColor=DEFAULT_LINK_COLOR)

    # Get joint information
    joint_names = []
    joint_indices = []
    control_mode = p.POSITION_CONTROL # or p.VELOCITY_CONTROL, p.TORQUE_CONTROL

    print("--- Robot Joint Information ---")
    for i in range(p.getNumJoints(robotId)):
        joint_info = p.getJointInfo(robotId, i)
        joint_id = joint_info[0]
        joint_name = joint_info[1].decode("utf-8")
        joint_type = joint_info[2]
        joint_lower_limit = joint_info[8]
        joint_upper_limit = joint_info[9]

        if joint_type == p.JOINT_REVOLUTE or joint_type == p.JOINT_PRISMATIC:
            joint_names.append(joint_name)
            joint_indices.append(joint_id)
            p.setJointMotorControl2(robotId, joint_id, p.POSITION_CONTROL, targetPosition=0, force=0) # Disable motors initially

        print(f"ID: {joint_id}, Name: {joint_name}, Type: {joint_type}, Limits: ({joint_lower_limit:.2f}, {joint_upper_limit:.2f})")

    print("-------------------------------")
    return physicsClient, robotId, joint_indices, joint_names

# --- Joint Control Example ---
def control_joints_interactive(robotId, joint_indices):
    """
    Sets up sliders in the GUI to control a few selected joints.
    """
    print("Setting up joint control sliders...")
    controlled_joints = {}
    slider_scales = {}

    # Example: Select a few joints to control (adjust as per your robot's URDF)
    # You'll need to inspect your URDF or the output from setup_simulation to pick relevant joints
    # For a general humanoid, often hip/knee/ankle pitch, shoulder/elbow pitch/roll
    
    # Try to find some common humanoid joints
    potential_joints_to_control = [
        "left_hip_pitch", "left_knee_pitch", "left_ankle_pitch",
        "right_hip_pitch", "right_knee_pitch", "right_ankle_pitch",
        "left_shoulder_pitch", "left_elbow_pitch",
        "right_shoulder_pitch", "right_elbow_pitch",
        "neck_pitch", "neck_yaw"
    ]

    for joint_id in joint_indices:
        joint_info = p.getJointInfo(robotId, joint_id)
        joint_name = joint_info[1].decode("utf-8")
        joint_lower_limit = joint_info[8]
        joint_upper_limit = joint_info[9]

        if joint_name in potential_joints_to_control:
            # Create a slider for each selected joint
            initial_pos = 0.0 # Start at 0 or mid-range
            slider_id = p.addUserDebugParameter(
                joint_name, joint_lower_limit, joint_upper_limit, initial_pos
            )
            controlled_joints[joint_id] = slider_id
            # Scale slider range to control force, velocity, or position
            slider_scales[slider_id] = (joint_lower_limit, joint_upper_limit)

    print(f"Interactive control set for {len(controlled_joints)} joints.")
    return controlled_joints, slider_scales

def apply_joint_control(robotId, controlled_joints, slider_scales):
    """
    Reads slider values and applies them to the robot's joints.
    """
    for joint_id, slider_id in controlled_joints.items():
        joint_value = p.readUserDebugParameter(slider_id)
        # Apply the value using position control
        p.setJointMotorControl2(
            robotId,
            joint_id,
            p.POSITION_CONTROL,
            targetPosition=joint_value,
            force=500 # Apply a reasonable force to move the joint
        )

# --- Main Simulation Loop ---
def main():
    physicsClient, robotId, joint_indices, joint_names = setup_simulation()
    
    # Setup interactive control (sliders)
    controlled_joints, slider_scales = {}, {}
    if GUI:
        controlled_joints, slider_scales = control_joints_interactive(robotId, joint_indices)

    # Initial stable pose (e.g., slightly bent knees, arms down)
    # You'll need to adjust these values based on your robot's URDF and joint limits
    # Example: { "knee_pitch_joint": 0.5, "hip_pitch_joint": -0.5, ... }
    initial_pose = {} 
    for joint_id in joint_indices:
        joint_info = p.getJointInfo(robotId, joint_id)
        joint_name = joint_info[1].decode("utf-8")
        if "knee" in joint_name and "pitch" in joint_name:
            initial_pose[joint_id] = 0.5 # Bend knees slightly
        elif "hip" in joint_name and "pitch" in joint_name:
            initial_pose[joint_id] = -0.3 # Lean forward slightly
        else:
            initial_pose[joint_id] = 0.0 # Default to 0

    for joint_id, target_pos in initial_pose.items():
        p.setJointMotorControl2(robotId, joint_id, p.POSITION_CONTROL, targetPosition=target_pos, force=500)
    
    # Let robot settle into initial pose
    for _ in range(240): # Run for 1 second
        p.stepSimulation()
        if GUI:
            time.sleep(TIME_STEP)

    print("Starting main simulation loop...")
    try:
        while True:
            # Apply interactive controls if GUI is active
            if GUI:
                apply_joint_control(robotId, controlled_joints, slider_scales)

            # --- Control Logic would go here ---
            # This is where you'd implement:
            # - Reading joint states: p.getJointState(robotId, joint_id)
            # - Reading base state (position, orientation): p.getBasePositionAndOrientation(robotId)
            # - Reading IMU data (if simulated): p.getLinkState(robotId, imu_link_id, computeLinkVelocity=1)
            # - Your balance, gait generation, and kinematics algorithms
            # - Applying torques/positions/velocities: p.setJointMotorControl2(...)

            p.stepSimulation()
            if GUI:
                time.sleep(TIME_STEP)

    except KeyboardInterrupt:
        print("Simulation interrupted.")
    finally:
        p.disconnect()
        print("Simulation disconnected.")

if __name__ == "__main__":
    main()