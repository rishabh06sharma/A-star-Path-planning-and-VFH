#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from geometry_msgs.msg import PoseStamped
from sensor_msgs.msg import LaserScan
from nav_msgs.msg import Odometry
i=0
from math import pi
import math
def callback2(data2):

#Publish the x and y position of robot
	global xrpose, yrpose, zrorien, w, p_o
	xrpose=(data2.pose.pose.position.x)
	yrpose=(data2.pose.pose.position.y)
	zrorien=(data2.pose.pose.orientation.z)
	w=(data2.pose.pose.orientation.w)
	p_o=[xrpose,yrpose,zrorien,w]


#slope
def slope(a,b,c,d):
	#xpose,ypose,xrpose,yrpose
	s=((b-d)/(a-c))    
	return s



def quaternion_to_euler(x, y, z, w):
#converting quaternion to euler
	global XX,YY,NZ
        t0 = +2.0 * (w * x + y * z)
        t1 = +1.0 - 2.0 * (x * x + y * y)
        XX = math.degrees(math.atan2(t0, t1))

        t2 = +2.0 * (w * y - z * x)
        t2 = +1.0 if t2 > +1.0 else t2
        t2 = -1.0 if t2 < -1.0 else t2
        YY = math.degrees(math.asin(t2))

        t3 = +2.0 * (w * z + x * y)
        t4 = +1.0 - 2.0 * (y * y + z * z)
        ZZ = math.degrees(math.atan2(t3, t4))

# only converting z into 0 to 360 range	
	if ZZ<0:
		NZ=180+(90+ZZ)
	else:
		NZ=ZZ

        return XX, YY, NZ
def callback(data):
#takes the laser data and publish it to robot velocity
	global initial_slope,sl,ang,initial_angle,angle1, angg,c_ang,i

	i=i+1
	a=(data.ranges[1])
	vel_=Twist()
	rate = rospy.Rate(10) # 10hz
	pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
	

        #divide in sectors 
	d_a_c(data.ranges)

	sl=slope(xpose,ypose,xrpose,yrpose)
        ang=math.atan(sl)*(180/math.pi)
	angles=quaternion_to_euler(0,0,zrorien,w)
        print(data.ranges[181])
        if ang<0:
            ang=abs(ang)+90
        
    #bug2 algorithm
	#line follow mode

	def linefollow():  
		vel_.linear.x=0.2
		vel_.angular.z=0
        def wallfollow():
            d_a_c(data.intensities)
            print(r)
            if (1 in r) or (1 in fr) or (1 in f) or(1 in fl):
                vel_.angular.z=-2
		vel_.linear.x=0
	    if (1 not in r) or (1 not in fr) or (1 not in f):
		vel_.linear.x=1


	if (data.ranges[181]>0.90):
		if  round(ang)!=round(angles[2]) :
			vel_.angular.z=-0.1
		elif round(ang)==round(angles[2]): 
			linefollow()

        if (data.ranges[181]<=0.90):
        	wallfollow()



          
	vel_.linear.y=0
	vel_.linear.z=0
	
	vel_.angular.y=0
	pub.publish(vel_)		
	
        



def callback1(data1):
#Publish the x and y position of charger
	global xpose, ypose, pose
	#global b
	xpose=(data1.pose.position.x)
	ypose=(data1.pose.position.y)
	pose=[xpose,ypose]



	
def d_a_c(rg):
#divides the laser data into sections
	global l,fl,f,fr,r
	l=rg[0:71]
	fl=rg[72:143]
	f=rg[144:215]
	fr=rg[216:287]
	r=rg[288:361]
	return(l,fl,f,fr,r)

def bmyeye():
#subscribe to laser and carger position
	#global i
	#i +=1

	rospy.Subscriber("/base_pose_ground_truth", Odometry, callback2) 
	rospy.Subscriber("/homing_signal", PoseStamped, callback1)
	rospy.init_node('bmyeye', anonymous=True)
	rospy.Subscriber("/base_scan", LaserScan, callback)

	    
	#print(i)
    	rospy.spin()

#def f_charger():

if __name__ == '__main__':
    try:
	bmyeye()
    except rospy.ROSInterruptException:
        pass

