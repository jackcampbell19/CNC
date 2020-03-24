import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


# Visualizes motor instruction mstp on graph.
def visualize_coordinates(points):

    fig = plt.figure()
    plt.xlim(0, 5000)
    plt.ylim(5000, 0)

    last_point = points[0]
    x = []
    y = []
    mx = []
    my = []
    for i in range(1, len(points)):
        point = points[i]
        if last_point[2] == 0 and point[2] == 0:
            x.append(point[0])
            y.append(point[1])
            # plt.plot([last_point[0], point[0]], [last_point[1], point[1]], 'k-')
        else:
            mx.append(point[0])
            my.append(point[1])
            # plt.plot([last_point[0], point[0]], [last_point[1], point[1]], 'r:')
        last_point = point

    graph, = plt.plot([], [], 'k-')
    graph2, = plt.plot([], [], 'r:')

    # def animate(i):
    #     graph.set_data(x[:i], y[:i])
    #     return graph


    # ani = FuncAnimation(fig, animate, frames=len(x) + 1, interval=400)
    graph.set_data(x, y)
    graph2.set_data(mx, my)
    plt.gca().set_aspect('equal', adjustable='box')
    plt.show()
