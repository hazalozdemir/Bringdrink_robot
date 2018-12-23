#!/usr/bin/env python

"""This module is a simple demonstration of voice control
for ROS turtlebot using pocketsphinx
"""
from std_msgs.msg import String

import argparse
import roslib
import rospy

from pocketsphinx.pocketsphinx import *
from sphinxbase.sphinxbase import *
import pyaudio

class Voice_Control(object):

    def __init__(self, model, lexicon, kwlist):
        self.msg = String()

        #rospy.init_node('voice_cmd_vel')
        rospy.on_shutdown(self.shutdown)
        self.speech_pub = rospy.Publisher('voice', String, queue_size=1)
        rospy.init_node('speech', anonymous = True)
        rate = rospy.Rate(10)	

        # initialize pocketsphinx
        config = Decoder.default_config()
        config.set_string('-hmm', model)
        config.set_string('-dict', lexicon)
        config.set_string('-kws', kwlist)

        stream = pyaudio.PyAudio().open(format=pyaudio.paInt16, channels=1,
                        rate=16000, input=True, frames_per_buffer=1024)
        stream.start_stream()

        self.decoder = Decoder(config)
        self.decoder.start_utt()
        self.number = "empty"
        self.selection = "empty"
        self.table_number = "empty"
        while not rospy.is_shutdown():
            buf = stream.read(1024)
            if buf:
                self.decoder.process_raw(buf, False, False)
            else:
                break
            self.parse_order()
            
    def give_order(self):
        
        order = str(self.number) + ',' + self.selection + ',' + str(self.table_number)
        
        print("Your order is",self.number, self.selection, "to table ",self.table_number)
        self.msg.data = order
                
        self.speech_pub.publish(self.msg)
        print("message published")
        rate = rospy.Rate(10)	# sorun
        rate.sleep()		#sleep
        self.msg.data = "empty"
        self.speech_pub.publish(self.msg)
        print("message published 2")
        self.number = "empty"
        self.selection = "empty"
        self.table_number = "empty"
        
    def parse_order(self):

        if self.decoder.hyp() != None:
			#print ([(seg.word, seg.prob, seg.start_frame, seg.end_frame)
				for seg in self.decoder.seg()])
			#print ("Detected keyphrase, restarting search")          
			seg.word = seg.word.lower()
			self.decoder.end_utt()
			self.decoder.start_utt()
			
			if self.number == "empty":
				print(self.number)
				if seg.word.find("one") > -1:
					self.number = "one"
					
				elif seg.word.find("two") > -1:
					self.number = "two"
					
				elif seg.word.find("three") > -1:
					self.number = "three"
			elif self.number != "empty" and self.selection == "empty":
				print(self.selection)
				if seg.word.find("coke") > -1:
					self.selection = "coke"
				
				elif seg.word.find("sprite") > -1:
					self.selection = "sprite"
					
				elif seg.word.find("fanta") > -1:
					self.selection = "fanta"
			elif self.selection != "empty":
				print(self.table_number)
				if seg.word.find("one") > -1:
					self.table_number = "one"
				
				elif seg.word.find("two") > -1:
					self.table_number = "two"
				
				elif seg.word.find("three") > -1:
					self.table_number = "three"
					

			if self.number != "empty" and self.selection != "empty" and self.table_number != "empty":
					self.give_order()

      
        
    def shutdown(self):

        rospy.loginfo("Stop Voice_Control")
        #self.pub_.publish(Twist())
        rospy.sleep(1)
if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Control ROS turtlebot using pocketsphinx.')
    parser.add_argument('--model', type=str,
        default='/usr/local/lib/python2.7/dist-packages/pocketsphinx/model/en-us',
        help='''acoustic model path
        (default: /usr/local/lib/python2.7/dist-packages/pocketsphinx/model/en-us)''')
    parser.add_argument('--lexicon', type=str,
        default='words2.dic',
        help='''pronunciation dictionary
        (default: words2.dic)''')
    parser.add_argument('--kwlist', type=str,
        default='key_list3.kwlist',
        help='''keyword list with thresholds
        (default: key_list3.kwlist)''')
    ##parser.add_argument('--rospub', type=str,
    ##    default='mobile_base/commands/velocity',
     ##   help='''ROS publisher destination
       ## (default: mobile_base/commands/velocity)''')

    args = parser.parse_args()
    Voice_Control(args.model, args.lexicon, args.kwlist)


