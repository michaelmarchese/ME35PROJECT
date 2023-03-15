import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node
from std_msgs.msg import String 
from geometry_msgs.msg import Twist,Vector3
from rclpy.qos import qos_profile_sensor_data
from irobot_create_msgs.msg import IrIntensityVector
from Tensorflow import tensortest

from irobot_create_msgs.action import RotateAngle

#*Action stuff(left right)
class RotateActionClient(Node):
 
 
    def __init__(self):

        super().__init__('rotate_action_client')
        self._action_client = ActionClient(self, RotateAngle, 'rotate_angle')

    def send_goal(self, angle=1.57, max_rotation_speed=2):

        goal_msg = RotateAngle.Goal()
        goal_msg.angle = angle 
        goal_msg.max_rotation_speed = max_rotation_speed

        self._action_client.wait_for_server()
        self._send_goal_future = self._action_client.send_goal_async(goal_msg)
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
        '''
        Purpose
        -------
        Similar to sending the goal, we will get a future that will complete when the result is ready.
        '''
        result = future.result().result
        self.get_logger().info('Result: {0}'.format(result))
        rclpy.shutdown()

#*Forward move

class SimplePublisher(Node):

    # Defines class constructor
    def __init__(self):

        # Initializes and gives Node the name simple_publisher and inherits the Node class's attributes by using 'super()'
        super().__init__('simple_publisher')

        # Creates a publisher based on the message type "String" that has been imported from the std_msgs module above
        #* Works if you actaully just put cmd_vel but isnt sending to to the subscriber tho
        self.publisher_ = self.create_publisher(Twist, '/cmd_vel', 10)
        self.subscription = self.create_subscription(IrIntensityVector, '/ir_intensity', self.listener_callback, qos_profile_sensor_data)

        # Set delay in seconds
        timer_period = 0.5  

        # Creates a timer that triggers a callback function after the set timer_period
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.timer2 = self.create_timer(timer_period, self.listener_callback)
        
        self.IR_data = 0
        # Sets initial counter to zero
        self.i = 0

    def timer_callback(self):
        # Assigns message type "String" that has been imported from the std_msgs module above
        self.msg = Twist()
        
        # Publishes `msg` to topic 
        x = input("Start Or Stop:")
        if(x == 'Start'):

            self.msg.linear.x = 0.1
            self.publisher_.publish(self.msg)  
            x = 'Stop'


#*IR intensity

class IRSubscriber(Node):
    '''
    The IRSubscriber class is created which is a subclass of Node.
    The Node is subscribing to the /ir_intensity topic.
    '''
    
    def __init__(self):
        '''
        The following line calls the Node class' constructor and declares a node name,
        which is 'IR_subscriber' in this case. 
        '''
        super().__init__('IR_subscriber')
        '''
        This line indicates that the node is subscribing to the IrIntensityVector
        type over the '/ir_intensity' topic. 
        '''
        print('Creating subscription to to the IrIntensityVector type over the /ir_intensity topic')
        self.subscription = self.create_subscription(
            IrIntensityVector, '/ir_intensity', self.listener_callback,
            qos_profile_sensor_data)

    def listener_callback(self, msg:IrIntensityVector):
        '''
        The subscriber's callback listens and as soon as it receives the message,
        this function runs. 
        This callback function is basically printing what it hears. It runs the data
        it receives in your terminal (msg).  
        '''
        print('Now listening to IR sensor readings it hears...')

        self.printIR(msg)

    def printIR(self, msg):
        '''
        This function is used in the above function. Its purpose is to determine 
        which parts of the info are worth showing.
        :type msg: IrIntensity
        :rtype: None
        The msg is returned from our topic '/ir_intensity.'
        To get components of a message, use the '.' dot operator. 
        '''
        print('Printing IR sensor readings:')
        for reading in msg.readings: 
            val = reading.value
            #print(reading)
            print(msg.readings[3].value)
            #print("IR Sensor:" + str(val))
        return print(msg.readings[3].value)


def goleft90(args=None):
    rclpy.init(args=args)
    action_client = RotateActionClient()

    angle = 1.57
    speed = 0.5 # Max 1.9

    action_client.send_goal(angle, speed)
    rclpy.spin_once(action_client)

def goright90(args=None):
    rclpy.init(args=args)
    action_client = RotateActionClient()

    angle = -1.57
    speed = 0.5 # Max 1.9

    action_client.send_goal(angle, speed)
    rclpy.spin_once(action_client)

def printIRSTUFF(args=None):
    rclpy.init(args=args)
    IR_subscriber = IRSubscriber()
    rclpy.spin(IR_subscriber)
    IR_subscriber.printIR()
    IR_subscriber.destroy_node()


def main(args=None):
    #printIRSTUFF()
    print(tensortest())
#! if you are having trouble with things not working try this spin_once

    try:
        # Spins the Node to activate the callbacks
        print("hi")
        # printIRSTUFF()
        #rclpy.spin_once(simple_publisher)



    except KeyboardInterrupt:
        print('\nCaught Keyboard Interrupt')

        # Destroys the node that was created
        simple_publisher.destroy_node()

        # Shuts down rclpy 
        rclpy.shutdown()




if __name__ == '__main__':
    main()
