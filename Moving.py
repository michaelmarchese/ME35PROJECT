''' Code from ROS2 Docs
Modifications by Briana Bouchard

This code creates a publisher node and publishes a string to a topic with a counter every 0.5 seconds.
'''

import rclpy # imports rclpy client library 
from rclpy.node import Node # imports Node class of rclpy library

from std_msgs.msg import String # imports ROS2 built-in string message type
from geometry_msgs.msg import Twist,Vector3,Pose,Transform
from nav_msgs.msg import Odometry 
from rclpy.qos import qos_profile_sensor_data,QoSProfile,ReliabilityPolicy
import requests 
import json 

URL = 'https://api.airtable.com/v0/appPFWlX5Bx83P1XM/Projects?api_key=keyV4gvD2zJLNdP6d'

def getRequest():
    r = requests.get(url = URL, params = {})


    data1 = r.json()
    #angular
    Angularx=data1['records'][1]['fields']['X']
    Angulary=data1['records'][1]['fields']['Y']
    Angularz=data1['records'][1]['fields']['Z']

    Linearx=data1['records'][2]['fields']['X']
    Lineary=data1['records'][2]['fields']['Y']
    Linearz=data1['records'][2]['fields']['Z']

    return[Linearx,Lineary,Linearz,Angularx,Angulary,Angularz]




# Creates SimplePublisher class which is a subclass of Node 
class SimplePublisher(Node):

    # Defines class constructor
    def __init__(self):

        # Initializes and gives Node the name simple_publisher and inherits the Node class's attributes by using 'super()'
        super().__init__('simple_publisher')

        # Creates a publisher based on the message type "String" that has been imported from the std_msgs module above
        #* Works if you actaully just put cmd_vel but isnt sending to to the subscriber tho
        self.publisher_ = self.create_publisher(Transform,'/cmd_vel', 10)

        # Set delay in seconds
        timer_period = 0.5  

        # Creates a timer that triggers a callback function after the set timer_period
        self.timer = self.create_timer(timer_period, self.timer_callback)

        # Sets initial counter to zero
        self.i = 0

        self.subscription = self.create_subscription(Odometry,'/odom',self.listener_callback, QoSProfile(depth=10, reliability=ReliabilityPolicy.BEST_EFFORT))

        self.odom_data = 0

        # self.timer2 = self.create_timer(timer_period, self.listener_callback)

    def timer_callback(self):
        # Assigns message type "String" that has been imported from the std_msgs module above
        self.msg = Transform()
        
        # Publishes `msg` to topic 
        x = input("Start Or Stop:")
        if(x == 'Start'):
            values=getRequest()

            self.msg.translation.x = float(values[0])
            self.msg.translation.y = float(values[1])
            self.msg.translation.z = float(values[2])
            self.msg.rotation.x =float(values[3])
            self.msg.rotation.y =float(values[4])
            self.msg.rotation.z =float(values[5])
            self.msg.rotation.w = 0.0


            #*Header
            


            #*Pose
            # self.msg.pose.pose.position.x = 1.0
            # self.msg.pose.pose.position.y = 0.0
            # self.msg.pose.pose.position.z = 0.0
            # self.msg.pose.pose.orientation.z = 0.0
            # self.msg.pose.pose.orientation.x = 1.0
            # self.msg.pose.pose.orientation.y = 0.0
            # self.msg.pose.pose.orientation.w = 1.0

            #*Twist
            # self.msg.twist.twist.linear.x = 1.0
            # self.msg.twist.twist.linear.y = 0.0
            # self.msg.twist.twist.linear.z = 0.0
            # self.msg.twist.twist.angular.z = 1.0
            # self.msg.twist.twist.angular.x = 0.0
            # self.msg.twist.twist.angular.y = 0.0







            self.publisher_.publish(self.msg)  
            print(self.listener_callback(self))
            x = 'Stop'


    def listener_callback(self, msg2):
        self.odom_data = msg2

        return print(self.odom_data)



        # return odom_data

        # self.test =  self.odom_data.pose.pose.position
        # print(self.test)



        





        
       
    








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