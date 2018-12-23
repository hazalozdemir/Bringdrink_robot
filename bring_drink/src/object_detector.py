#!/usr/bin/env python
"""
usage:
rosrun proteus_demo ImageView.py image:=/ATRV/CameraMain
"""
#this code taken from web to use as UI template
#but the object detection algorithm implemented by BringDrink team
import roslib
roslib.load_manifest('rospy')
roslib.load_manifest('sensor_msgs')
import rospy
from sensor_msgs.msg import Image

import cv2
import numpy as np
from cv_bridge import CvBridge
from matplotlib import pyplot as plt


import wx
import sys

class ImageViewApp(wx.App):
    def OnInit(self):
        self.frame = wx.Frame(None, title = "ROS Image View", size = (256, 256))
        self.panel = ImageViewPanel(self.frame)
        self.frame.Show(True)
        return True


class ImageViewPanel(wx.Panel):
    """ class ImageViewPanel creates a panel with an image on it, inherits wx.Panel """
    def update(self, image):
        temp = image[:][0]
        image[:][0] = image[:][2]
        image[:][2] = temp[:]
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) # convert to grayscale
        # threshold to get just the signature (INVERTED)
        retval, thresh_gray = cv2.threshold(gray, thresh=100, maxval=255, \
                                           type=cv2.THRESH_BINARY_INV)

        img, contours, hierarchy = cv2.findContours(thresh_gray,cv2.RETR_LIST, \
                                           cv2.CHAIN_APPROX_SIMPLE)

        # Find object with the biggest bounding box
        mx = (0,0,0,0)      # biggest bounding box so far
        mx_area = 99999999
        for cont in contours:
            x,y,w,h = cv2.boundingRect(cont)
            area = w*h
            if area < mx_area and area > 300:
                mx = x,y,w,h
                mx_area = area
        x,y,w,h = mx
        roi=image[y:y+h,x:x+w]
        height, width = roi.shape[:2]
        crop_center = roi[height/2-15:height/2+15, width/2-15:width/2+15]
        color = ('r','g','b')

        for i,col in enumerate(color):
            histr = cv2.calcHist([roi],[i],None,[256],[0,256])
            plt.plot(histr,color = col)

        #plt.show()
        #cv2.imshow("Robot View", roi);
        b, g, r = cv2.split(crop_center)
        bmean = b.mean()
        gmean = g.mean()
        rmean = r.mean()
        mean = [bmean, gmean, rmean]
        max = np.amax(mean)
        if rmean < 130 and rmean > 80 and gmean > 35 and gmean < 50:
            print("fanta")
        else:
            if max == bmean:
                print("sprite")
            elif max == gmean:
                print("sprite")
            elif max == rmean:
                print("coke")
            else:
                print("gray")
        #cv2.rectangle(image, (x, x+w), (y, y+h), (0,0,255), 2)


        cv2.imshow("Crop Color", roi);



def handle_image(image):
    # make sure we update in the UI thread
    image = CvBridge().imgmsg_to_cv2(image, 'bgr8')
    wx.CallAfter(wx.GetApp().panel.update, image)
    # http://wiki.wxpython.org/LongRunningTasks

def main(argv):
    app = ImageViewApp()
    rospy.init_node('ImageView')
    rospy.Subscriber('/camera/rgb/image_raw', Image, handle_image)
    print(__doc__)
    app.MainLoop()
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))
