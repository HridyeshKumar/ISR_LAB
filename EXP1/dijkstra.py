import heapq

grid = [
    [0,0,0,0,0],
    [1,1,0,1,0],
    [0,0,0,1,0],
    [0,1,0,0,0],
    [0,0,0,1,0]
]

rows = len(grid)
cols = len(grid[0])

start = (0,0)
goal = (4,4)

moves = [(1,0),(-1,0),(0,1),(0,-1)]

pq = []
heapq.heappush(pq,(0,start))

dist = {start:0}
parent = {}

while pq:
    cost,node = heapq.heappop(pq)

    if node==goal:
        break

    for dx,dy in moves:
        nx=node[0]+dx
        ny=node[1]+dy

        if 0<=nx<rows and 0<=ny<cols:
            if grid[nx][ny]==0:

                newcost=cost+1

                if (nx,ny) not in dist or newcost<dist[(nx,ny)]:
                    dist[(nx,ny)]=newcost
                    parent[(nx,ny)]=node
                    heapq.heappush(pq,(newcost,(nx,ny)))

path=[]
node=goal

while node!=start:
    path.append(node)
    node=parent[node]

path.append(start)
path.reverse()

print("Shortest Path:")
print(path)