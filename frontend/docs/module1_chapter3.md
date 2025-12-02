# ROS 2 Communication: Deep Dive into Topics

## Learning Objectives

By the end of this chapter, you will be able to:
*   Gain a deeper understanding of how ROS 2 Topics facilitate asynchronous message passing.
*   Define and use custom message types for specific application needs.
*   Implement advanced publisher and subscriber nodes, leveraging Quality of Service (QoS) policies.
*   Utilize ROS 2 command-line tools to monitor and interact with active topics.

## How Topics Work: Beyond the Basics

In Chapter 1, we introduced Topics as named buses for asynchronous communication. At its core, ROS 2 communication relies on DDS (Data Distribution Service), an open standard for real-time systems. DDS handles the underlying network plumbing, enabling nodes to discover each other and exchange data efficiently, even across different machines.

### Quality of Service (QoS) Policies

QoS settings allow you to configure the behavior of your publishers and subscribers, influencing factors like reliability, latency, and message durability. Key QoS policies include:

*   **Reliability:**
    *   `BEST_EFFORT`: Messages may be lost (e.g., UDP). Good for high-frequency sensor data where missing a few readings is acceptable.
    *   `RELIABLE`: Guarantees delivery of all messages (e.g., TCP-like). Important for commands or critical data.
*   **Durability:**
    *   `VOLATILE`: New subscribers only receive messages published after they connect.
    *   `TRANSIENT_LOCAL`: The publisher will retain some number of messages for late-joining subscribers.
*   **History:**
    *   `KEEP_LAST`: Store only the last `N` messages.
    *   `KEEP_ALL`: Store all messages (up to a resource limit).
*   **Depth:** Used with `KEEP_LAST`, specifies how many messages to store.

Applying QoS is crucial for fine-tuning communication to your application's requirements.

## Defining Custom Messages

While `std_msgs` provides basic data types, real-world robotics often requires custom message structures. You define custom messages using `.msg` files.

1.  **Create a message definition file:**
    Inside your package (e.g., `my_ros2_package`), create a directory `msg` and a file, for example, `ComplexData.msg`:

    ```
    # my_ros2_package/msg/ComplexData.msg
    std_msgs/Header header
    uint32 id
    string name
    geometry_msgs/Point position
    float32[] data_array
    ```
    This message contains a header, an ID, a name, a 3D point, and an array of floats. Note that you can embed other message types.

2.  **Update `package.xml`:**
    Add these build and run dependencies:
    ```xml
    <!-- package.xml -->
    <build_depend>rosidl_default_generators</build_depend>
    <exec_depend>rosidl_default_runtime</exec_depend>
    <member_of_group>rosidl_interface_packages</member_of_group>
    ```

3.  **Update `CMakeLists.txt` (for `ament_cmake` packages) or `setup.py` (for `ament_python` packages):**

    **For Python packages (in `setup.py`):** You mainly need the `rosidl_default_generators` build dependency.

    **For C++ packages (in `CMakeLists.txt`):**
    ```cmake
    # CMakeLists.txt
    find_package(rosidl_default_generators REQUIRED)
    find_package(geometry_msgs REQUIRED) # If you use embedded messages like Point

    rosidl_generate_interfaces(${PROJECT_NAME}
      "msg/ComplexData.msg"
    )
    ament_export_dependencies(rosidl_default_runtime geometry_msgs)
    ```

4.  **Build your package:**
    ```bash
    colcon build --packages-select my_ros2_package
    ```
    After building, ROS 2 will generate Python and C++ source files for your custom message, which you can then import and use in your nodes.

## Advanced Publisher and Subscriber Patterns with QoS

Let's modify our publisher and subscriber to use QoS settings and our custom message.

First, ensure your `ComplexData.msg` is defined and built as described above.

**Publisher (`complex_publisher.py`):**

```python
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy, DurabilityPolicy
from my_ros2_package.msg import ComplexData # Import your custom message
from std_msgs.msg import Header
from geometry_msgs.msg import Point

class ComplexPublisher(Node):

    def __init__(self):
        super().__init__('complex_publisher')
        qos_profile = QoSProfile(
            reliability=ReliabilityPolicy.RELIABLE,
            history=HistoryPolicy.KEEP_LAST,
            depth=5, # Keep last 5 messages
            durability=DurabilityPolicy.TRANSIENT_LOCAL # Retain messages for late joiners
        )
        self.publisher_ = self.create_publisher(ComplexData, 'complex_topic', qos_profile)
        timer_period = 1.0  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.counter = 0

    def timer_callback(self):
        msg = ComplexData()
        msg.header = Header()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = 'base_link'
        msg.id = self.counter
        msg.name = f'SensorData_{self.counter}'
        msg.position = Point(x=float(self.counter), y=2.0, z=3.0)
        msg.data_array = [float(self.counter * 10), float(self.counter * 100)]

        self.publisher_.publish(msg)
        self.get_logger().info(f'Publishing ComplexData ID: {msg.id}')
        self.counter += 1

def main(args=None):
    rclpy.init(args=args)
    complex_publisher = ComplexPublisher()
    rclpy.spin(complex_publisher)
    complex_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

**Subscriber (`complex_subscriber.py`):**

```python
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy, DurabilityPolicy
from my_ros2_package.msg import ComplexData # Import your custom message

