''' Code from ROS2 Docs
Modifications by Briana Bouchard

This code creates a publisher node and publishes a string to a topic with a counter every 0.5 seconds
'''

import rclpy # imports rclpy client library 
from rclpy.node import Node # imports Node class of rclpy library

from std_msgs.msg import String # imports ROS2 built-in string message type
from geometry_msgs.msg import Twist,Vector3
from rclpy.qos import qos_profile_sensor_data


# Creates SimplePublisher class which is a subclass of Node 
class SimplePublisher(Node):

    # Defines class constructor
    def __init__(self):
        self.x = 0

        # Initializes and gives Node the name simple_publisher and inherits the Node class's attributes by using 'super()'
        super().__init__('simple_publisher')

        # Creates a publisher based on the message type "String" that has been imported from the std_msgs module above
        #* Works if you actaully just put cmd_vel but isnt sending to to the subscriber tho
        self.publisher_ = self.create_publisher(Twist, '/cmd_vel', 10)

        # Set delay in seconds
        timer_period = 0.5  

        # Creates a timer that triggers a callback function after the set timer_period
        self.timer = self.create_timer(timer_period, self.timer_callback)

        # Sets initial counter to zero
        self.i = 0

    def timer_callback(self):
        # Assigns message type "String" that has been imported from the std_msgs module above
        self.msg = Twist()
        
        # Publishes `msg` to topic 
        self.x = self.x +1

        self.msg.linear.x = 2.0
        self.msg.linear.y = 2.0
        self.msg.linear.z = 2.0
 
        self.msg.angular.z = 4.0
        self.publisher_.publish(self.msg) 
        self.get_logger().info('Publishing: %s' % self.msg.linear.x) 










def main(args=None):
    # Initializes ROS2 communication and allows Nodes to be created
    rclpy.init(args=args)

    # Creates the SimplePublisher Node
    simple_publisher = SimplePublisher()


    try:
        # Spins the Node to activate the callbacks
        rclpy.spin(simple_publisher)

        
        

    # Stops the code if CNTL-C is pressed on the keyboard    
    except KeyboardInterrupt:
        print('\nCaught Keyboard Interrupt')

        # Destroys the node that was created
        simple_publisher.destroy_node()

        # Shuts down rclpy 
        rclpy.shutdown()


if __name__ == '__main__':
    # Runs the main function
    main()