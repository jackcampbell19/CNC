import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


# Visualizes motor instruction mstp on graph.
def visualize_mstp(mstp):
    sequences = mstp
    x = []
    y = []
    for [(x0, y0, z0), sequence] in sequences:
        cx, cy = x0, y0
        for [dx, dy, dz] in sequence:
            cx += dx
            cy += dy
            x.append(cx)
            y.append(cy)

    fig = plt.figure()
    plt.xlim(0, 5000)
    plt.ylim(5000, 0)
    graph, = plt.plot([], [], '.')

    def animate(i):
        graph.set_data(x[:i], y[:i])
        return graph

    # ani = FuncAnimation(fig, animate, frames=len(x) + 1, interval=1)
    graph.set_data(x, y)
    plt.gca().set_aspect('equal', adjustable='box')
    plt.show()
