import PythonRunner from '@site/src/components/PythonRunner';

# Introduction to ROS 2

## Learning Objectives

By the end of this chapter, you will be able to:
*   Understand the fundamental purpose and architecture of ROS 2.
*   Identify and describe the key ROS 2 concepts: Nodes, Topics, Services, and Actions.
*   Create a simple ROS 2 publisher node in Python.
*   Create a simple ROS 2 subscriber node in Python.

## What is ROS 2?

ROS 2 (Robot Operating System 2) is an open-source, flexible framework for writing robot software. It is a collection of tools, libraries, and conventions that aim to simplify the task of creating complex and robust robot behaviors across a wide variety of robotic platforms. Building on the successes of its predecessor, ROS 1, ROS 2 was re-architected to address limitations in areas such as real-time control, multi-robot systems, and embedded systems, leveraging modern communication standards like DDS (Data Distribution Service).

## Key Concepts

### Nodes

A **Node** is an executable process that performs computation. In ROS 2, nodes are typically organized into packages, and each node has a specific role, such as controlling a motor, reading sensor data, or performing path planning. Nodes communicate with each other using ROS 2 communication mechanisms.

### Topics

**Topics** are named buses over which nodes exchange messages. A node can *publish* messages to a topic, and other nodes can *subscribe* to that topic to receive the messages. Topics are a fundamental asynchronous communication pattern in ROS 2, ideal for streaming data like sensor readings or robot odometry.

### Services

**Services** are a synchronous communication mechanism in ROS 2, enabling nodes to send a *request* and receive a *response*. Unlike topics, which are one-way streams, services are typically used for RPC (Remote Procedure Call) patterns where a client needs to trigger a specific operation on a server node and await its completion.

### Actions

**Actions** are a higher-level communication mechanism designed for long-running, goal-oriented tasks. They are similar to services but provide feedback on the goal's progress and allow for preemption (canceling a goal before it completes). Actions are composed of a goal, feedback, and result, making them suitable for tasks like navigating to a target or picking up an object.

## Code Example: Creating a Simple Publisher

This example demonstrates how to create a simple ROS 2 publisher node in Python that publishes "Hello, ROS 2!" messages to a topic.

First, create a new ROS 2 package (if you haven't already):
```bash
ros2 pkg create --build-type ament_python my_ros2_package --dependencies rclpy
```

Then, create a Python file `my_publisher.py` inside the `my_ros2_package/my_ros2_package` directory:

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class MinimalPublisher(Node):

    def __init__(self):
        super().__init__('minimal_publisher')
        self.publisher_ = self.create_publisher(String, 'topic', 10)
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0

    def timer_callback(self):
        msg = String()
        msg.data = f'Hello, ROS 2! {self.i}'
        self.publisher_.publish(msg)
        self.get_logger().info(f'Publishing: "{msg.data}"')
        self.i += 1

def main(args=None):
    rclpy.init(args=args)

    minimal_publisher = MinimalPublisher()

    rclpy.spin(minimal_publisher)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

Don't forget to add an entry point in `setup.py` within your package folder:

```python
# setup.py (partial view)
entry_points={
    'console_scripts': [
        'my_publisher = my_ros2_package.my_publisher:main',
    ],
},
```

Build your package:
```bash
cd ~/ros2_ws # or your workspace root
colcon build --packages-select my_ros2_package
source install/setup.bash # source your workspace
```

Run the publisher:
```bash
ros2 run my_ros2_package my_publisher
```

### Try it Yourself!
<PythonRunner code={`print("Hello from Pyodide!")
a = 10
b = 20
print(f"The sum of a and b is: {a + b}")`} />

## Code Example: Creating a Simple Subscriber

This example demonstrates how to create a simple ROS 2 subscriber node in Python that listens for messages on the same topic.

Create a Python file `my_subscriber.py` inside the `my_ros2_package/my_ros2_package` directory:

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class MinimalSubscriber(Node):

    def __init__(self):
        super().__init__('minimal_subscriber')
        self.subscription = self.create_subscription(
            String,
            'topic',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning

    def listener_callback(self, msg):
        self.get_logger().info(f'I heard: "{msg.data}"')

def main(args=None):
    rclpy.init(args=args)

    minimal_subscriber = MinimalSubscriber()

    rclpy.spin(minimal_subscriber)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_subscriber.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

Add another entry point in `setup.py`:

```python
# setup.py (partial view)
entry_points={
    'console_scripts': [
        'my_publisher = my_ros2_package.my_publisher:main',
        'my_subscriber = my_ros2_package.my_subscriber:main', # New entry
    ],
},
```

Build your package again:
```bash
cd ~/ros2_ws # or your workspace root
colcon build --packages-select my_ros2_package
source install/setup.bash # source your workspace
```

Run the subscriber (in a new terminal, while the publisher is running):
```bash
ros2 run my_ros2_package my_subscriber
```

## Interactive Quiz

<details>
  <summary>What is the primary communication mechanism for streaming continuous data in ROS 2?</summary>
  <p><b>Answer:</b> Topics</p>
</details>

<details>
  <summary>Which ROS 2 concept is best suited for long-running, goal-oriented tasks with feedback and preemption capabilities?</summary>
  <p><b>Answer:</b> Actions</p>
</details>

<details>
  <summary>True or False: A ROS 2 Service allows multiple nodes to publish data simultaneously without waiting for a response.</summary>
  <p><b>Answer:</b> False (This describes Topics; Services are for synchronous request/response.)</p>
</details>

## Further Reading

*   [ROS 2 Documentation](https://docs.ros.org/en/humble/index.html)
*   [Understanding ROS 2 Nodes](https://docs.ros.org/en/humble/Concepts/Basic/Nodes/Understanding-Nodes.html)
*   [Understanding ROS 2 Topics](https://docs.ros.org/en/humble/Concepts/Basic/Topics/Understanding-Topics.html)
*   [Understanding ROS 2 Services](https://docs.ros.org/en/humble/Concepts/Basic/Services/Understanding-Services.html)
*   [Understanding ROS 2 Actions](https://docs.ros.org/en/humble/Concepts/Basic/Actions/Understanding-Actions.html)