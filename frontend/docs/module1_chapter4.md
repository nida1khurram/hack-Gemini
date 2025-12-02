# ROS 2 Communication: Services and Actions

## Learning Objectives

By the end of this chapter, you will be able to:
*   Differentiate between ROS 2 Topics, Services, and Actions, and identify appropriate use cases for each.
*   Define custom service and action types using `.srv` and `.action` files.
*   Implement client and server nodes for both ROS 2 Services and Actions in Python.
*   Effectively use ROS 2 command-line tools to interact with Services and Actions.

## How Services Work

ROS 2 Services provide a synchronous request/response communication pattern. Unlike Topics, which are publish-subscribe, Services are used when a node (the client) needs to make a specific request to another node (the server) and wait for a single, definitive response. This is analogous to a function call in a distributed system.

### Defining Custom Services

Similar to custom messages, custom services are defined using `.srv` files. A service definition consists of a request part and a response part, separated by `---`.

1.  **Create a service definition file:**
    Inside your package (e.g., `my_ros2_package`), create a directory `srv` and a file, for example, `AddTwoInts.srv`:

    ```
    # my_ros2_package/srv/AddTwoInts.srv
    int64 a
    int64 b
    ---
    int64 sum
    ```
    This service takes two `int64` integers (`a` and `b`) as a request and returns their `sum` as an `int64` in the response.

2.  **Update `package.xml` and `CMakeLists.txt`:**
    The process is similar to custom messages. Ensure `rosidl_default_generators` and `rosidl_default_runtime` are correctly set up.
    In `CMakeLists.txt`:
    ```cmake
    # CMakeLists.txt
    rosidl_generate_interfaces(${PROJECT_NAME}
      "srv/AddTwoInts.srv"
    )
    ```

## Service Client and Server

Let's implement a service server that adds two integers and a client that calls this service.

**Service Server (`add_two_ints_server.py`):**

```python
import rclpy
from rclpy.node import Node
from my_ros2_package.srv import AddTwoInts # Import your custom service

class AddTwoIntsService(Node):

    def __init__(self):
        super().__init__('add_two_ints_server')
        self.srv = self.create_service(AddTwoInts, 'add_two_ints', self.add_two_ints_callback)
        self.get_logger().info('Add two ints service ready.')

    def add_two_ints_callback(self, request, response):
        response.sum = request.a + request.b
        self.get_logger().info(f'Incoming request: a={request.a} b={request.b}')
        self.get_logger().info(f'Sending response: {response.sum}')
        return response

def main(args=None):
    rclpy.init(args=args)
    add_two_ints_service = AddTwoIntsService()
    rclpy.spin(add_two_ints_service)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

**Service Client (`add_two_ints_client.py`):**

```python
import sys
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, QoSReliabilityPolicy, QoSHistoryPolicy
from my_ros2_package.srv import AddTwoInts # Import your custom service

class AddTwoIntsClient(Node):

    def __init__(self):
        super().__init__('add_two_ints_client')
        # QoS for client to ensure reliable communication
        qos_profile = QoSProfile(
            reliability=QoSReliabilityPolicy.RELIABLE,
            history=QoSHistoryPolicy.KEEP_LAST,
            depth=1
        )
        self.cli = self.create_client(AddTwoInts, 'add_two_ints', qos_profile=qos_profile)
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('service not available, waiting again...')
        self.req = AddTwoInts.Request()

    def send_request(self, a, b):
        self.req.a = a
        self.req.b = b
        self.future = self.cli.call_async(self.req)
        rclpy.spin_until_future_complete(self, self.future)
        return self.future.result()

def main(args=None):
    rclpy.init(args=args)
    add_two_ints_client = AddTwoIntsClient()
    response = add_two_ints_client.send_request(int(sys.argv[1]), int(sys.argv[2]))
    add_two_ints_client.get_logger().info(
        f'Result of add_two_ints: for {sys.argv[1]} + {sys.argv[2]} = {response.sum}')
    add_two_ints_client.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: ros2 run my_ros2_package add_two_ints_client <int> <int>')
        sys.exit(1)
    main()
