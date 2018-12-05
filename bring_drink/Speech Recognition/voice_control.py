#!/usr/bin/env python

"""This module is a simple demonstration of voice control
for ROS turtlebot using pocketsphinx
"""

import argparse
import roslib
import rospy
from geometry_msgs.msg import Twist

from pocketsphinx.pocketsphinx import *
from sphinxbase.sphinxbase import *
import pyaudio


class ASRControl(object):

    def __init__(self, model, lexicon, kwlist, pub):
        self.msg = Twist()

        rospy.init_node('voice_cmd_vel')
        rospy.on_shutdown(self.shutdown)
        self.pub_ = rospy.Publisher(pub, Twist, queue_size=10)

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
        self.number = 0
        self.selection = "empty"
        while not rospy.is_shutdown():
            buf = stream.read(1024)
            if buf:
                self.decoder.process_raw(buf, False, False)
            else:
                break
            self.parse_order()
    def give_order(self):
        
        print("Your order is",self.number,self.selection )  
        self.number = 0
        self.selection = "empty"

    def parse_order(self):

        if self.decoder.hyp() != None:
            print ([(seg.word, seg.prob, seg.start_frame, seg.end_frame)
                for seg in self.decoder.seg()])
            print ("Detected keyphrase, restarting search")          
            seg.word = seg.word.lower()
            self.decoder.end_utt()
            self.decoder.start_utt()

            if seg.word.find("one") > -1:
                self.number = 1
                
            elif seg.word.find("two") > -1:
                self.number = 2
                
            elif seg.word.find("three") > -1:
                self.number = 3
            
            if seg.word.find("coke") > -1:
                self.selection = "coke"
            
            elif seg.word.find("sprite") > -1:
                self.selection = "sprite"
                
            elif seg.word.find("fanta") > -1:
                self.selection = "fanta"

            if(self.number != 0 and self.selection != "empty"):
                self.give_order()

        self.pub_.publish(self.msg)
      
        
    def shutdown(self):

        rospy.loginfo("Stop ASRControl")
        self.pub_.publish(Twist())
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
    parser.add_argument('--rospub', type=str,
        default='mobile_base/commands/velocity',
        help='''ROS publisher destination
        (default: mobile_base/commands/velocity)''')

    args = parser.parse_args()
    ASRControl(args.model, args.lexicon, args.kwlist, args.rospub)


