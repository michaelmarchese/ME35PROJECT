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
class SimplePublisher(Node):

    # Defines class constructor
    def __init__(self):

        # Initializes and gives Node the name simple_publisher and inherits the Node class's attributes by using 'super()'
        super().__init__('simple_publisher')

        # Creates a publisher based on the message type "String" that has been imported from the std_msgs module above
        self.publisher_ = self.create_publisher(Twist, '/cmd_vel', 10)

        # Set delay in seconds
        timer_period = 0.5  

        # Creates a timer that triggers a callback function after the set timer_period
        self.timer = self.create_timer(timer_period, self.timer_callback)

        # Sets initial counter to zero
        self.i = 0

    def timer_callback(self):
        # Assigns message type "String" that has been imported from the std_msgs module above
        msg = Twist()

        # Publishes `msg` to topic 

        msg.linear.x = 2.0
        self.publisher_.publish(msg) 
        self.get_logger().info('Publishing: %s' % msg.linear.x) 



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


class MotorSubscriber(Node):
    '''
    The MotorSubscriber class is created which is a subclass of Node.
    The Node is subscribing to the /simple_publisher topic.
    '''
    
    def __init__(self):
        '''
        The following line calls the Node class' constructor and declares a node name,
        which is 'simple_publisher' in this case. 
        '''
        super().__init__('simple_subscriber')
        '''
        This line indicates that the node is subscribing to the IrIntensityVector
        type over the '/ir_intensity' topic. 
        '''
        print('Creating subscription to to the geometry_msgs type over the /Motor_subscriber topic')
        self.subscription = self.create_subscription(
            Twist, '/simple_subscriber', self.listener_callback,10)

    def listener_callback(self, msg:Twist):
        '''
        The subscriber's callback listens and as soon as it receives the message,
        this function runs. 
        This callback function is basically printing what it hears. It runs the data
        it receives in your terminal (msg).  
        '''
        print('Now listening to IR sensor readings it hears...')

        self.printTwist(msg)

    def printTwist(self, msg):
        '''
        This function is used in the above function. Its purpose is to determine 
        which parts of the info are worth showing.
        :type msg: IrIntensity
        :rtype: None
        The msg is returned from our topic '/ir_intensity.'
        To get components of a message, use the '.' dot operator. 
        '''
        print('Printing robot location:')
        for reading in msg.readings: 
            val = reading.value
            print("x:" + str(val))



def main(args=None):
    '''
    This line initializes the rclpy library. 
    '''
    rclpy.init(args=args)
    '''
    This creates the node.
    '''
    motor_subscriber = MotorSubscriber()
    '''
    The node is then "spun" so its callbacks are called.
    '''
    print('Callbacks are called.')
    try:
        rclpy.spin(motor_subscriber)
    except KeyboardInterrupt:
        print('\nCaught keyboard interrupt')
    finally:
        '''Destroying the node acts as a "reset" so we don't run into
        any problems when we try and run again'''
        print("Done")
        motor_subscriber.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
