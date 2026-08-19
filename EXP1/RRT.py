import random
import math
import matplotlib.pyplot as plt

# -----------------------------------------
# Start and Goal
# -----------------------------------------

start = (1, 1)
goal = (9, 9)

# -----------------------------------------
# Circular Obstacles
# Format: (x, y, radius)
# -----------------------------------------

obstacles = [
    (3, 4, 1.0),
    (5, 6, 1.0),
    (7, 4, 1.0),
    (6, 8, 0.8)
]

# -----------------------------------------
# RRT Parameters
# -----------------------------------------

nodes = [start]
parent = {}

step = 0.5
max_iterations = 5000


# -----------------------------------------
# Check if point is inside obstacle
# -----------------------------------------

def is_collision(point):

    x, y = point

    for ox, oy, radius in obstacles:

        distance = math.sqrt(
            (x - ox) ** 2 +
            (y - oy) ** 2
        )

        if distance <= radius:
            return True

    return False


# -----------------------------------------
# Check whether line crosses obstacle
# -----------------------------------------

def collision_free(p1, p2):

    distance = math.dist(p1, p2)

    number_of_checks = int(distance / 0.05) + 1

    for i in range(number_of_checks + 1):

        t = i / number_of_checks

        x = p1[0] + t * (p2[0] - p1[0])
        y = p1[1] + t * (p2[1] - p1[1])

        if is_collision((x, y)):
            return False

    return True


# -----------------------------------------
# RRT Algorithm
# -----------------------------------------

goal_reached = False

for i in range(max_iterations):

    # Random point
    random_point = (
        random.uniform(0, 10),
        random.uniform(0, 10)
    )

    # Find nearest node
    nearest = min(
        nodes,
        key=lambda n:
        (n[0] - random_point[0]) ** 2 +
        (n[1] - random_point[1]) ** 2
    )

    # Direction
    angle = math.atan2(
        random_point[1] - nearest[1],
        random_point[0] - nearest[0]
    )

    # New node
    new = (
        nearest[0] + step * math.cos(angle),
        nearest[1] + step * math.sin(angle)
    )

    # Check boundary
    if not (
        0 <= new[0] <= 10 and
        0 <= new[1] <= 10
    ):
        continue

    # Check obstacle collision
    if is_collision(new):
        continue

    # Check path collision
    if not collision_free(nearest, new):
        continue

    # Add node
    nodes.append(new)
    parent[new] = nearest

    # Check goal
    if math.dist(new, goal) <= step:

        if collision_free(new, goal):

            nodes.append(goal)
            parent[goal] = new

            goal_reached = True

            print("Goal Reached!")
            break


# -----------------------------------------
# Construct Final Path
# -----------------------------------------

path = []

if goal_reached:

    current = goal

    while current != start:

        path.append(current)

        current = parent[current]

    path.append(start)

    # Reverse path
    path.reverse()

    print("\nPath from Start to Goal")
    print("------------------------")

    for i, point in enumerate(path):

        print(
            f"Step {i}: "
            f"({point[0]:.2f}, {point[1]:.2f})"
        )

else:

    print("Goal could not be reached.")


# -----------------------------------------
# Plot
# -----------------------------------------

plt.figure(figsize=(9, 9))

# -----------------------------------------
# Draw RRT Tree
# -----------------------------------------

for child, par in parent.items():

    plt.plot(
        [par[0], child[0]],
        [par[1], child[1]],
        linewidth=0.5,
        alpha=0.35
    )


# -----------------------------------------
# Draw Circular Obstacles
# -----------------------------------------

for ox, oy, radius in obstacles:

    circle = plt.Circle(
        (ox, oy),
        radius,
        color="red",
        alpha=0.7
    )

    plt.gca().add_patch(circle)

    # Obstacle symbol "X"
    plt.text(
        ox,
        oy,
        "×",
        fontsize=18,
        ha="center",
        va="center",
        color="white",
        fontweight="bold"
    )


# -----------------------------------------
# Draw Final Path
# -----------------------------------------

if goal_reached:

    path_x = [p[0] for p in path]
    path_y = [p[1] for p in path]

    plt.plot(
        path_x,
        path_y,
        color="black",
        linewidth=3,
        label="Planned Path"
    )


# -----------------------------------------
# Start
# -----------------------------------------

plt.scatter(
    start[0],
    start[1],
    s=180,
    color="green",
    marker="o",
    label="Start"
)


# -----------------------------------------
# Goal
# -----------------------------------------

plt.scatter(
    goal[0],
    goal[1],
    s=250,
    color="blue",
    marker="*",
    label="Goal"
)


# -----------------------------------------
# Graph Settings
# -----------------------------------------

plt.xlim(0, 10)
plt.ylim(0, 10)

plt.xlabel("X Coordinate")
plt.ylabel("Y Coordinate")

plt.title("RRT Path Planning with Circular Obstacles")

plt.grid(True)

plt.legend()

plt.gca().set_aspect("equal")

plt.show()