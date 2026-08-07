import heapq

grid = [
    [0,0,0,0,0],
    [1,1,0,1,0],
    [0,0,0,1,0],
    [0,1,0,0,0],
    [0,0,0,1,0]
]

rows=len(grid)
cols=len(grid[0])

start=(0,0)
goal=(4,4)

moves=[(1,0),(-1,0),(0,1),(0,-1)]

def heuristic(a,b):
    return abs(a[0]-b[0])+abs(a[1]-b[1])

pq=[]

heapq.heappush(pq,(0,start))

g={start:0}

parent={}

while pq:

    _,current=heapq.heappop(pq)

    if current==goal:
        break

    for dx,dy in moves:

        nx=current[0]+dx
        ny=current[1]+dy

        if 0<=nx<rows and 0<=ny<cols:

            if grid[nx][ny]==0:

                temp=g[current]+1

                if (nx,ny) not in g or temp<g[(nx,ny)]:

                    g[(nx,ny)]=temp

                    f=temp+heuristic((nx,ny),goal)

                    parent[(nx,ny)]=current

                    heapq.heappush(pq,(f,(nx,ny)))

path=[]
node=goal

while node!=start:
    path.append(node)
    node=parent[node]

path.append(start)
path.reverse()

print(path)
