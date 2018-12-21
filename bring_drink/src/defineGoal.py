#!/usr/bin/env python
# license removed for brevity

import rospy

# Brings in the SimpleActionClient
import actionlib
# Brings in the .action file and messages used by the move base action
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from gazebo_msgs.msg import ModelState
from std_msgs.msg import String

fanta_no = 24
cola_no = 19
sprite_no = 25

table1_drinks = 0
table2_drinks = 0
table3_drinks = 0

objects = {
    #table 3 coords
    "three" : {
        "pos_coor_x" : -1.595,
        "pos_coor_y" : 5.525,
        "ori_z" : 0.990,
        "ori_w" : -0.138,
    },

    #table 2 coords
    "two" : {
        "pos_coor_x" : -1.632,
        "pos_coor_y" : 1.608,
        "ori_z" : 0.996,
        "ori_w" : -0.090,
    },

    #table 1 coords
    "one" : {
        "pos_coor_x" : -1.600,
        "pos_coor_y" : -2.363,
        "ori_z" : 0.997,
        "ori_w" : -0.073,
    },



    #coke coords
    "coke" : {
        "pos_coor_x" : 4.445,
        "pos_coor_y" : 2.161,
        "ori_z" : 0.066,
        "ori_w" : 0.998,
    },

    #sprite coords
    "sprite" : {
        "pos_coor_x" : 4.319,
        "pos_coor_y" : 0.452,
        "ori_z" : -0.131,
        "ori_w" : 0.991,
    },


    #fanta coords
    "fanta" : {
        "pos_coor_x" : 4.347,
        "pos_coor_y" : -1.492,
        "ori_z" : -0.134,
        "ori_w" : 0.991,
    }
}

def parse_order(msg):
    global cola_no, fanta_no, sprite_no, table1_drinks, table2_drinks, table3_drinks
    rate = rospy.Rate(10)
    pub = rospy.Publisher('/gazebo/set_model_state', ModelState, queue_size=10)
    #order = rospy.Subscriber('voice', String, callback)
    printr(msg.data)
    
    order = msg.split(',')
    drink = movebase_client(order[1])
    
    ordered_drink = ModelState()

    if (order[1] == "fanta"):
       model_name = "can_fanta_clone_" + str(fanta_no)
       fanta_no -= 1
    elif (order[1] == "coke"):
       model_name = "can_coke_clone_" + str(cola_no)
       cola_no -= 1
    elif (order[1] == "sprite"):
       model_name = "can_sprite_clone_" + str(sprite_no)
       sprite_no -= 1

    ordered_drink.model_name = model_name

    if (order[2] == "one"):
    	ordered_drink.pose.position.x = -2.3 - 0.1*(table1_drinks%2)
        ordered_drink.pose.position.y = -2.3 + 0.1*table1_drinks
        ordered_drink.pose.position.z = -1
        table1_drinks += 1

    elif (order[2] == "two"):
    	ordered_drink.pose.position.x = -2.3 - 0.1*(table2_drinks%2)
        ordered_drink.pose.position.y = 1.3 + 0.1*table2_drinks
        ordered_drink.pose.position.z = -1
        table2_drinks += 1

    elif (order[2] == "three"):
    	ordered_drink.pose.position.x = -2.3 - 0.1*(table3_drinks%2)
        ordered_drink.pose.position.y = 5.2 + 0.1*table3_drinks
        ordered_drink.pose.position.z = -1
        table3_drinks += 1
    a = 0
    while a < 50:
        pub.publish(ordered_drink)
        rate.sleep()
        a += 1
    #remove drink from kitchen
    table = movebase_client(order[2])
    
    ordered_drink.pose.position.z = 0.8
    a = 0
    while a < 50:
        pub.publish(ordered_drink)
        rate.sleep()
        a += 1
        
    #add drink to table
    return table

def movebase_client(data):

    global objects

    navObj = {
            "pos_coor_x" : 0,
            "pos_coor_y" : 0,
            "ori_z" : 0,
            "ori_w" : 0
    }

    if(data == "coke"):
        navObj = objects["coke"]
    elif(data == "fanta"):
        navObj = objects["fanta"]
    elif(data == "sprite"):
        navObj = objects["sprite"]
    elif(data == "one"):
        navObj = objects["one"]
    elif(data == "two"):
        navObj = objects["two"]
    elif(data == "three"):
        navObj = objects["three"]
    else:
        print("navigation target can not recognized")

   # Create an action client called "move_base" with action definition file "MoveBaseAction"
    client = actionlib.SimpleActionClient('move_base',MoveBaseAction)

   # Waits until the action server has started up and started listening for goals.
    client.wait_for_server()

   # Creates a new goal with the MoveBaseGoal constructor
    goal = MoveBaseGoal()
    goal.target_pose.header.frame_id = "map"
    goal.target_pose.header.stamp = rospy.Time.now()


   # Move 0.5 meters forward along the x axis of the "map" coordinate frame

    goal.target_pose.pose.position.x = navObj["pos_coor_x"]


    goal.target_pose.pose.position.y = navObj["pos_coor_y"]
   # No rotation of the mobile base frame w.r.t. map frame

    goal.target_pose.pose.orientation.z = navObj["ori_z"]

    goal.target_pose.pose.orientation.w = navObj["ori_w"]

   # Sends the goal to the action server.
    client.send_goal(goal)
   # Waits for the server to finish performing the action.
    wait = client.wait_for_result()
   # If the result doesn't arrive, assume the Server is not available
    if not wait:
        rospy.logerr("Action server not available!")
        rospy.signal_shutdown("Action server not available!")
    else:
    # Result of executing the action
        return client.get_result()

# If the python node is executed as main process (sourced directly)
if __name__ == '__main__':
    rospy.init_node('movebase_client_py')
    while not rospy.is_shutdown():
        try:
           # Initializes a rospy node to let the SimpleActionClient publish and subscribe

			result = parse_order("one,fanta,two")
			result = movebase_client("coke")
			rospy.Subscriber('voice', String, parse_order)
			if result:
				rospy.loginfo("Goal execution done!")
        except rospy.ROSInterruptException:
            rospy.loginfo("Navigation test finished.")
