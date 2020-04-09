
import numpy as np
import copy
from math import sqrt
from collections import OrderedDict
map = [0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,0,0,
       0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,0,0,
       0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
       1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
       1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
       0,1,1,0,0,0,1,1,1,1,1,1,0,0,0,0,0,0,
       0,0,1,0,0,0,1,1,1,1,1,1,0,0,0,0,0,0,
       0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,1,1,0,
       0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,1,1,1,
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
[xpos,ypos]=[9,2]
#save initial
[xposj,yposj]=[xpos,ypos]
#Final Poaition
[xposf,yposf]=[3,15]
# def lets_find_path():
last_closed=[]
def lets_find_path(pathx,pathy,xposf,yposf,xposi,yposi):
    while [xposi,yposi]!=[xposj,yposj]:
        a=[pathx[xposi,yposi]-2,pathy[xposi,yposi]-2]
        #print(type(a))
        final_path.append(a)
        [xposi,yposi]=[pathx[xposi,yposi],pathy[xposi,yposi]]
        print(a)
    print(final_path)
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
                else:
                        closed.append([xpos+a,ypos+b])
    for k in nebr:
        global x0,y0
        x0=k[0]
        y0=k[1]
        e=ocost[xpos,ypos]
        d(xpos,ypos,xposf,yposf,x0,y0)
        ocost[x0,y0]=e+dorigin
        gcost[x0,y0]=dgoal
        addcost[x0,y0]=dorigin+dgoal+e

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
        global final_path
        print(ocost)
        np.savetxt("array3.txt", ocost, fmt="%s")
        final_path=[]
        xpo=xposi-2
        ypo=yposi-2
        final_path.append([xpo,ypo])
        lets_find_path(pathx,pathy,xposf,yposf,xposi,yposi)
        
    #find unique in open
    open= [list(y) for y in set([tuple(x) for x in open])]
    #find unique in closed
    closed= [list(y) for y in set([tuple(x) for x in closed])]



