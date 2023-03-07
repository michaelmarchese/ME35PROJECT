''' Code from ROS2 Docs
Modifications by Briana Bouchard

This code creates a publisher node and publishes a string to a topic with a counter every 0.5 seconds
'''

import rclpy # imports rclpy client library 
from rclpy.node import Node # imports Node class of rclpy library

from std_msgs.msg import String # imports ROS2 built-in string message type
from geometry_msgs.msg import Twist
from rclpy.qos import qos_profile_sensor_data


# Creates SimplePublisher class which is a subclass of Node 


 

class SubScriberNodes(Node):

     def __init__(self):

        super().__init__('Subscriber_Node')
#! may need to add the qosprofile thing
        self.subscription = self.create_subscription(Twist,'/cmd_vel',self.listener_callback,10)
        self.subscription
    
     def listener_callback(self, msg):

        self.get_logger().info('Publishing: %s' % msg.linear.x) 






def main(args=None):
    # Initializes ROS2 communication and allows Nodes to be created
    rclpy.init(args=args)

    # Creates the SimplePublisher Node
    
    Subscriber_node = SubScriberNodes()

    try:
        # Spins the Node to activate the callbacks

        rclpy.spin(Subscriber_node)
        
        

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