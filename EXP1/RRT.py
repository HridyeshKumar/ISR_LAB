import random
import math
import matplotlib.pyplot as plt

start=(1,1)
goal=(9,9)

nodes=[start]
parent={}

step=1

for i in range(500):

    rand=(random.randint(0,10),random.randint(0,10))

    nearest=min(nodes,key=lambda n:(n[0]-rand[0])**2+(n[1]-rand[1])**2)

    angle=math.atan2(rand[1]-nearest[1],rand[0]-nearest[0])

    new=(nearest[0]+step*math.cos(angle),
         nearest[1]+step*math.sin(angle))

    nodes.append(new)
    parent[new]=nearest

    if math.dist(new,goal)<1:

        parent[goal]=new
        break

x=[]
y=[]

for node in nodes:
    x.append(node[0])
    y.append(node[1])

plt.scatter(x,y)
plt.scatter(start[0],start[1],marker="o")
plt.scatter(goal[0],goal[1],marker="*")
plt.title("RRT")
plt.show()