class ComplexSubscriber(Node):

    def __init__(self):
        super().__init__('complex_subscriber')
        qos_profile = QoSProfile(
            reliability=ReliabilityPolicy.RELIABLE,
            history=HistoryPolicy.KEEP_LAST,
            depth=5,
            durability=DurabilityPolicy.TRANSIENT_LOCAL
        )
        self.subscription = self.create_subscription(
            ComplexData,
            'complex_topic',
            self.listener_callback,
            qos_profile)
        self.subscription  # prevent unused variable warning

    def listener_callback(self, msg):
        self.get_logger().info(f'Received ComplexData:'
                               f'\n  ID: {msg.id}'
                               f'\n  Name: {msg.name}'
                               f'\n  Position: ({msg.position.x}, {msg.position.y}, {msg.position.z})'
                               f'\n  Data Array: {msg.data_array}')

def main(args=None):
    rclpy.init(args=args)
    complex_subscriber = ComplexSubscriber()
    rclpy.spin(complex_subscriber)
    complex_subscriber.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

Don't forget to update your `setup.py` entry points for these new scripts and rebuild your package.

## ROS 2 CLI Tools for Topics

ROS 2 provides powerful command-line tools to inspect and interact with topics.

*   **`ros2 topic list`**: Lists all active topics in the ROS 2 graph.
    ```bash
    ros2 topic list
    # Expected output:
    # /complex_topic
    # /parameter_events
    # /rosout
    ```
    Use `-t` or `--show-type` to also display message types:
    ```bash
    ros2 topic list -t
    # Expected output:
    # /complex_topic [my_ros2_package/msg/ComplexData]
    # ...
    ```

*   **`ros2 topic info <topic_name>`**: Shows information about a specific topic, including its type, publishers, and subscribers.
    ```bash
    ros2 topic info /complex_topic
    # Expected output (approx):
    # Type: my_ros2_package/msg/ComplexData
    # Publishers: 1
    #   Node name: complex_publisher
    #   Node namespace: /
    # Subscribers: 1
    #   Node name: complex_subscriber
    #   Node namespace: /
    ```

*   **`ros2 topic echo <topic_name>`**: Displays the messages being published on a topic in real-time. This is invaluable for debugging and monitoring data flow.
    ```bash
    ros2 topic echo /complex_topic
    # Expected output:
    # header:
    #   stamp:
    #     sec: 1678886400
    #     nanosec: 0
    #   frame_id: base_link
    # id: 0
    # name: SensorData_0
    # position:
    #   x: 0.0
    #   y: 2.0
    #   z: 3.0
    # data_array:
    # - 0.0
    # - 0.0
    # ---
    # ...
    ```

*   **`ros2 topic pub <topic_name> <msg_type> <values>`**: Publishes data to a topic from the command line. Useful for testing or manually injecting data. You need to provide the message type and values in YAML format.
    ```bash
    ros2 topic pub /complex_topic my_ros2_package/msg/ComplexData "{header: {stamp: {sec: 0, nanosec: 0}, frame_id: 'manual'}, id: 99, name: 'ManualData', position: {x: 10.0, y: 20.0, z: 30.0}, data_array: [1.1, 2.2]}" --once
    ```
    The `--once` flag publishes the message once and exits. You can omit it to publish continuously at a default rate.

## Interactive Quiz

<details>
  <summary>Which QoS policy would you use to ensure all messages are delivered, even if it means retransmissions?</summary>
  <p><b>Answer:</b> Reliable</p>
</details>

<details>
  <summary>What file extension is used to define custom message types in ROS 2?</summary>
  <p><b>Answer:</b> `.msg`</p>
</details>

<details>
  <summary>True or False: `ros2 topic echo` can be used to publish messages to a topic.</summary>
  <p><b>Answer:</b> False. `ros2 topic echo` is for *displaying* messages; `ros2 topic pub` is for *publishing* messages.</p>
</details>

## Further Reading

*   [ROS 2 Tutorials: Custom Interfaces](https://docs.ros.org/en/humble/Tutorials/Beginner-CLI-Tools/Custom-ROS2-Interfaces.html)
*   [ROS 2 Tutorials: Writing a Publisher and Subscriber (Python)](https://docs.ros.org/en/humble/Tutorials/Beginner-Client-Libraries/Writing-A-Simple-Py-Publisher-And-Subscriber.html)
*   [ROS 2 Documentation: Quality of Service Policies](https://docs.ros.org/en/humble/Concepts/About-Quality-Of-Service-Settings.html)
*   [ROS 2 CLI Tools: Topics](https://docs.ros.org/en/humble/Tutorials/Beginner-CLI-Tools/Using-ROS2-Topics.html)