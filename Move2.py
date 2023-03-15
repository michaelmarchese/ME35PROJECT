import rclpy
from keras.models import load_model  # TensorFlow is required for Keras to work
from PIL import Image, ImageOps  # Install pillow instead of PIL
import numpy as np
from rclpy.action import ActionClient
from rclpy.node import Node
from std_msgs.msg import String 
from geometry_msgs.msg import Twist,Vector3
from rclpy.qos import qos_profile_sensor_data
from irobot_create_msgs.msg import IrIntensityVector
from picamera2 import Picamera2 
import cv2 as cv 
import numpy as np
from libcamera import controls
import time

from irobot_create_msgs.action import RotateAngle

picam2 = Picamera2()
picam2.set_controls({"AfMode": controls.AfModeEnum.Continuous}) #sets auto focus mode


picam2.start() #must start the camera before taking any images
model = load_model("/home/tuftsrobot/ME35PROJECT/keras_model.h5", compile=False)

def tensortest():
    # picam2 = Picamera2()
    # picam2.set_controls({"AfMode": controls.AfModeEnum.Continuous}) #sets auto focus mode


    # picam2.start() #must start the camera before taking any images
    # time.sleep(1)

    # picam2.capture_file('/home/tuftsrobot/ME35PROJECT/imagetensor.jpg')

    # Disable scientific notation for clarity
    np.set_printoptions(suppress=True)


    # Load the model

    # Load the labels
    class_names = open("/home/tuftsrobot/ME35PROJECT/labels.txt", "r").readlines()

    # Create the array of the right shape to feed into the keras model
    # The 'length' or number of images you can put into the array is
    # determined by the first position in the shape tuple, in this case 1
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

    # Replace this with the path to your image
    image = Image.open('/home/tuftsrobot/ME35PROJECT/imagetensor.jpg').convert("RGB")

    # resizing the image to be at least 224x224 and then cropping from the center
    size = (224, 224)
    image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)

    # turn the image into a numpy array
    image_array = np.asarray(image)

    # Normalize the image
    normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1

    # Load the image into the array
    data[0] = normalized_image_array

    # Predicts the model
    prediction = model.predict(data)
    index = np.argmax(prediction)
    class_name = class_names[index]
    confidence_score = prediction[0][index]

    # Print prediction and confidence score
    print("Class:", class_name[2:], end="")
    print("Confidence Score:", confidence_score)

    # picam2.stop()
    #! ill comment what was working before just check u need to get the class
    # return confidence_score
    return [confidence_score, class_name]

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
        #self.subscription = self.create_subscription(IrIntensityVector, '/ir_intensity', self.listener_callback, qos_profile_sensor_data)

        # Set delay in seconds
        timer_period = 0.5  

        # Creates a timer that triggers a callback function after the set timer_period
        self.timer = self.create_timer(timer_period, self.timer_callback)
        #self.timer2 = self.create_timer(timer_period, self.listener_callback)
        
        self.IR_data = 0
        # Sets initial counter to zero
        self.i = 0

    def timer_callback(self):
        # Assigns message type "String" that has been imported from the std_msgs module above
        self.msg = Twist()
        
        # Publishes `msg` to topic 
        #x = input("Start Or Stop:")
        #if(x == 'Start'):

        self.msg.linear.x = 0.1
        self.publisher_.publish(self.msg)  
        time.sleep(1)

        picam2.capture_file('/home/tuftsrobot/ME35PROJECT/imagetensor.jpg')
        lens_position = picam2.capture_metadata()['LensPosition']
        print(lens_position)

        #! this is not working it worked when i just had it return the confidence interval it could be that its making it a string or something try bringing it back later and check
        tensordata = tensortest()
        print("ClassMIKE" +tensordata[1])
        print("cONFIDENCE"+ str(tensordata[0]))
        if(tensordata[1] == "0 Class 1" and int(tensordata[0])>0.9996):
            goleft90()
            print("complete")
           # x = 'Stop'
        # if(tensordata()>0.9996):
        #     goleft90()
        #     print("complete")
        # # x = 'Stop'


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
    rclpy.init(args=args)

    # Creates the SimplePublisher Node
    simple_publisher = SimplePublisher()
    #printIRSTUFF()
    #print(tensortest())
#! if you are having trouble with things not working try this spin_once

    try:
        # Spins the Node to activate the callbacks
        rclpy.spin(simple_publisher)
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
