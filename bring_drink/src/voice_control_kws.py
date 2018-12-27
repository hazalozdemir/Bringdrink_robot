#!/usr/bin/env python

from std_msgs.msg import String

import argparse
import roslib
import rospy

from pocketsphinx.pocketsphinx import *
from sphinxbase.sphinxbase import *
import pyaudio

### Some parts of the below code taken from https://github.com/gorinars/ros_voice_control/blob/master/ros_voice_control.py/###

class Voice_Control(object):

    def __init__(self, model, lexicon, kwlist):
        self.msg = String()

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

### BELOW CODE ADDED BY TEAM BRINGDRINK 2018 BLG456E PROJECT ###
            
    def give_order(self):
        
        order = str(self.number) + ',' + self.selection + ',' + str(self.table_number)
        
        print("Your order is",self.number, self.selection, "to table ",self.table_number)
        self.msg.data = order
                
        self.speech_pub.publish(self.msg)
        print("message published")
        rate = rospy.Rate(10)	
        rate.sleep()		
        self.msg.data = "empty"
        self.speech_pub.publish(self.msg)
        self.number = "empty"
        self.selection = "empty"
        self.table_number = "empty"
        
    def parse_order(self):

        if self.decoder.hyp() != None:  
			print ([(seg.word, seg.prob, seg.start_frame, seg.end_frame)
				for seg in self.decoder.seg()])    
			seg.word = seg.word.lower()
			self.decoder.end_utt()
			self.decoder.start_utt()
			
			if self.number == "empty":
				if seg.word.find("one") > -1:
					self.number = "one"
					print(self.number)
			
				elif seg.word.find("two") > -1:
					self.number = "two"
					print(self.number)
					
				elif seg.word.find("three") > -1:
					self.number = "three"
					print(self.number)

			elif self.number != "empty" and self.selection == "empty":
				if seg.word.find("coke") > -1:
					self.selection = "coke"
					print(self.selection)

				elif seg.word.find("sprite") > -1:
					self.selection = "sprite"
					print(self.selection)

					
				elif seg.word.find("fanta") > -1:
					self.selection = "fanta"
					print(self.selection)

			elif self.selection != "empty":
				if seg.word.find("one") > -1:
					self.table_number = "one"
					print(self.table_number)

				
				elif seg.word.find("two") > -1:
					self.table_number = "two"
					print(self.table_number)

				
				elif seg.word.find("three") > -1:
					self.table_number = "three"
					print(self.table_number)

					

			if self.number != "empty" and self.selection != "empty" and self.table_number != "empty":
					self.give_order()

        
    def shutdown(self):
        rospy.loginfo("Stop Voice_Control")
        rospy.sleep(1)

### Below code taken from https://github.com/gorinars/ros_voice_control/blob/master/ros_voice_control.py/###
        
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

    args = parser.parse_args()
    Voice_Control(args.model, args.lexicon, args.kwlist)


