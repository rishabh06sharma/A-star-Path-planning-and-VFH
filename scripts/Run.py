# import numpy as np
# import copy
# from math import sqrt
# map = [0,0,0,0,0,0,0,0,0,0,0,
#        0,0,0,1,100,0,0,0,0,0,0,
#        0,0,0,1,1,1,1,1,0,0,0,
#        0,0,0,0,0,0,0,0,0,0,0,
#        0,0,0,0,0,0,0,0,0,0,0,
#        0,0,0,0,0,0,0,0,0,0,0]

# #Creating empty list of open and closed nodes
# open=[]
# closed=[]
# #Initializing
#        #size of the map
# x=11
# y=6


# #converting to the 2-D array
# map=np.reshape(np.array(map),(-1,x))

#        #Empty array
# ocost = copy.deepcopy(map)
# gcost = copy.deepcopy(map)
# addcost = copy.deepcopy(map)

# #Initial position
# [xpos,ypos]=[4,7]

# #Final Poaition
# [xposf,yposf]=[1,4]

# #Find distance
# def d(xpos,ypos,xposf,yposf,x0,y0):
#        global dorigin
#        global dgoal
#        dorigin= (sqrt( (xpos - x0)**2 + (ypos - y0)**2 ))*10
#        dgoal= (sqrt( (xposf - x0)**2 + (yposf - y0)**2 ))*10       
# # add indices to the open and closed list
# for a in range(-1,2):
#        for b in range(-1,2):
#               if map[xpos+a,ypos+b]==0 :
#                      open.append([xpos+a,ypos+b])
#               else:
#                      closed.append([xpos+a,ypos+b])
# for k in open:
#        global x0,y0
#        x0=k[0]
#        y0=k[1]
#        d(xpos,ypos,xposf,yposf,x0,y0)
#        ocost[x0,y0]=dorigin
#        gcost[x0,y0]=dgoal
#        addcost[x0,y0]=dorigin+dgoal

# print(ocost)
# print(gcost)
# print(map[1,4])

# print(addcost)
a=[10,2,1]
print(a.index(min(a)))                 