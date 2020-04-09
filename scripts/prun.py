#!/usr/bin/env python
import rospy
import numpy as np
from geometry_msgs.msg import Twist
from geometry_msgs.msg import PoseStamped
from sensor_msgs.msg import LaserScan
from nav_msgs.msg import Odometry
from itertools import count
from itertools import islice
from operator import add
import matplotlib.pyplot as plt
import copy
from geometry_msgs.msg import Quaternion
import math
def printer():
    print('MISSION ACCOMPLISHED')
def c2m(x0,y0):
    global x,y
    if x0<0 and x0!=int(x0):
        x0=x0-1
    if x0!=9:
        x=9+int(x0)
    else:
        x=17
    if y0<0 and y0!=int(y0):
        y0=y0-1
    if y0!=-10:
        y=10-int(y0)
    else:
        y=19
    return x,y
#slope
def slope(a,b,c,d):
	#xpose,ypose,xrpose,yrpose
	s=((b-d)/(a-c))    
	return s

#converting quaternion to euler
def quaternion_to_euler(x, y, z, w):
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
		NZ=180+(180+ZZ)
	else:
		NZ=ZZ

        return XX, YY, ZZ

#Publish the x and y position of robot 
def m2c(x00,y00):
    global x000,y000
    x00=float(x00)
    y00=float(y00)
    ax=(x00-9)
    bx=(x00-9)+1
    ay=(10-y00)
    by=(10-y00)-1
    x000=((ax+bx)/2)
    y000=((ay+by)/2)
    # x000=ax
    # y000=by
#Publish the x and y position of robot 
def callback2(data2): 
	global xx,yy,zrorien,w,roll,pitch,yaw
	xx=(data2.pose.pose.position.x)
	yy=(data2.pose.pose.position.y)
	zrorien=(data2.pose.pose.orientation.z)
	w=(data2.pose.pose.orientation.w)
	q=np.array([data2.pose.pose.orientation.x,data2.pose.pose.orientation.y,data2.pose.pose.orientation.z,data2.pose.pose.orientation.w])
     
#takes the laser data and publish it to robot velocity
def astar(x,y,xd,yd):

    global final_path
    import numpy as np
    import copy
    from math import sqrt
    from collections import OrderedDict
    map = [0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,0,0,
        0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,0,0,
        0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
        1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
        0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
        0,0,1,0,0,0,1,1,1,1,1,1,0,0,0,0,0,0,
        0,0,1,0,0,0,1,1,1,1,1,1,0,0,0,0,0,0,
        0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,1,1,0,
        0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1,1,1,
        0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,1,1,1,
        0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,1,1,
        0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,1,0,
        0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,
        0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,
        0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
        0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,
        0,0,0,0,0,0,0,0,1,1,0,0,0,1,1,1,1,0,
        0,0,0,0,0,0,0,0,1,1,1,0,0,1,1,1,1,0,
        0,0,0,0,0,0,0,1,1,1,0,0,0,1,1,1,1,0,
        0,0,0,0,0,0,0,0,1,1,0,0,0,1,1,1,1,1]
    #Creating empty list of open and closed nodes
    open=[]
    closed=[]
    nebr=[]
    #size of the map
    xx=20
    yy=18
    e=0
    #converting to the 2-D array
    map=np.reshape(np.array(map),(-1,yy))
    map=np.pad(map,((2,2),(2,2)), 'constant',constant_values=(1, 1))
    #Empty array
    ocost = copy.deepcopy(map)
    gcost = copy.deepcopy(map)
    addcost = copy.deepcopy(map)
    pathx=copy.deepcopy(map)
    pathy=copy.deepcopy(map)
    #Initial position
    [xpos,ypos]=[y+2,x+2]
    #save initial
    [xposj,yposj]=[xpos,ypos]
    #Final Poaition
    [xposf,yposf]=[yd+2,xd+2]
    # def lets_find_path():
    last_closed=[]
    def lets_find_path(pathx,pathy,xposf,yposf,xposi,yposi):
        while [xposi,yposi]!=[xposj,yposj]:
            a=[pathy[xposi,yposi]-2,pathx[xposi,yposi]-2]
            final_path.append(a)
            [xposi,yposi]=[pathx[xposi,yposi],pathy[xposi,yposi]]
        return final_path
        exit()
    def d(xpos,ypos,xposf,yposf,x0,y0):
        global dorigin
        global dgoal
        dorigin= (sqrt( (xpos - x0)**2 + (ypos - y0)**2 ))*10
        dgoal= (sqrt( (xposf - x0)**2 + (yposf - y0)**2 ))*10
    for lo in range(0,200):
        [c1,c2]=[xpos,ypos]
        # add indices to the open and closed list
        for a in range(-1,2):
            for b in range(-1,2):
                if map[xpos+a,ypos+b]==0 and [a,b]!=[0,0] and ([xpos+a,ypos+b] not in closed): 
                    open.append([xpos+a,ypos+b])
                    nebr.append([xpos+a,ypos+b])
                    pathx[xpos+a,ypos+b]=xpos 
                    pathy[xpos+a,ypos+b]=ypos
                    if [xpos+a,ypos+b]==[xpos-1,ypos+1] and map[xpos+a,ypos+b]==0:
                        if map[xpos,ypos+1]==1 and map[xpos-1,ypos]==1:
                            open.remove([xpos+a,ypos+b])
                            nebr.remove([xpos+a,ypos+b])
                else:
                        closed.append([xpos+a,ypos+b])
        for k in nebr:
            global x0,y0
            x0=k[0]
            y0=k[1]
            e=ocost[xpos,ypos]
            d(xpos,ypos,xposf,yposf,x0,y0)
            # ocost[x0,y0]=e+dorigin
            gcost[x0,y0]=dgoal
            if ocost[x0,y0]<e+dorigin:
                ocost[x0,y0]=ocost[x0,y0]
            elif ocost[x0,y0]==0:
                ocost[x0,y0]=e+dorigin
            else:
                ocost[x0,y0]=e+dorigin
            addcost[x0,y0]=ocost[x0,y0]+dgoal

        nebr=[0]
        nebr=[]
        minbox=[]
        for l in open:
            x0=l[0]
            y0=l[1]
            minbox.append(addcost[x0,y0])
        minind=minbox.index(min(minbox))
        [xpos,ypos]=open[minind]
        if [xpos,ypos]!=[xposf,yposf]:
            if [xpos,ypos] in open: open.remove([xpos,ypos])
            
        else:
            [xposi,yposi]=[xpos,ypos]
            np.savetxt("array3.txt", ocost, fmt="%s")
            final_path=[]
            xpo=xposi-2
            ypo=yposi-2
            final_path.append([ypo,xpo])
            lets_find_path(pathx,pathy,xposf,yposf,xposi,yposi)
            
        #find unique in open
        open= [list(y) for y in set([tuple(x) for x in open])]
        #find unique in closed
        closed= [list(y) for y in set([tuple(x) for x in closed])]