```
Don't forget to update your `setup.py` entry points and rebuild your package.

## How Actions Work

ROS 2 Actions are designed for long-running tasks that provide periodic feedback and can be preempted. They are a higher-level abstraction built on top of topics and services. An Action involves three parts: a Goal, a Result, and Feedback.

*   **Goal:** What the client wants the server to achieve.
*   **Result:** The outcome of the goal (sent once the goal is completed).
*   **Feedback:** Intermediate updates on the progress toward the goal (sent periodically).

### Defining Custom Actions

Custom actions are defined using `.action` files. The file structure separates Goal, Result, and Feedback with `---`.

1.  **Create an action definition file:**
    Inside your package, create a directory `action` and a file, for example, `Fibonacci.action`:

    ```
    # my_ros2_package/action/Fibonacci.action
    int32 order
    ---
    int32[] sequence
    ---
    int32[] partial_sequence
    ```
    *   **Goal:** `order` (the number of Fibonacci terms to generate).
    *   **Result:** `sequence` (the final Fibonacci sequence).
    *   **Feedback:** `partial_sequence` (the sequence generated so far).

2.  **Update `package.xml` and `CMakeLists.txt`:**
    Similar to messages/services, ensure `rosidl_default_generators` and `rosidl_default_runtime` are correctly set up.
    In `CMakeLists.txt`:
    ```cmake
    # CMakeLists.txt
    rosidl_generate_interfaces(${PROJECT_NAME}
      "action/Fibonacci.action"
    )
    ```

## Action Client and Server

Let's implement an action server that calculates the Fibonacci sequence and an action client that requests this calculation.

**Action Server (`fibonacci_action_server.py`):**

```python
import time
import rclpy
from rclpy.node import Node
from rclpy.action import ActionServer
from my_ros2_package.action import Fibonacci # Import your custom action

class FibonacciActionServer(Node):

    def __init__(self):
        super().__init__('fibonacci_action_server')
        self._action_server = ActionServer(
            self,
            Fibonacci,
            'fibonacci',
            self.execute_callback)
        self.get_logger().info('Fibonacci action server ready.')

    def execute_callback(self, goal_handle):
        self.get_logger().info('Executing goal...')

        feedback_msg = Fibonacci.Feedback()
        feedback_msg.partial_sequence = [0, 1]

        # Publish feedback at a certain rate
        for i in range(1, goal_handle.request.order):
            if goal_handle.is_cancel_requested:
                goal_handle.canceled()
                self.get_logger().info('Goal canceled')
                return Fibonacci.Result()

            feedback_msg.partial_sequence.append(
                feedback_msg.partial_sequence[i] + feedback_msg.partial_sequence[i-1])
            self.get_logger().info(f'Feedback: {feedback_msg.partial_sequence}')
            goal_handle.publish_feedback(feedback_msg)
            time.sleep(1) # Simulate work

        goal_handle.succeed()

        result = Fibonacci.Result()
        result.sequence = feedback_msg.partial_sequence
        self.get_logger().info(f'Goal succeeded: {result.sequence}')
        return result

def main(args=None):
    rclpy.init(args=args)
    fibonacci_action_server = FibonacciActionServer()
    rclpy.spin(fibonacci_action_server)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

**Action Client (`fibonacci_action_client.py`):**

```python
import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node
from my_ros2_package.action import Fibonacci # Import your custom action

class FibonacciActionClient(Node):

    def __init__(self):
        super().__init__('fibonacci_action_client')
        self._action_client = ActionClient(self, Fibonacci, 'fibonacci')

    def send_goal(self, order):
        goal_msg = Fibonacci.Goal()
        goal_msg.order = order

        self._action_client.wait_for_server()

        self._send_goal_future = self._action_client.send_goal_async(
            goal_msg,
            feedback_callback=self.feedback_callback)

        self._send_goal_future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().info('Goal rejected :(')
            return

        self.get_logger().info('Goal accepted :)')

        self._get_result_future = goal_handle.get_result_async()
        self._get_result_future.add_done_callback(self.get_result_callback)

    def get_result_callback(self, future):
        result = future.result().result
        self.get_logger().info(f'Result: {result.sequence}')
        rclpy.shutdown()

    def feedback_callback(self, feedback_msg):
        self.get_logger().info(f'Received feedback: {feedback_msg.feedback.partial_sequence}')

def main(args=None):
    rclpy.init(args=args)
    action_client = FibonacciActionClient()
    action_client.send_goal(10) # Request Fibonacci sequence of order 10
    rclpy.spin(action_client)

if __name__ == '__main__':
    main()
```
Don't forget to update your `setup.py` entry points and rebuild your package.

