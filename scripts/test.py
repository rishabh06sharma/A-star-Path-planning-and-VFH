
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
print(map)
#Empty array
ocost = copy.deepcopy(map)
gcost = copy.deepcopy(map)
addcost = copy.deepcopy(map)
pathx=copy.deepcopy(map)
pathy=copy.deepcopy(map)
#Initial position
x=1
y=12
xd=13
yd=1
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
        #print(type(a))
        final_path.append(a)
        [xposi,yposi]=[pathx[xposi,yposi],pathy[xposi,yposi]]
    print(final_path)
    exit()
def d(xpos,ypos,xposf,yposf,x0,y0):
       global dorigin
       global dgoal
       dorigin= (sqrt( (xpos - x0)**2 + (ypos - y0)**2 ))*10
       dgoal= (sqrt( (xposf - x0)**2 + (yposf - y0)**2 ))*10
for lo in range(0,100):
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
                        if (map[xpos,ypos+1]==1 and map[xpos-1,ypos]==1):
                            open.remove([xpos+a,ypos+b])
                            nebr.remove([xpos+a,ypos+b])
                else:
                        closed.append([xpos+a,ypos+b])
    # print(open)               
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
        addcost[x0,y0]=ocost[x0,y0]+gcost[x0,y0]


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
        # with open("f.txt", "w") as output:
        #         output.write('Map values' + str(addcost) + '\n \n Coordinates-')
    else:
        [xposi,yposi]=[xpos,ypos]
        global final_path
        
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