def callback(data):
	a=(data.ranges[1])
	vel_=Twist()
	rate = rospy.Rate(10) # 10hz
	pub= rospy.Publisher('/cmd_vel', Twist, queue_size=10)
        [x,y]=c2m(xx,yy)
        goalx=(rospy.get_param('/goalx'))
        goaly=(rospy.get_param('/goaly'))
        [goalxx,goalyy]=c2m(goalx,goaly)
        global i
        global su
        global a
        global path_
        i=i+1
        print(i)
        if i==1:
            #A* algorithm
            astar(x,y,goalxx,goalyy)
            print(final_path)
            # converting map 2 cordinates
            just2print=copy.deepcopy(final_path)
            path_len=len(final_path)
            final_path.remove([goalxx,goalyy])
            final_path.remove([x,y])
            path_=[]
            path_.append([goalx,goaly])
            for values in final_path:
                aq=values[0]
                bq=values[1]
                m2c(aq,bq)
                path_.append([x000,y000])
            path_.append([xx,yy])
            path_.reverse()
            with open("file.txt", "w") as output:
                output.write('Map values' + str(just2print) + '\n \n Coordinates-' + str(path_))
        # using range instead of intensities


        rangeee=list(data.ranges)
        inten=rangeee
        print(type(inten))
        for lal in range(0,len(inten)):
            if rangeee[lal]<1.5:
                inten[lal]=1
            else:
                inten[lal]=0

        print(inten)
        # inten=list(data.intensities)


        n=10
        final = [inten[i * n:(i + 1) * n] for i in range((len(inten) + n - 1) // n )]
        # taking max value
        for v in range(0,len(final)):
            final[v]=max(final[v])
        initial=final
        ###########hostogram
        maxlim=100
        for values in range(0,len(final)):
            if initial[values]==1:
                if acc[values]<maxlim:
                    acc[values]=acc[values]+1
                else:
                    acc[values]=maxlim
            if initial[values]==0:
                if initial[values]<maxlim and initial[values]>0:
                    acc[values]=acc[values]-1
                else:
                    acc[values]=0
            if acc[values]>30:
                bcc[values]=1
            else:
                bcc[values]=0
        #robot size compensation (make some changes near dcc if you change rcomp)
        rcomp=3
        dcc=copy.deepcopy(bcc)
        for vv in range(rcomp,len(bcc)-rcomp):
                if bcc[vv]==1:
                    dcc[vv-(rcomp-1)]=1
                    dcc[vv+(rcomp-1)]=1
                    dcc[vv-(rcomp-2)]=1
                    dcc[vv+(rcomp-2)]=1
                    dcc[vv-(rcomp-3)]=1
                    dcc[vv+(rcomp-3)]=1                    
                    dcc[vv-rcomp]=1
                    dcc[vv+rcomp]=1

        #finding the angle
        # print(path_)
        # dist=copy.deepcopy(path_)
        # for ooo in range(0,len(path_)):
        #     [xl,yl]=path_[ooo]
        #     dist[ooo]=((((xl-xx)**2)+(((yl-yy)**2)))**0.5)
        # mmm = min(i for i in dist if i > 0)
        # indd=dist.index(mmm)
        # print(indd)
        # [xp,yp]=path_[indd]
        [xp,yp]=path_[1]
        # [xp,yp]=[-4,-1]
        import numpy as np

        if yy>yp:
            a = np.array([xx+5,yy])
            b = np.array([xx,yy])
            c = np.array([xp,yp])
            ba = a - b
            bc = c - b
            cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
            angg = -np.degrees((np.arccos(cosine_angle)))
        if yy<yp:
            a = np.array([xx+5,yy])
            b = np.array([xx,yy])
            c = np.array([xp,yp])
            ba = a - b
            bc = c - b

            cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
            angg = np.degrees(np.arccos(cosine_angle))

        ang=list(quaternion_to_euler(0,0,zrorien,w))
        ###### angg => angle of the destination
        ###### ang => angle of the orientation
        ###VFH
        #creating corrosponding angles list
        if ang[2]<=0:
            abc=ang[2]-90
            if abs(abc)>180:
                ref=180-(-(180+abc))
            else:
                ref=abc
        if ang[2]>0:
            ref=ang[2]-90
        #creating corrosponding angles list
        angle=copy.deepcopy(dcc)
        if ref<=0:
            angle[0]=ref+5
            for vvv in range(1,len(angle)):
                angle[vvv]=angle[vvv-1]+5
        if ref>0:
            abcc=ref+5
            if abcc>180:
                angle[0]=(ref+5)-360
            else:
                angle[0]=ref+5
            for vvv in range(1,len(angle)):
                abc=angle[vvv-1]+5
                if abc<180:
                    angle[vvv]=angle[vvv-1]+5
                else:
                    angle[vvv]=(angle[vvv-1]+5)-360

        acoff=1
        bcoff=1
        ccoff=1

        gcost=copy.deepcopy(angle)
        gcost[0]=abs(((angle[0])-angg)+((angle[0])-ang[2]))
        for uu in range(1,len(gcost)):
            if dcc[uu]==0:
                td=(acoff*((angle[uu])-angg))
                cd=(bcoff*((angle[uu])-ang[2]))
                # pd=(ccoff*(angle[uu-1]-angle[uu]))
                gcost[uu]=abs(td+(cd))
            else:
                gcost[uu]=1000000
        # print((gcost))
        thita=gcost.index(np.min(gcost))
        f_ang=angle[thita]
        # print(f_ang)
        # print(path_[1])
        # print(xp)
        # print(len(dcc))
        print(ang)

        if np.round(ang[2])!=np.round(f_ang) and ang[2]<f_ang and data.ranges[180]>0.7:
            vel_.angular.z=1
        if np.round(ang[2])!=np.round(f_ang) and ang[2]>f_ang and data.ranges[180]>0.7:
            vel_.angular.z=-1
        if np.round(ang[2])==np.round(f_ang) and data.ranges[180]>0.7:
            vel_.linear.x=1
        # if [np.round(xp),np.round(yp)]==[np.round(xx),np.round(yy)]:
        #     path_.remove([xp,yp])
        if ((((xp-xx)**2)+(((yp-yy)**2)))**0.5)<0.5:
            path_.remove([xp,yp])
        print([np.round(xp),np.round(yp)])
        print([np.round(xx),np.round(yy)])

        if data.ranges[180]<0.5 and data.ranges[210<0.5]:
            vel_.angular.z=-10
            pub.publish(vel_)
            astar(x,y,goalxx,goalyy)
        for aa in range(0,7):
            if data.ranges[180]<0.5:
                vel_.angular.z=-10
                vel_.linear.x=5
                pub.publish(vel_)
                astar(x,y,goalxx,goalyy)

	pub.publish(vel_)

def prun():
    #subscribe to laser and carger position

	rospy.Subscriber("/base_pose_ground_truth", Odometry, callback2)
	rospy.init_node('prun', anonymous=True)
	rospy.Subscriber("/base_scan", LaserScan, callback)   
        rospy.spin()

if __name__ == '__main__':
    try:
        i=0
        initial=np.zeros(37)
        acc=list(np.zeros(37))
        bcc=list(np.zeros(37))
        
	prun()
    except rospy.ROSInterruptException:
        pass


# plt.plot(acc)
# plt.pause(0.1)
# plt.close() 