## ROS 2 CLI Tools for Services and Actions

### Services CLI Tools

*   **`ros2 service list`**: Lists all active services.
    ```bash
    ros2 service list
    # Expected output:
    # /add_two_ints
    # /rosout/get_type_description
    # ...
    ```
    Use `-t` to show service types:
    ```bash
    ros2 service list -t
    # Expected output:
    # /add_two_ints [my_ros2_package/srv/AddTwoInts]
    # ...
    ```

*   **`ros2 service type <service_name>`**: Shows the type of a specific service.
    ```bash
    ros2 service type /add_two_ints
    # Expected output:
    # my_ros2_package/srv/AddTwoInts
    ```

*   **`ros2 service call <service_name> <service_type> <request_values>`**: Calls a service from the command line.
    ```bash
    ros2 service call /add_two_ints my_ros2_package/srv/AddTwoInts "{a: 5, b: 3}"
    # Expected output:
    # response:
    #   sum: 8
    ```

### Actions CLI Tools

*   **`ros2 action list`**: Lists all active actions.
    ```bash
    ros2 action list
    # Expected output:
    # /fibonacci
    # ...
    ```
    Use `-t` to show action types:
    ```bash
    ros2 action list -t
    # Expected output:
    # /fibonacci [my_ros2_package/action/Fibonacci]
    # ...
    ```

*   **`ros2 action info <action_name>`**: Shows information about a specific action, including its type, servers, and clients.
    ```bash
    ros2 action info /fibonacci
    # Expected output:
    # Action: /fibonacci
    # Goal STATUS:
    #   my_ros2_package/action/Fibonacci
    # Goal CLIENTS: 1
    #   Node name: fibonacci_action_client
    # Goal SERVERS: 1
    #   Node name: fibonacci_action_server
    # ...
    ```

*   **`ros2 action send_goal <action_name> <action_type> <goal_values>`**: Sends a goal to an action server from the command line.
    ```bash
    ros2 action send_goal /fibonacci my_ros2_package/action/Fibonacci "{order: 5}"
    # Expected output (includes feedback and final result):
    # Goal accepted with ID: <some_uuid>
    # ...
    # Feedback: partial_sequence: [0, 1, 1, 2]
    # ...
    # Result: sequence: [0, 1, 1, 2, 3]
    ```

## Interactive Quiz

<details>
  <summary>What separates the request and response parts in a `.srv` file?</summary>
  <p><b>Answer:</b> `---` (three hyphens)</p>
</details>

<details>
  <summary>Which component is unique to ROS 2 Actions compared to Services and provides updates on progress?</summary>
  <p><b>Answer:</b> Feedback</p>
</details>

<details>
  <summary>True or False: A ROS 2 Service call is asynchronous, meaning the client does not wait for the server's response.</summary>
  <p><b>Answer:</b> False. Services are synchronous; the client waits for the response.</p>
</details>

## Further Reading

*   [ROS 2 Tutorials: Writing a Simple Service and Client (Python)](https://docs.ros.org/en/humble/Tutorials/Beginner-Client-Libraries/Writing-A-Simple-Py-Service-And-Client.html)
*   [ROS 2 Tutorials: Writing a Simple Action Client and Server (Python)](https://docs.ros.org/en/humble/Tutorials/Beginner-Client-Libraries/Writing-A-Simple-Py-Action-Client-And-Server.html)
*   [ROS 2 CLI Tools: Services](https://docs.ros.org/en/humble/Tutorials/Beginner-CLI-Tools/Using-ROS2-Services.html)
*   [ROS 2 CLI Tools: Actions](https://docs.ros.org/en/humble/Tutorials/Beginner-CLI-Tools/Using-ROS2-Actions.html)